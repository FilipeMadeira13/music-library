# Proposta técnica — music-library v1

## Context
O repositório tem só [requisitos.md](requisitos.md) e o projeto começa do zero. Este plano traduz os requisitos em arquitetura, modelo de dados, contratos, estratégia de erros e uma sequência de commits pequenos.

> **Status (2026-11-25):** as tarefas 1 e 2 foram entregues no commit `b85399a` (correção em `16f5931`); a documentação foi sincronizada em `7cb4357`. A próxima é a tarefa 3. Os desvios em relação a este plano estão registrados em [decisoes/](decisoes/) (ADR 0001: ambiente local sem Docker; ADR 0002: gate de qualidade estrito; ADR 0003: fuso `America/Fortaleza`). O diário de sessões fica em [progresso.md](progresso.md).

### Campos preenchidos (tirados do documento de requisitos)
| Campo | Valor |
|---|---|
| LINGUAGEM | Python 3.12 |
| FRAMEWORK | Django 5.2 LTS + Django REST Framework; frontend com templates Django + HTMX (arquivo vendorizado) |
| BANCO | PostgreSQL 16 (Neon free em produção; service do GitHub Actions no CI; em dev, SQLite por padrão ou Postgres via `DATABASE_URL`, ver [ADR 0001](decisoes/0001-ambiente-local-sem-docker.md)) |
| HOSPEDAGEM | Render Web Service free + Neon free + Brevo via API HTTP (e-mail; SMTP bloqueado no Render free) + WhiteNoise (estáticos) |
| LIMITES | Custo zero; sem Redis, sem worker e sem cron (o Render free não tem); instância de ~512 MB que hiberna; MusicBrainz a ~1 req/s por IP com `User-Agent` obrigatório; Neon ~0,5 GB e com autosuspend; e-mail com algumas centenas por dia; cobertura ≥ 80%; resposta < 500 ms com 5.000 álbuns |

---

## 1. Arquitetura

```
 Navegador (HTML + HTMX)            Cliente da API (Swagger, testes, futuro)
        │  sessão + CSRF                     │  sessão + CSRF
        ▼                                    ▼
  web/ (views HTMX, templates)        api/ (DRF views, serializers)
        └──────────────┬─────────────────────┘
                       ▼
            library/services.py  ← regra de negócio única
            library/query.py     ← parse tolerante de filtros/ordenação
            library/streaming.py ← detecção/validação de URL (funções puras)
                       │                     │
                       ▼                     ▼
             models (ORM / Postgres)   musicbrainz/client.py → MusicBrainz API
                                       (timeout, retry, throttle, cache)
  accounts/ (User custom, allauth: e-mail/senha, Google, GitHub, reset, rate limit)
  core/ (settings, erros de domínio, logging, middleware HTMX-auth)
```

| App/módulo | Responsabilidade |
|---|---|
| `config/` | um único `settings.py` em que todo valor que muda por ambiente vem de variável de ambiente; urls, wsgi |
| `core/` | exceções de domínio, handler de exceções do DRF, logging estruturado (JSON), middleware que troca o redirect de login por `HX-Redirect` em requisições HTMX |
| `accounts/` | `User` custom (e-mail como login, `preferred_service`), configuração do allauth, página de perfil |
| `musicbrainz/` | cliente HTTP isolado. Devolve DTOs (`dataclass`) e nunca objetos do ORM. É o único lugar que fala com a rede |
| `library/` | models, `services.py`, `query.py`, `streaming.py`, `random.py` |
| `api/` | serializers e views DRF que apenas validam a entrada, chamam o serviço e serializam a saída |
| `web/` | views que devolvem páginas ou fragmentos HTMX, chamando os mesmos serviços |

Fluxo das duas camadas: a view (API ou web) valida o formato da entrada e chama `services.*(user, ...)`, que aplica a regra de negócio e o escopo por usuário. O serviço devolve um model ou lança um `DomainError`, que a view traduz em JSON ou em fragmento HTML. Toda consulta parte de `UserAlbum.objects.for_user(user)`, de modo que o isolamento fica num único ponto.

**Capas:** o backend não chama o Cover Art Archive. A URL é derivada do MBID (`https://coverartarchive.org/release-group/{mbid}/front-250`), e o `<img loading="lazy">` tem um fallback `onerror` para o placeholder. Isso atende "sem capa", "capa quebrada" e "sob demanda" sem gastar rate limit.

---

