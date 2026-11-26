# Requisitos — music-library (v1)

> Status: requisitos da v1 consolidados e validados em 2026-11-22. Todas as decisões da seção 3 foram confirmadas.

## 1. Visão e contexto

Aplicação web para catalogar e organizar álbuns de música. Os serviços de streaming oferecem pouca organização para álbuns salvos (o Apple Music é o que chega mais perto, mas ainda pode melhorar). Este app é uma biblioteca própria com estas características:

- os álbuns entram por **busca no MusicBrainz**, com capas do **Cover Art Archive**;
- cada álbum tem **status de escuta**, **nota** e **observação** pessoal;
- a biblioteca pode ser **buscada, filtrada e ordenada** de várias formas;
- há um **sorteio de álbum aleatório** para quando não se sabe o que ouvir;
- o álbum **abre no streaming** por links que o usuário cadastra para qualquer serviço (Tidal, Spotify, Apple Music etc.), e a reprodução não acontece no app.

**Natureza do projeto:** estudo e portfólio. Por isso, qualidade de engenharia (testes, CI, documentação da API) é requisito, não um extra.

## 2. Personas

| Persona | Descrição |
|---|---|
| **Ouvinte organizado** (persona principal) | Ouve álbuns completos, salva muitos e quer saber o que já ouviu, o que achou e o que falta ouvir. |
| **Visitante** | Pessoa sem conta, que só consegue se cadastrar ou entrar. |
| **Avaliador do portfólio** | Recrutador ou dev que lê o código, a documentação da API e o pipeline de CI. Não é usuário do app, mas influencia os requisitos não funcionais. |

## 3. Decisões e suposições

| # | Tema | Decisão |
|---|---|---|
| 1 | Stack | **Python + Django + Django REST Framework + PostgreSQL**. |
| 1a | Frontend | **Templates Django + HTMX**, renderizados no servidor no mesmo domínio do backend. As views HTMX devolvem fragmentos HTML. A **API REST (DRF)** expõe os mesmos recursos (documentação OpenAPI 3/Swagger via `drf-spectacular`, testes e uso futuro). As duas camadas chamam uma **camada de serviços** comum, de modo que a regra de negócio não fica duplicada. |
| 2 | Autenticação | **E-mail/senha e OAuth (Google e GitHub)**, com **"esqueci minha senha"** por e-mail. Sugestão: `django-allauth` + `dj-rest-auth`. |
| 3 | Fonte de metadados | **MusicBrainz** (API pública, sem chave) + **Cover Art Archive** para as capas. |
| 4 | Unidade "álbum" | **A obra** (o *release group* do MusicBrainz), não uma edição específica. |
| 5 | Gênero | Os gêneros vêm do MusicBrainz e o usuário pode editá-los no seu álbum. |
| 6 | Status de escuta | Três status: `quero ouvir` (padrão), `ouvindo`, `já ouvi`. Guarda a data em que o álbum passou a "já ouvi". Não conta quantas vezes foi reouvido na v1. |
| 7 | Links de streaming | **O usuário cadastra os links**, e cada álbum pode ter **vários links, um por serviço** (Tidal, Spotify, Apple Music, Deezer, YouTube Music, Amazon Music, Bandcamp ou "outro"). O serviço é identificado pelo domínio da URL. Ao adicionar um álbum, os links que existirem nas relações de URL do MusicBrainz são importados como ponto de partida e podem ser editados ou removidos. No perfil, o usuário escolhe um **serviço preferido**, que vira o botão principal "Abrir no Tidal" (o usuário troca de serviço com frequência). |
| 8 | Sorteio | **Todos os álbuns elegíveis têm o mesmo peso** (distribuição uniforme). Com 2 ou mais elegíveis, o álbum sorteado logo antes não sai de novo em seguida. |
| 9 | Remoção | Confirmação + "desfazer" por alguns segundos. Sem lixeira. |
| 10 | Visibilidade | A biblioteca é sempre privada na v1. |
| 11 | Dispositivos | Layout responsivo (celular e desktop) desde a v1. |
| 12 | Idioma | Interface em português, com textos preparados para i18n (`gettext`), sem tradução na v1. |
| 13 | Deploy sem custo | Ver a seção 7. |
| 14 | Qualidade | **Sim:** testes automatizados (unidade, integração e e2e), CI no GitHub Actions e documentação OpenAPI 3 com Swagger UI, gerada por `drf-spectacular`. |

