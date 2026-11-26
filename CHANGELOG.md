# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- Esqueleto do projeto Django 5.2 + DRF com os apps `core`, `accounts`, `musicbrainz`, `library`, `api` e `web` (`b85399a`).
- Endpoint `GET /healthz` com smoke tests.
- Settings 100% por variáveis de ambiente, com `DATABASE_URL` opcional (SQLite como fallback) e `.env.example`.
- `Makefile` com `make check` como gate único (ruff, mypy strict, `makemigrations --check`, pytest com cobertura ≥ 80%) e hook de pre-commit.
- CI no GitHub Actions rodando `make check` contra Postgres 16.
- Documentação: requisitos, plano técnico, ADRs 0001–0002, README e este changelog.
- Model `User` próprio, com e-mail como login (sem `username`) e serviço de streaming preferido opcional; enum `Service` em `library/choices.py`.
- O e-mail do usuário não diferencia maiúsculas: é guardado em minúsculas, é único no banco por `LOWER(email)` e o login aceita qualquer caixa; o serviço preferido só aceita valores do enum ou vazio (ADR 0006).
- Admin de usuários baseado em e-mail.

### Changed
- Qobuz entra na lista de serviços de streaming reconhecidos (ADR 0004).
- Requisitos: a documentação da API é OpenAPI 3 com Swagger UI, gerada por `drf-spectacular`; a qualidade inclui mypy strict; o ambiente local é um venv, sem Docker; o fuso de exibição é `America/Fortaleza` (ADR 0003).

### Fixed
- `manage.py` passa a ser commitado como executável, o que corrige o ruff EXE001 no CI (`16f5931`).
