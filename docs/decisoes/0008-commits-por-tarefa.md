# 0008 — Um commit `feat:` por tarefa, com `fix:`/`docs:` à parte

- **Status:** Aceita (2026-11-26)
- **Altera:** o título do [plano.md](../plano.md) §5 ("1 commit cada") e a convenção de commits do `CLAUDE.md`

## Contexto
O plano previa exatamente um commit por tarefa. Na tarefa 3, a revisão do `feat:` (`33d7955`) encontrou problemas reais (e-mail com distinção de caixa, restrições só no `full_clean()`), corrigidos em `3a098a1` (`fix:`), e a sincronização das docs ficou para um commit `docs:`. Juntar tudo no `feat:` esconderia o que a revisão mudou.

## Decisão
- Cada tarefa do plano tem **um** commit `feat:` (ou `chore:`, para infraestrutura).
- Correções vindas da revisão vão em commits `fix:` e a sincronização de documentação em `docs:`, na mesma branch e antes do merge.
- Cada commit passa no `make check` sozinho (o pre-commit já garante).

## Consequências
- ➕ O histórico mostra o que a revisão mudou; `git log --oneline --grep '^feat'` continua com uma linha por tarefa.
- ➖ Mais commits por PR.
- Continua em aberto se cada tarefa ganha a própria branch e PR (ver [progresso.md](../progresso.md), dúvidas em aberto).