## 4. Histórias de usuário

| ID | História |
|---|---|
| US01 | Como visitante, quero criar uma conta com e-mail/senha ou entrar com Google/GitHub para ter minha biblioteca privada. |
| US02 | Como usuário, quero redefinir minha senha por e-mail caso a esqueça. |
| US03 | Como usuário, quero buscar álbuns no MusicBrainz pelo nome ou artista para não precisar digitar os metadados. |
| US04 | Como usuário, quero adicionar um resultado da busca à minha biblioteca. |
| US05 | Como usuário, quero ver minha biblioteca em grade ou lista com as capas. |
| US06 | Como usuário, quero buscar, filtrar e ordenar minha biblioteca para achar álbuns rapidamente. |
| US07 | Como usuário, quero marcar o status de escuta de um álbum. |
| US08 | Como usuário, quero dar uma nota de 1 a 5 e escrever uma observação sobre um álbum. |
| US09 | Como usuário, quero sortear um álbum aleatório, opcionalmente com filtros, para decidir o que ouvir. |
| US10 | Como usuário, quero cadastrar links do álbum em qualquer serviço de streaming e abri-lo no meu serviço preferido com um clique, mesmo quando eu trocar de serviço. |
| US11 | Como usuário, quero remover um álbum da minha biblioteca. |

## 5. Critérios de aceite

### US01 — Cadastro e login
- **Feliz (e-mail):** Dado um e-mail não cadastrado e uma senha válida, quando me cadastro, então a conta é criada e eu fico logado. Sem confirmação de e-mail obrigatória na v1.
- **Feliz (OAuth):** Dado que escolho "Entrar com Google/GitHub" e autorizo, quando volto ao app, então a conta é criada (primeiro acesso) ou eu entro na existente.
- **OAuth com e-mail já cadastrado:** Dado que já tenho conta com e-mail e senha e entro por OAuth com o mesmo e-mail **verificado** pelo provedor, então as contas são vinculadas. Se o e-mail não for verificado pelo provedor, não há vínculo automático.
- **OAuth cancelado ou com erro:** Dado que cancelo a autorização ou o provedor falha, quando volto ao app, então vejo "não foi possível entrar com X" e continuo deslogado.
- **E-mail duplicado:** Dado um e-mail já cadastrado, quando tento cadastrar de novo, então vejo "e-mail já em uso" e nenhuma conta nova é criada.
- **Entrada vazia ou inválida:** Dado e-mail vazio ou mal formatado, ou senha que não passa nos validadores do Django, quando envio, então vejo um erro por campo.
- **Credenciais erradas:** Dado uma senha incorreta, quando faço login, então vejo "e-mail ou senha inválidos", sem indicar qual dos dois está errado.
- **Força bruta:** Dado 5 tentativas falhas em 15 minutos para o mesmo e-mail/IP, quando tento de novo, então recebo 429 e o login fica bloqueado temporariamente.
- **Sem autenticação:** Dado que não estou logado, quando acesso uma rota da biblioteca, então sou redirecionado ao login (ou recebo 401 na API).
- **Isolamento:** Dado que estou logado como A, quando requisito um álbum de B pelo ID, então recebo **404** e nenhum dado de B aparece.
- **Sessão expirada:** Dado um token ou sessão expirada, quando faço uma ação, então sou levado ao login e, depois de entrar, volto à página onde estava.