## 2. Modelo de dados

```
User (AbstractUser, username removido)
  email            unique, login
  preferred_service  choices(Service) null

Album  — catálogo compartilhado, dados do MusicBrainz, somente leitura para o usuário
  id, mbid UUID unique, title, artist_name, year int null,
  mb_genres text[] (snapshot), fetched_at

Genre
  id, name unique (minúsculo, sem espaços nas pontas)

UserAlbum  — o "álbum na minha biblioteca"
  id, user FK, album FK
  status        enum('want','listening','listened') default 'want'
  rating        smallint null  CHECK 1..5
  notes         text default ''  (máx. 2000 validado no serviço)
  genres        M2M Genre  (copiado do MB ao adicionar e editável)
  added_at, updated_at, listened_at null, deleted_at null
  UNIQUE(user, album) WHERE deleted_at IS NULL
  INDEX (user, status), (user, added_at), (user, listened_at)

StreamingLink
  id, user_album FK (cascade)
  service  enum(tidal, spotify, apple_music, deezer, youtube_music, amazon_music, bandcamp, qobuz, other)
  url      varchar(2000)   label varchar(80) null (só para "other")
  source   enum(musicbrainz, user)   created_at
  UNIQUE(user_album, service) WHERE service <> 'other'
```
- `(usuario, mbid)` dos requisitos vira `(user, album)`, porque `album.mbid` é único.
- `unaccent` é habilitado numa migração (`UnaccentExtension`); o Neon suporta.
- Último álbum sorteado: guardado na sessão (`request.session["last_random_id"]`), sem tabela nova.

### Contratos de serviço (`library/services.py`)
```python
add_album(user, mbid: UUID) -> UserAlbum                 # AlreadyInLibrary, NotFound, ExternalUnavailable
update_album(user, ua_id: int, *, status=UNSET, rating=UNSET,
             notes=UNSET, genres=UNSET) -> UserAlbum      # NotFound, InvalidInput
remove_album(user, ua_id) -> None                         # soft delete; NotFound
restore_album(user, ua_id) -> UserAlbum                   # NotFound (expirado/inexistente)
list_albums(user, q: LibraryQuery) -> QuerySet[UserAlbum]
pick_random(user, q: LibraryQuery, exclude_id: int|None) -> UserAlbum | None
add_link(user, ua_id, url: str, label=None, replace=False) -> StreamingLink   # LinkConflict, InvalidInput
update_link(user, link_id, url=UNSET, label=UNSET) -> StreamingLink
delete_link(user, link_id) -> None
resolve_buttons(ua, preferred: Service|None) -> Buttons(primary, others, suggest_add: Service|None)
set_preferred_service(user, service|None) -> None
```
`library/query.py`: `LibraryQuery.from_params(QueryDict) -> LibraryQuery`. Faz parse tolerante: um valor inválido vira `None`/padrão e nunca lança erro. Campos: `q, artist, genre, decade, status, min_rating, unrated, missing_preferred, ordering`.

`library/streaming.py`: `validate_url(url) -> str` (só https, ≤ 2000 caracteres, host válido, rejeita `javascript:`/`data:`) e `detect_service(url) -> Service`, com tabela de domínios e sufixos (`*.bandcamp.com`, `music.amazon.*`).

`musicbrainz/client.py`:
```python
search_release_groups(term: str, page: int = 1) -> SearchPage  # itens: mbid,title,artist,year,cover_url
get_release_group(mbid: UUID) -> ReleaseGroupDetail             # + genres, url_relations
```
Exceções do cliente: `MBTimeout`, `MBUnavailable`, `MBNotFound`.

### Endpoints da API (`/api/v1/`, sessão + CSRF, JSON)
| Método e rota | Entrada | Saída |
|---|---|---|
| GET `musicbrainz/search?q=&page=` | `q` 1–200 caracteres após trim | 200 `{results:[{mbid,title,artist,year,cover_url,in_library}], page, has_next}`; 400; 502/504 |
| GET `albums?<filtros>&ordering=&page=` | filtros tolerantes | 200 paginado (50) `{count,next,previous,results:[UserAlbum]}` |
| POST `albums` | `{mbid}` | 201 UserAlbum; 400; 404; 409; 502/504 |
| GET/PATCH/DELETE `albums/{id}` | PATCH: `{status?,rating?(int 1–5\|null),notes?,genres?[str]}` | 200 / 204; 400; 404 |
| POST `albums/{id}/restore` | — | 200; 404 |
| GET `albums/random?<filtros>` | exclui o último sorteado (sessão) | 200 UserAlbum; 404 `{error:{code:"no_candidates"}}` |
| GET/POST `albums/{id}/links` | `{url,label?,replace?:bool}` | 201; 400; 409 `link_conflict` (quando `replace` não foi enviado) |
| PATCH/DELETE `links/{id}` | `{url?,label?}` | 200 / 204; 400; 404 |
| GET/PATCH `me` | `{preferred_service}` | 200 |
| GET `genres` | — | 200 gêneros que o usuário usa |
| `/api/schema/`, `/api/docs/` | — | OpenAPI e Swagger (drf-spectacular) |

