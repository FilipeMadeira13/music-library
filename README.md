# music-library

Biblioteca pessoal de álbuns de música: busca no MusicBrainz, status de escuta, nota, filtros, sorteio e links para o seu serviço de streaming.

> Em desenvolvimento. O progresso segue as tarefas de [docs/plano.md](docs/plano.md).

**Stack:** Python 3.12 · Django 5.2 · Django REST Framework · HTMX · PostgreSQL 16

## Rodando localmente
```bash
make install          # cria .venv e instala dependências + pre-commit
make check            # format, lint, mypy, migrações e testes
.venv/bin/python manage.py migrate   # cria as tabelas (SQLite por padrão)
make run              # http://localhost:8000/healthz
```
Para entrar no admin (`/admin/`), crie um usuário com `.venv/bin/python manage.py createsuperuser` (o login é o e-mail).
Sem `DATABASE_URL` o projeto usa SQLite. Para usar Postgres, exporte as variáveis de [.env.example](.env.example). O arquivo `.env` não é carregado automaticamente.

## Documentação
- [Requisitos](docs/requisitos.md)
- [Plano técnico](docs/plano.md): arquitetura, modelo de dados, endpoints e tarefas
- [Decisões (ADRs)](docs/decisoes/)
- [Changelog](CHANGELOG.md)