### US02 — Esqueci minha senha
- **Feliz:** Dado um e-mail cadastrado, quando peço a redefinição, então recebo um link de uso único que expira em 1 hora e, com ele, defino uma nova senha.
- **E-mail inexistente:** Dado um e-mail não cadastrado, quando peço a redefinição, então vejo a **mesma** mensagem do caso feliz ("se o e-mail existir, enviaremos um link"), para não revelar quais e-mails existem.
- **Link expirado ou já usado:** Dado um link vencido ou já usado, quando o abro, então vejo "link inválido ou expirado" e a opção de pedir outro.
- **Conta só OAuth:** Dado uma conta criada só via OAuth, quando peço a redefinição, então recebo o link e posso definir uma senha.
- **Falha no envio do e-mail:** Dado que o provedor de e-mail falha, quando peço a redefinição, então o erro é registrado no log e a mensagem ao usuário continua a mesma.
- **Abuso:** Dado mais de 3 pedidos por hora para o mesmo e-mail, então os pedidos extras são ignorados (rate limit).
- **Sessões antigas:** Dado que redefini a senha, então as sessões e tokens anteriores são invalidados.

### US03 — Buscar no MusicBrainz
- **Feliz:** Dado o termo "Kind of Blue", quando busco, então vejo os *release groups* do tipo álbum com capa, título, artista e ano.
- **Vazio:** Dado um termo vazio ou só com espaços, então a busca não é disparada e o botão fica desabilitado. Na API, isso retorna 400.
- **Sem resultados:** Dado um termo sem correspondência, então vejo "nenhum álbum encontrado".
- **Extremos:** Dado um termo com mais de 200 caracteres, então ele é rejeitado ou truncado. Acentos, emoji e caracteres da sintaxe Lucene (`"`, `:`, `(`) não quebram a busca, pois são escapados.
- **Timeout ou indisponibilidade:** Dado que o MusicBrainz não responde em 5 s ou retorna 5xx, então vejo um erro amigável com "tentar novamente". O backend responde 502/504, nunca 500.
- **Rate limit do MusicBrainz (~1 req/s por IP):** Dado várias buscas seguidas, então o frontend aplica debounce (~400 ms) e o backend limita as chamadas ao MusicBrainz. Um 503 do serviço gera retry com backoff. As requisições enviam um `User-Agent` identificando o app, como a política do MusicBrainz exige.
- **Cache:** Dado uma busca repetida em poucos minutos, então ela é atendida pelo cache, sem nova chamada ao MusicBrainz.
- **Sem capa:** Dado um álbum sem capa no Cover Art Archive (404), então aparece um placeholder.
- **Corrida de respostas:** Dado que busco "A" e logo depois "B", quando "A" responde depois de "B", então a tela mostra só os resultados de "B".

### US04 — Adicionar à biblioteca
- **Feliz:** Dado um resultado de busca, quando clico em "Adicionar", então o álbum entra na biblioteca com o status `quero ouvir` e a data de adição. Os metadados (título, artista, ano, gêneros, capa e os links de streaming que vierem do MusicBrainz) ficam salvos localmente.
- **Duplicado:** Dado um álbum que já está na biblioteca (mesmo MBID de *release group*), quando tento adicionar, então vejo "já está na sua biblioteca" e nenhuma cópia é criada. A API retorna 409.
- **Clique duplo ou duas abas:** Dado duas requisições simultâneas para o mesmo álbum, então só um registro é criado (restrição `UNIQUE(usuario, mbid)` no banco).
- **MBID inexistente:** Dado um MBID inválido ou removido do MusicBrainz, então a adição falha com uma mensagem clara (400/404).
- **Falha ao salvar:** Dado um erro no servidor, então vejo um erro e a interface não mostra o álbum como adicionado.
- **Obra, não edição:** Dado uma obra com várias edições, então é salvo o *release group*, e o resultado da busca não mostra a mesma obra repetida.