Formato de `UserAlbum`: `{id, mbid, title, artist, year, cover_url, genres[], status, rating, notes, added_at, listened_at, links:[{id,service,url,label,source}], primary_link}`.

Autenticação (cadastro, login, OAuth, reset) fica nas rotas HTML do allauth em `/accounts/`. A API usa a mesma sessão.

Rotas web: `/` (biblioteca), `/search`, `/albums/<id>`, `/random`, `/profile` e as mesmas ações como `hx-post`/`hx-patch`, devolvendo fragmentos.

---

## 3. Erros e validação

- **Duas camadas de validação:** formato (tipo, tamanho, enum) no serializer do DRF ou no `forms.Form` da view web; regra de negócio (duplicado, conflito de link, transições) no serviço. O banco é a última barreira: `CHECK` na nota e os `UNIQUE` parciais. `IntegrityError` é capturado no serviço e vira `AlreadyInLibrary` ou `LinkConflict`, o que cobre o clique duplo e as duas abas.
- **Hierarquia de exceções (`core/errors.py`):** `DomainError(code, message, status)` com as subclasses `InvalidInput(fields)`=400, `NotFound`=404, `AlreadyInLibrary`/`LinkConflict`=409, `ExternalUnavailable`=502, `ExternalTimeout`=504.
- **API:** um `EXCEPTION_HANDLER` custom produz sempre `{"error":{"code","message","fields"?}}`. Exceções desconhecidas: log com stack e resposta 500 genérica. Erros do MusicBrainz nunca chegam como 500.
- **Web/HTMX:** a view captura `DomainError` e devolve um fragmento de erro com o status correto, usando `HX-Retarget` para a área de mensagens. O HTMX é configurado (`htmx.config.responseHandling`) para trocar o conteúdo em 4xx/5xx. Um handler global `htmx:responseError`/`sendError` mostra um toast e restaura o valor anterior do controle (status ou nota), o que cobre a "atualização otimista que falha".
- **Parâmetros de listagem:** são sempre tolerantes (`LibraryQuery`); um valor inválido é ignorado.
- **Saída:** autoescape do Django em todos os templates, sem `|safe` em conteúdo do usuário. Links com `target="_blank" rel="noopener noreferrer"`.
- **Segurança de autenticação:** os rate limits do allauth (`login_failed: 5/15m` por IP e por chave, retorno 429; `reset_password: 3/h` por chave); `PASSWORD_RESET_TIMEOUT=3600`; troca de senha invalida as outras sessões pelo hash de sessão do Django.
- **Observabilidade:** logger JSON; o cliente do MusicBrainz registra método, URL sem dados do usuário, status, latência e tentativas. Falha no envio de e-mail vai para o log e não muda a resposta ao usuário.

---

## 4. Decisões (2 alternativas e recomendação)

