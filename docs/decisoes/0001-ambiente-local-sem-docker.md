# 0001 — Ambiente local sem Docker

- **Status:** Aceita (rascunho registrado em 2026-11-25; decisão tomada no commit `b85399a`, em 2026-11-22)
- **Substitui:** a tarefa 1 do [plano.md](../plano.md) ("Docker Compose (web + db)") e a linha "Desenvolvimento local" da seção 7 de [requisitos.md](../requisitos.md)

## Contexto
O plano previa `Dockerfile` + `docker-compose.yml` para ter a mesma configuração em dev e no CI. O desenvolvimento acontece no WSL2, e o bootstrap foi feito sem Docker.

## Decisão
- O ambiente local é um venv Python 3.12 criado por `make install`, e todos os comandos passam pelo `Makefile`.
- `config/settings.py` lê `DATABASE_URL` via `dj-database-url`. Sem a variável, o projeto usa SQLite (`db.sqlite3`).
- O CI (GitHub Actions) roda o mesmo `make check` contra um service Postgres 16, que é a referência de compatibilidade.
- Nada carrega `.env`. O `.env.example` só documenta as variáveis, que precisam ser exportadas no shell.

## Consequências
- ➕ Setup mais rápido e sem depender do Docker Desktop no WSL.
- ➖ O SQLite em dev não cobre recursos específicos do Postgres que o plano usa: a extensão `unaccent`, `UNIQUE` parcial com `WHERE` e `ArrayField` (`mb_genres text[]`). A partir da tarefa 9 (models), testar localmente com Postgres (`DATABASE_URL=…`) ou confiar no CI.
- ➖ Quem copia `.env.example` para `.env` espera que ele seja lido, e não é. Alternativas a decidir: ler o `.env` com `python-dotenv` / `django-environ`, ou carregá-lo no `Makefile`.
- O deploy (tarefa 29) continua sem Docker: o Render roda o build Python nativo.
