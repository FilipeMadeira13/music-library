PYTHON ?= python3.12
VENV   := .venv
BIN    := $(VENV)/bin

# In CI (GitHub sets CI=true) formatting is only verified; locally it is applied.
ifeq ($(CI),true)
FORMAT_CMD := $(BIN)/ruff format --check .
LINT_CMD   := $(BIN)/ruff check .
else
FORMAT_CMD := $(BIN)/ruff format .
LINT_CMD   := $(BIN)/ruff check --fix .
endif

.PHONY: install fmt format lint types migrations-check test check run

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e ".[dev]"
	@if [ -d .git ] && [ "$(CI)" != "true" ]; then $(BIN)/pre-commit install; fi

fmt:
	$(BIN)/ruff format .
	$(BIN)/ruff check --fix .

format:
	$(FORMAT_CMD)

lint:
	$(LINT_CMD)

types:
	$(BIN)/mypy .

migrations-check:
	$(BIN)/python manage.py makemigrations --check --dry-run

test:
	$(BIN)/pytest

check: format lint types migrations-check test

# Local dev server: DEBUG defaults to true so runserver serves static files (admin CSS).
# An explicitly exported DEBUG still wins.
run:
	DEBUG=$${DEBUG:-true} $(BIN)/python manage.py runserver
