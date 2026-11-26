# music-library

Personal music library (Django 5.2 + DRF + HTMX, PostgreSQL) backed by MusicBrainz.
Requirements: [docs/requisitos.md](docs/requisitos.md). Architecture, data model and task order: [docs/plano.md](docs/plano.md).
Decisions that deviate from or extend the plan: [docs/decisoes/](docs/decisoes/). Notable changes: [CHANGELOG.md](CHANGELOG.md).
Session log (done, where we stopped, next steps, open questions): [docs/progresso.md](docs/progresso.md). Read it at the start of a session and update it at the end.

## Commands
| Command | What it does |
|---|---|
| `make install` | Creates `.venv` (Python 3.12), runs `pip install -e ".[dev]"` and `pre-commit install` |
| `make check` | **Single gate:** ruff format → ruff check → mypy strict → `makemigrations --check` → pytest with coverage ≥ 80%. Locally it applies format/lint fixes; with `CI=true` it only verifies |
| `make fmt` | Applies `ruff format` and `ruff check --fix` |
| `make lint` / `make types` / `make test` | Run each step on its own |
| `.venv/bin/pytest tests/test_smoke.py -k healthz` | Run a single test (coverage threshold applies; add `--no-cov` for quick runs) |
| `make run` | `manage.py runserver` with `DEBUG=true` unless `DEBUG` is already set (needed for admin static files) |
| `.venv/bin/python manage.py migrate` | Apply migrations (SQLite by default) |

Settings read real environment variables only; nothing loads `.env` (export the vars from `.env.example` yourself).
Without `DATABASE_URL` the project uses SQLite (`db.sqlite3`); CI uses Postgres 16.

## Layout
`config/` settings/urls · `core/` cross-cutting (errors, logging, middleware, `/healthz`) · `accounts/` users/auth ·
`musicbrainz/` the only module that talks to the network · `library/` models + business rules (`services.py`) ·
`api/` DRF views (thin) · `web/` HTMX views (thin) · `tests/` pytest suite.

## Conventions
- **Commits:** Conventional Commits (`feat:`, `fix:`, `chore:`, `test:`, `refactor:`, `docs:`), in English. One `feat:` commit per task of `docs/plano.md`; review fixes (`fix:`) and docs (`docs:`) may follow as separate commits on the same branch (ADR 0008). `make check` must be green before committing (the pre-commit hook runs it).
- **Language:** code, identifiers, comments and commit messages in English; user-facing text in Portuguese, always wrapped in `gettext` / `{% translate %}`.
- **Tests:** every new behaviour ships with tests in the same commit. Coverage below 80% fails the build. Never hardcode passwords in tests; use the `password` / `other_password` fixtures from `tests/conftest.py` (GitGuardian flags literals).
- **Strictness:** ruff runs with `select = ["ALL"]` and mypy with `strict = true`. Don't silence a rule without a reason on the same line (`# noqa: XXX - reason`, `# type: ignore[code]  # reason`).
- **Executable bit:** a file with a shebang must be committed as executable (`git update-index --chmod=+x <file>`). ruff's `EXE` rules don't fire under WSL, so only CI catches it.
- **Shared models/enums:** refer to the user via `settings.AUTH_USER_MODEL` / `get_user_model()` (it is `accounts.User`, email login); streaming services come only from `library.choices.Service`. `accounts` may import `library`, never the reverse.
- **E-mail:** stored lower-cased; normalize any e-mail you look up or compare with `User.objects.normalize_email` (ADR 0006).
- **Stub generics:** `django-stubs` generics (`UserAdmin[User]`, `ModelForm[User]`, …) fail at runtime; alias them under `if TYPE_CHECKING:` as in `accounts/forms.py` (ADR 0007).
- **Docs:** a decision that changes or adds to `docs/plano.md` gets an ADR in `docs/decisoes/`; user-visible changes get a line under `[Unreleased]` in `CHANGELOG.md`.