### US05 — Ver biblioteca
- **Vazia:** Dado uma biblioteca sem álbuns, então vejo um estado vazio com o atalho "buscar álbuns".
- **Volume:** Dado 5.000 álbuns, então a primeira página (paginação da API, 50 itens) carrega em menos de 2 s e as capas carregam sob demanda.
- **Capa quebrada:** Dado uma URL de capa que falha, então aparece o placeholder.
- **Responsivo:** Em telas de 360 px de largura, a grade se ajusta sem rolagem horizontal.

### US06 — Buscar, filtrar e ordenar
- **Filtros combinados:** Dado os filtros gênero = jazz, década = 1950 e status = já ouvi, então vejo só os álbuns que atendem a todos (E lógico).
- **Filtros disponíveis:** artista, gênero, década, status, nota (mínima), "sem nota".
- **Ordenações disponíveis:** título, artista, ano, nota, data de adição, data em que foi ouvido, em ordem crescente ou decrescente.
- **Nulos na ordenação:** Ao ordenar por nota ou por data de escuta, os álbuns sem valor ficam no fim. Os empates são desempatados por título.
- **Busca textual:** Dado o termo "bjork", então encontro "Björk" (sem distinguir maiúsculas e acentos, com `unaccent` + `icontains` no PostgreSQL).
- **Sem resultado:** Dado filtros sem correspondência, então vejo "nenhum álbum com esses filtros" e a opção "limpar filtros".
- **Estado na URL:** Dado filtros aplicados, quando recarrego a página ou compartilho a URL, então os filtros se mantêm.
- **Parâmetro inválido:** Dado `?decada=abc` ou `?ordering=xyz`, então o valor é ignorado ou substituído pelo padrão. A API nunca responde 500.

### US07 — Status de escuta
- **Feliz:** Dado um álbum em `quero ouvir`, quando mudo para `já ouvi`, então o status e a data de escuta (hoje) são salvos.
- **Transições:** Qualquer status pode ir para qualquer outro. Sair de `já ouvi` limpa a data de escuta.
- **Valor inválido:** Dado um status fora da lista, então a API retorna 400.
- **Concorrência:** Dado alterações em duas abas, então prevalece a última escrita (*last write wins*).
- **Falha de rede:** Dado uma atualização otimista que falha, então a interface volta ao valor anterior e mostra um erro.

### US08 — Nota e observação
- **Feliz:** Dado um álbum, quando dou nota 4 e escrevo uma observação, então os dois são salvos.
- **Extremos:** São aceitas apenas notas inteiras de 1 a 5. Valores como 0, 6, -1, 3.7 e "abc" retornam 400. A observação tem no máximo 2.000 caracteres, com contador na interface, e pode ficar vazia.
- **Remover nota:** Dado um álbum com nota, quando limpo a nota, então ele volta a "sem nota" (nulo).
- **XSS:** Dado uma observação contendo `<script>`, então ela é exibida como texto escapado.

### US09 — Álbum aleatório
- **Feliz:** Dado uma biblioteca com 10 álbuns, quando clico em "Sortear", então vejo um álbum com capa e o botão "abrir no streaming".
- **Com filtros:** Dado os filtros status = quero ouvir e gênero = rock, então o álbum sorteado atende aos filtros.
- **Peso igual:** Todos os álbuns elegíveis têm a mesma probabilidade. Há um teste estatístico: em 10.000 sorteios entre N álbuns, cada um aparece perto de 1/N vezes.
- **Vazio:** Dado zero álbuns elegíveis, então vejo "nenhum álbum para sortear". A API retorna 404 ou corpo vazio, nunca 500.
- **Um só:** Dado 1 álbum elegível, então ele sai sempre.
- **Sem repetição imediata:** Dado 2 ou mais elegíveis, quando sorteio de novo, então o álbum anterior não sai.
- **Escala:** O sorteio não carrega a biblioteca inteira na memória (por exemplo, `COUNT` + `OFFSET` aleatório ou uma seleção por ID).

