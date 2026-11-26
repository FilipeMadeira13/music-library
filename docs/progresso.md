# Progresso

Diário de sessões: o que foi feito, onde paramos e o que vem a seguir. A sessão mais recente fica no topo.

## 2026-11-26

### Feito
- `33d7955` feat: tarefa 3 — `User` custom (e-mail como login, sem `username`, `preferred_service` opcional), enum `Service` em `library/choices.py` com Qobuz ([ADR 0004](decisoes/0004-qobuz.md)) e `accounts/migrations/0001`.
- Revisão do commit acima (`git diff main...HEAD`). Achados e correções, no commit `fix:` seguinte ([ADR 0006](decisoes/0006-email-sem-distincao-de-caixa.md)):
  - **Importante:** o e-mail diferenciava maiúsculas na unicidade e no login (`normalize_email` do Django só baixa o domínio). Agora é guardado inteiro em minúsculas (`UserManager.normalize_email`, `User.save()`, `get_by_natural_key`) e há `UniqueConstraint(Lower("email"))` no banco.
  - `preferred_service` só era validado em `full_clean()`: agora um `CheckConstraint` aceita só `Service.values` ou `NULL` (rejeita `""`).
  - `create_user` rejeita e-mail vazio, só com espaços ou mal formatado.
  - `UserAdmin` e formulários baseados em e-mail (`accounts/admin.py`, `accounts/forms.py`); os genéricos dos stubs ficam atrás de `TYPE_CHECKING`, porque `django_stubs_ext` é só dependência de dev.
  - `accounts/migrations/0002` normaliza as linhas existentes antes de criar as restrições.
  - Testes: `authenticate` com caixa variada e senha errada, duplicata por caixa (via `create_user`, `update()` e `full_clean`), `createsuperuser --noinput`, conta sem senha, coluna `username` ausente no banco, admin (lista, edição, cadastro e duplicata). 35 testes, cobertura 98,8%, só em SQLite.
- `3a098a1` é o commit `fix:` acima.
- Auditoria das docs contra o código desde `main` (`ef407ad`): status, modelo `User` e arquivos da tarefa 3 no `plano.md`; regras de e-mail, direção de import e genéricos dos stubs no `CLAUDE.md`; admin no `README.md`; hashes no `CHANGELOG.md`. ADRs novos: [0007](decisoes/0007-genericos-dos-stubs-sob-type-checking.md) (genéricos dos stubs sob `TYPE_CHECKING`) e [0008](decisoes/0008-commits-por-tarefa.md) (um `feat:` por tarefa, `fix:`/`docs:` à parte).
- `2d13c8c` docs: a auditoria acima, commitada.
- Admin sem CSS no dev: o servidor subia com `DEBUG=False` (o `settings.py` assume `False` sem a variável, e nada carrega o `.env`), e nesse modo o `runserver` não serve `/static/`. O `source .env.example` exportava junto `DATABASE_URL` e trocava o SQLite por um Postgres inexistente. Agora `make run` exporta `DEBUG=true` por padrão e o `.env.example` deixa `DATABASE_URL` comentado ([ADR 0009](decisoes/0009-make-run-com-debug.md)).
- Nova auditoria das docs desde `main` (`ef407ad`): progresso, README, CHANGELOG, plano e índice de ADRs atualizados com a ADR 0009.

### Onde paramos
Branch `feat/custom-user`, com `33d7955`, `3a098a1` e `2d13c8c`, **ainda sem push** (sem upstream). O `db.sqlite3` local já tem `accounts.0001` e `0002` aplicadas.
`Makefile`, `.env.example`, a ADR 0009 e as docs desta auditoria estão **no working tree, sem commit**.