| # | Decisão | A | B | Recomendação |
|---|---|---|---|---|
| D1 | Autenticação da API | **Só sessão + CSRF** (mesmo domínio). Prós: zero dependência extra, um único mecanismo de login, invalidação de sessão já pronta. Contra: inviável para app nativo | **dj-rest-auth + token/JWT**. Prós: API "independente". Contras: +1 dependência, dois fluxos de login para testar e revogar | **A.** Atende aos requisitos; o app nativo está fora do escopo. Se precisar de token no futuro, o allauth `headless` já está incluído no pacote |
| D2 | Brute force e rate limit | **Rate limit nativo do allauth** sobre o cache do Django. Prós: sem dependência, devolve 429 | **django-axes.** Prós: auditoria e bloqueio por usuário. Contras: +1 dependência e configuração extra | **A** |
| D3 | Backend de cache (buscas do MB, rate limits, throttle) | **`DatabaseCache` no Postgres.** Prós: compartilhado entre workers, sem serviço novo. Contra: um pouco mais lento | **Redis (Render Key Value).** Prós: rápido. Contras: mais um serviço, limites do plano free, mais um ponto de falha | **A.** O volume é baixo; o `LocMemCache` quebraria com mais de um worker |
| D4 | Desfazer remoção | **Soft delete** (`deleted_at`) com purga preguiçosa (> 1 min) a cada listagem ou remoção. Prós: robusto a fechar a aba; o restore é trivial e preserva os links. Contras: `UNIQUE` parcial e filtro `deleted_at IS NULL` em toda consulta (centralizado no manager) | **DELETE adiado no cliente** (timer de 5 s). Prós: sem coluna extra. Contras: perde o DELETE se a aba fechar; JS mais frágil; difícil de testar | **A.** A purga é preguiçosa porque o Render free não tem cron |
| D5 | Metadados | **`Album` compartilhado + `UserAlbum`.** Prós: o MB é consultado uma vez por obra; separa os dados do MB dos pessoais. Contra: um join | **Tabela única denormalizada.** Prós: consultas mais simples. Contra: duplica os metadados por usuário | **A.** É um join barato e indexado, e o modelo fica mais claro |
| D6 | Gêneros | **M2M com `Genre`.** Prós: filtro e lista de gêneros simples via ORM, sem SQL cru | **`ArrayField` + GIN.** Prós: uma tabela a menos. Contras: listar os gêneros distintos exige `unnest`; é específico do Postgres | **A** |
| D7 | Filtros e ordenação | **Parser próprio (`LibraryQuery`)** compartilhado entre a web e a API. Prós: tolerante a inválidos como os requisitos pedem; sem dependência | **django-filter.** Prós: padrão do DRF. Contras: por padrão responde 400 para valor inválido; integra mal com as views HTMX | **A** |
| D8 | Sorteio | **`COUNT` + `OFFSET` aleatório** sobre o queryset filtrado, excluindo o último. Prós: uniforme, O(1) em memória, simples | **`ORDER BY random() LIMIT 1`.** Prós: uma linha. Contra: ordena todos os elegíveis (aceitável com 5k, mas não escala) | **A** |
| D9 | Throttle do MusicBrainz | **Gunicorn com 1 worker e threads + `threading.Lock`** espaçando as chamadas em ≥ 1 s, mais o cache. Prós: simples e garantido no processo. Contra: amarra o número de workers | **Slot por segundo no cache compartilhado** (`cache.add("mb:slot:<ts>")`). Prós: funciona com vários workers. Contra: mais código e mais testes | **A.** O plano free comporta só 1 worker mesmo; fica documentado. B é a evolução |
| D10 | Envio de e-mail (**resolvida**: o Render free bloqueia SMTP nas portas 25, 465 e 587 desde 26/09/2025) | **API HTTP do Brevo** via `EmailBackend` próprio (~40 linhas, com `httpx`, que já é dependência). Chamada: `POST https://api.brevo.com/v3/smtp/email` com header `api-key`. Prós: funciona no Render free; ~300 e-mails/dia grátis; aceita remetente único verificado (não exige domínio próprio); fácil de testar com `respx` | **`django-anymail[brevo]`**. Prós: backend pronto e mantido, troca de provedor por configuração. Contra: +1 dependência para um único e-mail transacional. *(Pagar US$ 7/mês para liberar SMTP fica descartado pelo custo zero.)* | **A.** Dev usa `console.EmailBackend` e testes usam `locmem`; produção usa `core.email.BrevoEmailBackend`, escolhido por variável de ambiente. Se o backend próprio crescer, migrar para o B |
| D12 | Importar links de streaming do MusicBrainz (**resolvida com testes reais**: o release group não tem links de streaming; eles ficam nas *releases*) | **Síncrono na adição, com 2 chamadas:** (1) `GET /ws/2/release-group/{mbid}?inc=genres+artist-credits` e (2) `GET /ws/2/release?release-group={mbid}&inc=url-rels&limit=100` (uma página só). Filtrar relações `streaming`, `free streaming` e `purchase for download` (esta só para Bandcamp); mapear com `detect_service`; ficar com 1 por serviço, priorizando edição com status *Official* e depois a URL mais frequente. Prós: sem worker; ~1–2 s com o throttle; uma falha na chamada (2) só deixa o álbum sem links, como o requisito permite | **Sob demanda:** adiciona só com a chamada (1) e mostra no detalhe um botão "importar links do MusicBrainz". Prós: adição mais rápida e menos cota gasta. Contra: o requisito pede os links "já cadastrados" ao adicionar | **A**, com `hx-indicator` (spinner) no botão "Adicionar". A chamada (2) tem orçamento de tempo próprio e, se estourar, é descartada |
| D11 | Testes e2e | **pytest-playwright** (mesmo runner). Prós: integra com pytest-django (`live_server`) | **Cypress.** Contra: ecossistema Node | **A** |