### US10 — Links de streaming
- **Cadastrar:** Dado um álbum, quando colo `https://tidal.com/browse/album/123`, então o link é salvo e o serviço é identificado como "Tidal".
- **Serviços reconhecidos:** Tidal (`tidal.com`, `listen.tidal.com`), Spotify (`open.spotify.com`), Apple Music (`music.apple.com`), Deezer (`deezer.com`), YouTube Music (`music.youtube.com`), Amazon Music (`music.amazon.*`), Bandcamp (`*.bandcamp.com`). Qualquer outra URL `https://` válida é salva como "Outro", com um nome opcional dado pelo usuário.
- **Um por serviço:** Dado que o álbum já tem um link do Tidal, quando cadastro outro link do Tidal, então ele substitui o anterior, depois de confirmação. Restrição `UNIQUE(album_do_usuario, servico)`; a exceção é "Outro", que permite vários.
- **Editar e remover:** Posso editar ou remover qualquer link, inclusive os importados do MusicBrainz.
- **Importação do MusicBrainz:** Dado que o MusicBrainz tem links de streaming do álbum, quando adiciono o álbum, então eles aparecem já cadastrados. Se o MusicBrainz falhar nessa etapa, o álbum é adicionado mesmo assim, sem links.
- **Serviço preferido:** Dado o serviço preferido "Tidal" no perfil e um álbum com link do Tidal, então o botão principal é "Abrir no Tidal", e os demais links ficam num menu secundário.
- **Preferido ausente:** Dado o preferido "Tidal" e um álbum só com link do Spotify, então o botão principal é "Abrir no Spotify", junto com o atalho "adicionar link do Tidal".
- **Trocar de serviço:** Dado que mudo o preferido de Spotify para Tidal, então o botão principal de todos os álbuns passa a priorizar o Tidal, sem alterar nenhum link salvo.
- **Sem link:** Dado um álbum sem nenhum link, então não há botão de abrir, só "adicionar link".
- **Filtro:** Na biblioteca, posso filtrar "sem link no meu serviço preferido", para completar os links depois de uma troca de serviço.
- **Abrir:** O link abre em nova aba com `rel="noopener noreferrer"`.
- **Link inválido:** Dado `javascript:...`, `data:...`, `http://` (sem TLS), uma URL mal formada ou com mais de 2.000 caracteres, então o link é rejeitado com uma mensagem (400 na API).

### US11 — Remover
- **Feliz:** Dado um álbum, quando removo e confirmo, então ele sai da biblioteca com o status, a nota e a observação.
- **Desfazer:** Logo após remover, aparece "desfazer" por 5 s e o álbum volta com todos os dados, inclusive os links. Pode ser implementado por *soft delete* com limpeza posterior ou por atraso no envio do DELETE.
- **Já removido:** Dado um álbum removido em outra aba, quando removo de novo, então recebo 404, tratado de forma silenciosa na interface.

## 6. Requisitos não funcionais

| Área | Requisito |
|---|---|
| Desempenho | Listagem paginada abaixo de 500 ms no servidor com 5.000 álbuns. Índices em `(usuario, mbid)`, `(usuario, status)` e `(usuario, data_adicao)`. |
| Segurança | HTTPS em produção; senhas com o hasher padrão do Django (PBKDF2/Argon2); CSRF ativo, inclusive nas requisições HTMX (token enviado via `hx-headers`); frontend e API no mesmo domínio, sem necessidade de CORS; segredos só em variáveis de ambiente; `DEBUG=False` em produção. |
| Autorização | Todo *queryset* é filtrado pelo usuário autenticado. Acesso a um recurso de outro usuário retorna 404. |
| Integração externa | Cliente do MusicBrainz isolado num módulo, com timeout de 5 s, retry com backoff, limite de ~1 req/s, `User-Agent` identificado e cache das buscas. |
| Disponibilidade | Se o MusicBrainz cair, a biblioteca local continua funcionando (só a busca externa fica indisponível). |
| Acessibilidade | Navegação por teclado, `alt` nas capas, contraste AA, foco visível. |
| i18n | Textos marcados com `gettext`; datas no fuso `America/Fortaleza` na exibição e em UTC no banco. |
| Observabilidade | Logs estruturados de erros e das chamadas externas (sem dados sensíveis). |
| Qualidade | Testes com pytest + pytest-django (unidade e integração, com o MusicBrainz mockado); testes e2e (por exemplo Playwright); cobertura mínima de 80%; lint e formatação com ruff; checagem de tipos com mypy strict; CI no GitHub Actions rodando lint, tipos, testes e migrações em cada PR; documentação OpenAPI gerada por `drf-spectacular`, com Swagger UI. |

