# 0010 — Senhas de teste geradas em tempo de execução

- **Status:** Aceita (2026-11-26)
- **Complementa:** a [ADR 0002](0002-gate-de-qualidade-estrito.md) (gate de qualidade estrito)

## Contexto
O PR #2 (`feat/custom-user`) passou no CI, mas o check do GitGuardian falhou: 7 incidentes "Generic Password" em `tests/test_accounts_models.py`, nos commits `33d7955` e `3a098a1`. Eram senhas de teste inventadas (como `"s3cret-pass"`), ou seja, falsos positivos. Os testes ainda precisavam de `# noqa: S106` para o ruff aceitar os literais.

Alternativas consideradas:
- **Só ignorar no painel do GitGuardian.** Resolve o PR atual, mas cada teste novo com senha literal abriria outro incidente.
- **`.gitguardian.yaml` ignorando `tests/`.** Também esconderia um segredo real colado por engano num teste.
- **Gerar as senhas nos testes.** Nenhum literal parecido com credencial entra no repositório.

## Decisão
- `tests/conftest.py` expõe os fixtures `password` e `other_password`, que retornam `secrets.token_urlsafe(16)` a cada teste. `other_password` é sempre diferente de `password`.
- Testes não usam senha literal: pedem um desses fixtures (`d88b636`). Os `# noqa: S106` saíram.
- Os incidentes que já estão no histórico (`33d7955`, `3a098a1`) são marcados no painel do GitGuardian como *Ignore → Test credential*. O histórico não é reescrito.
- A regra está no `CLAUDE.md` (Conventions → Tests).

## Consequências
- ➕ O GitGuardian continua varrendo `tests/` sem falsos positivos, e o ruff não precisa de exceção.
- ➕ Cada teste recebe uma senha diferente, então nenhum teste passa por acaso por depender de um valor fixo.
- ➖ Os valores mudam a cada execução. Para depurar uma falha, é preciso imprimir o fixture.
- Os testes de allauth (tarefa 4) e de redefinição de senha (tarefa 6) devem usar os mesmos fixtures.
