# music-library

Personal music library (Django 5.2 + DRF + HTMX, PostgreSQL) backed by MusicBrainz.
Requirements: [docs/requisitos.md](docs/requisitos.md). Architecture, data model and task order: [docs/plano.md](docs/plano.md).

## Commands
| Command | What it does |
|---|---|
| `make install` | Creates `.venv` (Python 3.12), runs `pip install -e ".[dev]"` and `pre-commit install` |
| `make check` | **Single gate:** ruff format → ruff check → mypy strict → `makemigrations --check` → pytest with coverage ≥ 80%. Locally it applies format/lint fixes; with `CI=true` it only verifies |
| `make fmt` | Applies `ruff format` and `ruff check --fix` |
| `make lint` / `make types` / `make test` | Run each step on its own |
| `.venv/bin/pytest tests/test_smoke.py -k healthz` | Run a single test (coverage threshold applies; add `--no-cov` for quick runs) |
| `make run` | `manage.py runserver` |

Without `DATABASE_URL` the project uses SQLite (`db.sqlite3`); CI uses Postgres 16. See `.env.example`.

## Layout
`config/` settings/urls · `core/` cross-cutting (errors, logging, middleware, `/healthz`) · `accounts/` users/auth ·
`musicbrainz/` the only module that talks to the network · `library/` models + business rules (`services.py`) ·
`api/` DRF views (thin) · `web/` HTMX views (thin) · `tests/` pytest suite.

## Conventions
- **Commits:** Conventional Commits (`feat:`, `fix:`, `chore:`, `test:`, `refactor:`, `docs:`), in English, one commit per task of `docs/plano.md`. `make check` must be green before committing (the pre-commit hook runs it).
- **Language:** code, identifiers, comments and commit messages in English; user-facing text in Portuguese, always wrapped in `gettext` / `{% translate %}`.
- **Tests:** every new behaviour ships with tests in the same commit. Coverage below 80% fails the build.
- **Strictness:** ruff runs with `select = ["ALL"]` and mypy with `strict = true`. Don't silence a rule without a reason on the same line (`# noqa: XXX - reason`, `# type: ignore[code]  # reason`).