## 7. Deploy sem custo (sugestão)

Planos gratuitos mudam com frequência, então confira as condições atuais antes de adotar qualquer um.

| Peça | Sugestão | Observações |
|---|---|---|
| Backend Django | **Render** (Web Service, plano free) | Faz deploy a partir do GitHub. Entra em hibernação depois de alguns minutos sem uso, e o primeiro acesso leva algumas dezenas de segundos para acordar. Isso é aceitável para portfólio. |
| PostgreSQL | **Neon** (plano free) | Postgres gerenciado e gratuito sem prazo de expiração, ao contrário do Postgres free do Render, que expira. |
| E-mail (redefinir senha) | **Brevo** (free), via **API HTTP** | O Render free bloqueia o envio por SMTP (portas 25, 465 e 587) desde 26/09/2025, então o e-mail sai pela API HTTP do Brevo (~300 e-mails/dia, mais que suficiente). O Brevo aceita um remetente único verificado, sem domínio próprio. Sem domínio próprio, os e-mails podem cair no spam, o que é aceitável para portfólio. Detalhes na decisão D10 de [plano.md](plano.md). |
| Frontend | Junto com o backend | Templates + HTMX são servidos pelo próprio Django. O HTMX é um único arquivo JS, incluído nos estáticos. |
| Arquivos estáticos | **WhiteNoise** | Serve os estáticos pelo próprio Django, sem serviço extra. As capas não são armazenadas, só a URL do Cover Art Archive. |
| Desenvolvimento local | **venv + `make`**, com SQLite por padrão ou Postgres via `DATABASE_URL` | O CI roda o mesmo `make check` contra Postgres 16. Ver a [ADR 0001](decisoes/0001-ambiente-local-sem-docker.md). |

## 8. Fora do escopo da v1
- Reprodução de áudio dentro do app.
- Importação ou sincronização da biblioteca do Spotify/Apple Music (OAuth de streaming).
- Coleções, tags personalizadas e listas ordenadas (candidatas para a v2).
- Perfil público e recursos sociais (seguir, feed, comentários, compartilhamento).
- Scrobble e histórico de reprodução (Last.fm).
- Recomendações inteligentes ou por IA, e sorteio com pesos.
- Cadastro manual de álbuns que não existem no MusicBrainz.
- Importação e exportação (CSV/JSON).
- App mobile nativo.
- Faixas individuais (no máximo, a lista de faixas é exibida, sem interação).
- Contagem de reaudições.
- Confirmação de e-mail no cadastro.

## 9. Questões em aberto
Nenhuma. Novas dúvidas que surgirem na implementação entram aqui.

## 10. Glossário
- **MusicBrainz:** base aberta de metadados musicais, consultada pela API pública.
- **MBID:** identificador único (UUID) de uma entidade no MusicBrainz.
- **Release group:** a "obra" no MusicBrainz, ou seja, o álbum como conceito. Agrupa todas as edições (*releases*).
- **Release:** uma edição específica de uma obra (remaster, vinil, edição de luxo).
- **Cover Art Archive:** serviço parceiro do MusicBrainz que fornece as capas por MBID.
- **HTMX:** biblioteca JS que permite atualizar partes da página com fragmentos HTML vindos do servidor, sem escrever uma SPA.
- **Serviço preferido:** o serviço de streaming escolhido no perfil, priorizado no botão "Abrir no…".
- **Last write wins:** em edições simultâneas, vale a última gravação.
