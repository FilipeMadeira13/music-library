# 0009 — `make run` sobe com `DEBUG=true` por padrão

- **Status:** Aceita (2026-11-26)
- **Complementa:** a [ADR 0001](0001-ambiente-local-sem-docker.md) (settings só por variáveis de ambiente, `.env` não é carregado)

## Contexto
`config/settings.py` usa `DEBUG=False` quando a variável não existe, o que é o padrão seguro para produção. Como nada carrega o `.env`, `make run` num terminal novo subia com `DEBUG=False`, e nesse modo o `runserver` não serve `/static/`: o admin abria sem CSS, com 404 em `/static/admin/…`. A saída óbvia, `source .env.example`, também exportava `DATABASE_URL` e trocava o SQLite por um Postgres inexistente (`password authentication failed for user "music"`).

## Decisão
- O alvo `run` do `Makefile` roda `DEBUG=$${DEBUG:-true} … runserver`: no dev, `DEBUG` é `true` por padrão, e um `DEBUG` já exportado continua valendo.
- O default de `settings.py` continua `False`. Produção, CI e testes não passam por `make run`.
- `DATABASE_URL` fica comentado no `.env.example`, para que exportá-lo não troque o banco sem querer.

## Consequências
- ➕ `make run` funciona em qualquer terminal, com o admin estilizado e sem passos manuais.
- ➖ Rodar `manage.py runserver` direto, sem o Makefile, continua com `DEBUG=False`.
- A tarefa 29 (WhiteNoise e `collectstatic`) resolve os estáticos em produção; esta decisão vale só para o dev.
- A dúvida em aberto da ADR 0001 (carregar ou não o `.env`) continua aberta. Se o `.env` passar a ser lido, esta ADR pode ser revista.