**Dependências (todas justificadas):** runtime com `Django`, `djangorestframework`, `django-allauth[socialaccount]` (e-mail, OAuth, reset e rate limit num pacote só), `drf-spectacular` (OpenAPI exigida), `psycopg[binary]`, `httpx` (timeout e transporte mockável), `gunicorn`, `whitenoise`, `dj-database-url` (para ler `DATABASE_URL` do Neon). Dev com `pytest`, `pytest-django`, `pytest-cov`, `respx` (mock do httpx), `pytest-playwright`, `ruff`, `mypy` + `django-stubs` + `djangorestframework-stubs` (tipagem estrita) e `pre-commit` (ver [ADR 0002](decisoes/0002-gate-de-qualidade-estrito.md)). HTMX vendorizado como arquivo estático. Sem Celery, Redis, django-filter ou dj-rest-auth.

---

## 5. Tarefas (1 commit cada, em ordem)

| # | O que muda | Arquivos | Como testar | Pronto quando |
|---|---|---|---|---|
| 1 ✅ | Esqueleto do projeto: `pyproject.toml`, ruff + mypy strict, settings por env, `Makefile` (`make check`), pre-commit, `.env.example` (sem Docker, ver ADR 0001) | `pyproject.toml`, `config/settings.py`, `Makefile`, `.pre-commit-config.yaml`, `manage.py` | `make check` (1 smoke test) | `/healthz` responde 200 e `make check` passa |
| 2 ✅ | CI no GitHub Actions: `make check` com `CI=true` e Postgres 16 como service (entregue no mesmo commit da tarefa 1) | `.github/workflows/ci.yml` | Abrir um PR | O pipeline fica verde |
| 3 ⏭️ | `User` custom (e-mail como login, `preferred_service`) e primeira migração | `accounts/models.py`, `accounts/migrations/0001*` | Teste de criação de usuário | Migração aplicada, sem `username` |
| 4 | allauth com e-mail/senha: cadastro, login, logout e templates básicos em PT com `gettext` | `config/settings.py`, `accounts/templates/…` | Testes de integração: cadastro feliz, e-mail duplicado, erros por campo, credencial errada com mensagem genérica | Os critérios de US01 de e-mail passam |
| 5 | Rate limit de login (429) e `LOGIN_REQUIRED` nas rotas da biblioteca, com `next=` | settings, `core/middleware.py` (HX-Redirect) | Teste com 6 tentativas resultando em 429; acesso anônimo redireciona; requisição HTMX anônima recebe `HX-Redirect` | Força bruta, sem autenticação e sessão expirada passam |
| 6 | Redefinir senha: timeout de 1 h, mensagem neutra, rate limit 3/h, falha de e-mail só no log | settings, templates | Testes com `mail.outbox`, token usado ou expirado, e-mail inexistente, backend que lança exceção | US02 completa |
| 6b | `BrevoEmailBackend` (D10): monta o JSON (remetente, destinatário, assunto, texto/HTML), timeout de 10 s, loga a falha sem expor o destinatário, respeita `fail_silently`; seleção por `EMAIL_BACKEND` no env | `core/email.py`, `config/settings.py`, `.env.example` | `respx`: 201 → sucesso; 4xx/5xx/timeout → exceção ou `fail_silently`; payload conferido | Backend testado; produção configurável só por env |
| 7 | OAuth Google/GitHub, com vínculo apenas por e-mail verificado e mensagem de erro ou cancelamento | settings, adapter `accounts/adapters.py`, templates | Testes do adapter com `sociallogin` mockado (verificado ou não) e callback de erro | Os critérios de OAuth de US01 passam com mocks |
| 8 | `core/errors.py`, handler de exceções do DRF, logging JSON | `core/errors.py`, `core/logging.py` | Unitários do handler para cada `DomainError` | Formato `{error:{…}}` uniforme |
| 9 | Models `Album`, `Genre`, `UserAlbum`, `StreamingLink`, constraints, índices, extensão `unaccent`, manager `for_user` | `library/models.py`, migrações | Testes de constraint (rating 0/6, `UNIQUE` parcial, link duplicado por serviço, "other" múltiplo) | Migrações aplicadas e constraints testadas |
| 10 | `streaming.py`: `validate_url` e `detect_service` | `library/streaming.py` | Testes parametrizados com todos os domínios e as URLs inválidas da US10 | 100% de cobertura no módulo |
| 11 | Cliente MusicBrainz: busca com escape Lucene, timeout 5 s, retry/backoff em 503, lock de 1 req/s, cache de 10 min, `User-Agent` | `musicbrainz/client.py`, `musicbrainz/dto.py` | `respx`: sucesso, timeout, 5xx, 503 seguido de 200, cache hit, termo com `"():` e emoji | Os critérios de US03 do backend passam |
| 12 | `get_release_group` (gêneros e artista) e `get_streaming_links(mbid)` (browse de releases com `inc=url-rels`, filtro por tipo de relação, 1 por serviço, prioridade *Official* e depois frequência), conforme a D12 | `musicbrainz/client.py`, `musicbrainz/links.py`, `tests/fixtures/mb/*.json` | `respx` com fixtures reais (Kind of Blue: quase sem links; Renaissance: vários por serviço) | DTO completo; a seleção de links é determinística e testada |
| 13 | API de busca `GET /api/v1/musicbrainz/search` (400 vazio/>200, 502/504, `in_library`) | `api/views/search.py`, `api/serializers.py`, `api/urls.py` | Testes de API | US03 na API |
| 14 | Serviço `add_album` e `POST /albums` (201/409/404/502; importa links; falha nos links não impede a adição) | `library/services.py`, `api/views/albums.py` | Testes, incluindo `IntegrityError` simulado que vira 409 | US04 na API |
| 15 | `LibraryQuery`, `list_albums` e `GET /albums` paginado | `library/query.py`, services, api | Testes de cada filtro, combinação com E, nulos no fim, desempate por título, "bjork" encontra "Björk", parâmetros inválidos | US06 na API |
| 16 | `update_album` e `PATCH /albums/{id}` (status com `listened_at`, nota, notas ≤ 2000, gêneros) | services, api | Testes dos extremos de nota e das transições | US07 e US08 na API |
| 17 | `remove_album`/`restore_album` (soft delete + purga) e DELETE/restore | services, api | Testes: restore preserva os links, 404 em remoção repetida, purga, re-adicionar após a purga | US11 na API |
| 18 | `pick_random` e `GET /albums/random` | `library/random.py`, api | Teste estatístico (10k sorteios, tolerância χ²), um elegível, zero elegíveis, sem repetição | US09 na API |
| 19 | CRUD de links, conflito por serviço, `GET/PATCH /me`, `resolve_buttons`, filtro `missing_preferred` | services, api | Testes de preferido presente, ausente, troca e sem link | US10 na API |
| 20 | Teste de isolamento cruzado em todos os endpoints (A não vê nada de B: 404) | `tests/test_isolation.py` | Parametrizado por rota | Todas as rotas retornam 404 |
| 21 | drf-spectacular: schema e Swagger em `/api/docs/` | settings, urls | Teste que gera o schema sem warnings | Docs navegáveis |
| 22 | Layout base: HTMX vendorizado, CSRF via `hx-headers`, toasts, responsivo, acessibilidade (foco e contraste) | `web/templates/base.html`, `static/` | Teste da view; checagem manual a 360 px | Base pronta |
| 23 | Página de busca HTMX: debounce de 400 ms, `hx-sync` para corrida, botão desabilitado, placeholder de capa, adicionar | `web/views/search.py`, templates | Testes de view (fragmento) | US03 e US04 na interface |
| 24 | Biblioteca em grade e lista, filtros na URL, estado vazio, "limpar filtros", paginação | `web/views/library.py`, templates | Testes de view | US05 e US06 na interface |
| 25 | Detalhe do álbum: status, nota e observação (contador), gêneros, rollback em erro | templates, `static/js/app.js` (pequeno) | Testes de view | US07 e US08 na interface |
| 26 | Links na interface: botão principal, menu secundário, atalho "adicionar link do X", confirmação de substituição; perfil com serviço preferido | templates, views | Testes de view | US10 na interface |
| 27 | Remover com confirmação e toast "desfazer" por 5 s; página de sorteio | templates, views | Testes de view | US09 e US11 na interface |
| 28 | E2E com Playwright: cadastro, busca (MB mockado por fixture), adicionar, filtrar, sortear, remover e desfazer, nos viewports 360 px e desktop | `tests/e2e/` | `pytest -m e2e` no CI | E2E verde no CI e cobertura ≥ 80% |
| 29 | Deploy: `render.yaml`, gunicorn com 1 worker, WhiteNoise, settings de produção (HTTPS, HSTS, `DEBUG=False`), Neon, e-mail, OAuth callbacks; README com arquitetura e como rodar | `render.yaml`, `README.md` | Smoke test manual em produção | App público funcionando |
| 30 | Teste de desempenho: seed de 5.000 álbuns e checagem de listagem < 500 ms e contagem de queries (sem N+1) | `tests/test_perf.py`, comando `seed` | `django_assert_max_num_queries` e medição de tempo | Requisito de desempenho verificado |

