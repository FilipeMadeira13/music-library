# Progresso

Diário de sessões: o que foi feito, onde paramos e o que vem a seguir. A sessão mais recente fica no topo.

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
