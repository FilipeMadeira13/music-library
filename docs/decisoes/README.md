# Registro de decisões (ADRs)

As decisões D1–D12 da proposta original continuam em [plano.md §4](../plano.md#4-decisões-2-alternativas-e-recomendação) e valem como aceitas.
Esta pasta registra as decisões tomadas **depois** do plano, que o alteram ou o complementam.

Formato: um arquivo `NNNN-titulo-curto.md` com as seções Status, Contexto, Decisão e Consequências.

| # | Título | Status | Data |
|---|---|---|---|
| [0001](0001-ambiente-local-sem-docker.md) | Ambiente local sem Docker | Aceita | 2026-11-22 |
| [0002](0002-gate-de-qualidade-estrito.md) | Gate de qualidade estrito (`make check`) | Aceita | 2026-11-22 |
| [0003](0003-fuso-horario-fortaleza.md) | Fuso horário de exibição `America/Fortaleza` | Aceita | 2026-11-25 |
| [0004](0004-qobuz.md) | Qobuz como serviço de streaming | Aceita | 2026-11-26 |
| [0005](0005-enum-service-em-library.md) | Enum `Service` em `library/choices.py` | Aceita | 2026-11-26 |
| [0006](0006-email-sem-distincao-de-caixa.md) | E-mail sem distinção de maiúsculas e restrições do `User` no banco | Aceita | 2026-11-26 |
| [0007](0007-genericos-dos-stubs-sob-type-checking.md) | Genéricos do `django-stubs` só sob `TYPE_CHECKING` | Aceita | 2026-11-26 |
| [0008](0008-commits-por-tarefa.md) | Um commit `feat:` por tarefa, com `fix:`/`docs:` à parte | Aceita | 2026-11-26 |
| [0009](0009-make-run-com-debug.md) | `make run` sobe com `DEBUG=true` por padrão | Aceita | 2026-11-26 |
| [0010](0010-senhas-de-teste-geradas.md) | Senhas de teste geradas em tempo de execução | Aceita | 2026-11-26 |