---

## 6. Riscos e incertezas

1. **Cobertura dos links do MusicBrainz (resolvida na D12, mas é só o melhor possível):** testes reais em 22/11/2026 mostraram links bem diferentes por álbum. *Kind of Blue* (138 edições) tinha só 1 link do Apple Music e 1 do Spotify. *In Rainbows* tinha Spotify e Bandcamp. *Renaissance* tinha Apple, Deezer, Tidal e Spotify, com vários links por serviço, de regiões e edições diferentes. A interface precisa tratar a importação como "ponto de partida". Obras com mais de 100 edições têm só a primeira página consultada.
2. **Entregabilidade do e-mail:** com a D10, o remetente verificado no Brevo sem domínio próprio (por exemplo um Gmail) pode falhar no DMARC e cair no spam. Para portfólio é aceitável; um domínio próprio barato resolve, mas tem custo.
3. **Cold start somado:** Render hibernando e Neon com autosuspend podem levar o primeiro acesso a mais de 30 s. É aceitável para portfólio, mas pode estourar o timeout do OAuth callback ou do primeiro request. Mitigação: página de aviso e `CONN_MAX_AGE` com health checks.
4. **Throttle de 1 req/s com 1 worker:** se o servidor escalar para mais workers ou instâncias, o lock em processo deixa de garantir o limite (aí entra a D9-B). E como o IP de saída do Render é compartilhado, outros apps podem consumir a mesma cota do MusicBrainz e provocar 503 inesperados.
5. **"Atualização otimista" com HTMX:** o HTMX não é otimista por natureza. O comportamento proposto (o controle muda na hora, e um erro restaura o valor anterior) exige um pouco de JS próprio. Confirme se isso basta.
6. **Teste estatístico do sorteio:** com a exclusão do anterior, a distribuição é uniforme entre N−1, não entre N. O teste precisa sortear sem estado de sessão (ou resetá-lo) para validar 1/N. É preciso definir a tolerância (χ² com p > 0,001) para o teste não ser instável.
7. **Busca no MusicBrainz por nome ou artista:** a query Lucene (`releasegroup:… OR artist:…` com `primarytype:album`) afeta a relevância. Coletâneas e ao vivo (*secondary types*) entram ou não? Proponho incluí-las.
8. **Desempenho de `unaccent` + `icontains`** sem índice: deve servir com 5k linhas por usuário (o filtro por usuário vem antes). Se não servir, a saída é `pg_trgm` com uma função imutável, o que acrescenta complexidade.
9. **Planos free mudam** (Render, Neon, Brevo/Resend): as condições precisam ser conferidas no momento do deploy.
10. **Rate limit 429 do allauth:** confirmar na versão escolhida que a resposta é 429 nos fluxos HTML (deve renderizar `429.html`) e que o limite por e-mail e por IP segue o formato de "5 em 15 min".

## Verificação geral
- `make check` (ruff format, ruff check, mypy strict, `makemigrations --check`, pytest com cobertura ≥ 80%), no CI em cada PR e no hook de pre-commit.
- `pytest -m e2e` com Playwright contra `live_server` e o MusicBrainz mockado.
- Swagger em `/api/docs/` gerado sem warnings.
- Smoke test manual em produção: cadastro, OAuth, reset por e-mail real, busca real no MusicBrainz, adicionar, sortear, remover e desfazer.