### Próximos passos
1. Commitar as mudanças pendentes (`chore:` para `Makefile` + `.env.example`, `docs:` para o resto), fazer push e abrir o PR de `feat/custom-user`; conferir que o CI passa no Postgres 16 (as restrições novas só foram testadas em SQLite).
2. **Tarefa 4:** allauth com e-mail/senha. Conferir que o allauth não reintroduz e-mail com caixa mista (a normalização do `User.save()` cobre, mas vale um teste de cadastro com `Ana@…` seguido de `ana@…` → "e-mail já em uso").
3. A partir da tarefa 9, testar localmente com Postgres via `DATABASE_URL` ou confiar no CI (ADR 0001).

### Dúvidas em aberto
- As da sessão de 2026-11-25 continuam valendo (`.env`, `dj-rest-auth` no requisito, branch + PR por tarefa, e2e no pre-commit, riscos 5–7 e 10).

## 2026-11-25

### Feito
- `7cb4357` docs: documentação sincronizada com o bootstrap.
  - `plano.md` e `requisitos.md` sem Docker Compose; tarefas 1 e 2 marcadas como entregues; `make check`, mypy strict e `drf-spectacular`/Swagger documentados.
  - Fuso de exibição alinhado ao `settings.py`: `America/Fortaleza` ([ADR 0003](decisoes/0003-fuso-horario-fortaleza.md)).
  - ADR 0001 (ambiente local sem Docker) e ADR 0002 (gate de qualidade estrito), índice em `docs/decisoes/README.md`.
  - `README.md` e `CHANGELOG.md` criados.
  - `CLAUDE.md`: `.env` não é carregado, regra do bit executável, convenção de ADR e changelog.
- `9d9669d` merge do PR #1 (`documentacao-swagger`) em `main`.

### Sessões anteriores (2026-11-22)
- `7bc4b8d` first commit (requisitos e plano).
- `b85399a` chore: bootstrap (tarefas 1 e 2 do plano): esqueleto Django 5.2 com os apps do plano, `/healthz`, ruff `ALL`, mypy strict, pytest com cobertura ≥ 80%, `make check`, pre-commit e CI com Postgres 16.
- `16f5931` fix: `manage.py` commitado como executável (EXE001 só falha no CI, não no WSL).

### Onde paramos
`main` está em `9d9669d`, sincronizada com `origin/main` e com a árvore limpa. Tarefas 1 e 2 entregues; nenhum model ou migração própria existe ainda (`accounts/` só tem `apps.py`, e `AUTH_USER_MODEL` não está definido).

### Próximos passos
1. **Tarefa 3:** `User` custom (e-mail como login, `preferred_service`) e `accounts/migrations/0001`. Definir `AUTH_USER_MODEL = "accounts.User"` **antes** de rodar qualquer `migrate`; se já existir um `db.sqlite3` local com as tabelas padrão do `auth`, apagá-lo.
2. Tarefa 4: allauth com e-mail/senha e templates em PT.
3. A partir da tarefa 9 (models com `unaccent`, `UNIQUE` parcial e `ArrayField`), testar localmente com Postgres via `DATABASE_URL` ou confiar no CI (ADR 0001).

### Dúvidas em aberto
- **`.env`:** continuar sem carregar (só exportar no shell), ou ler com `python-dotenv`/`django-environ` ou pelo `Makefile`? (ADR 0001, Consequências.)
- **`requisitos.md` §3, item 2** ainda sugere `dj-rest-auth`, mas a decisão D1 do plano descarta essa dependência (API só com sessão + CSRF). Ajustar o texto do requisito?
- **Fluxo de trabalho:** a sessão de hoje entrou por branch + PR (#1), enquanto as tarefas 1 e 2 foram commitadas direto em `main`. Adotar branch + PR por tarefa como padrão? A branch `documentacao-swagger` já foi mesclada e pode ser apagada (local e remota).
- **e2e no pre-commit:** quando a tarefa 28 chegar, excluir o marcador `e2e` do hook (ADR 0002) e rodá-lo só no CI?
- Riscos 5–7 e 10 do [plano.md §6](plano.md#6-riscos-e-incertezas) continuam pendentes de confirmação (atualização otimista com HTMX, tolerância do χ² no sorteio, secondary types na busca, 429 do allauth).
