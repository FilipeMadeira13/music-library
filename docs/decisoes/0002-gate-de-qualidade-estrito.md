# 0002 — Gate de qualidade estrito (`make check`)

- **Status:** Aceita (rascunho registrado em 2026-11-25; decisão tomada no commit `b85399a`, em 2026-11-22)
- **Complementa:** o requisito de qualidade de [requisitos.md §6](../requisitos.md) e as tarefas 1 e 2 do [plano.md](../plano.md), que previam só ruff, `makemigrations --check` e pytest

## Contexto
O projeto é portfólio, e qualidade de engenharia faz parte do requisito. O plano listava só `ruff` como ferramenta de lint, sem tipagem nem hook local.

## Decisão
- **ruff** com `select = ["ALL"]`, ignorando só regras conflitantes com o formatter, docstrings (D100–D107), D203/D213 e CPY001.
- **mypy** com `strict = true`, mais `django-stubs` e `djangorestframework-stubs`.
- **Um único gate**, `make check`: ruff format → ruff check → mypy → `makemigrations --check` → pytest com cobertura ≥ 80% (`--cov-fail-under=80`, com branch coverage).
- Localmente, `make check` aplica format e lint. Com `CI=true`, só verifica.
- O **pre-commit** roda `make check` inteiro em todo commit, além dos hooks básicos (whitespace, EOF, YAML/TOML, merge conflict).
- O CI roda o mesmo `make check`, de modo que local e CI usam um comando só.
- Silenciar uma regra exige justificativa na mesma linha.

## Consequências
- ➕ Erros de tipo e de estilo são barrados antes do commit, e o CI repete exatamente o que roda localmente.
- ➖ Cada commit roda a suíte inteira, e o commit fica mais lento à medida que os testes crescem (os e2e da tarefa 28 devem ficar fora do hook, por exemplo com um marcador `e2e` excluído por padrão).
- ➖ Exceção conhecida: no WSL o ruff não aplica as regras `EXE*`, então um arquivo com shebang sem bit executável só falha no CI (aconteceu com `manage.py`, corrigido em `16f5931`).
