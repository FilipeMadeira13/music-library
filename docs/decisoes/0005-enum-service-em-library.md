# 0005 — Enum `Service` em `library/choices.py`

- **Status:** Aceita (2026-11-26, tarefa 3, commit `33d7955`)
- **Complementa:** o [plano.md §1–2](../plano.md#2-modelo-de-dados), que cita `choices(Service)` sem dizer onde o enum fica

## Contexto
`User.preferred_service` (tarefa 3, em `accounts`) e `StreamingLink.service` (tarefa 9, em `library`) usam o mesmo conjunto de serviços. O enum precisava existir antes dos models da biblioteca.

## Decisão
- `Service(models.TextChoices)` fica em `library/choices.py`. É a única fonte dos serviços, e os rótulos passam por `gettext_lazy`.
- `accounts` importa de `library`, e nunca o contrário (`library` referencia o usuário só por `settings.AUTH_USER_MODEL`).
- `preferred_service` é `CharField(null=True)`, em que `NULL` quer dizer "não escolhido", como no plano. O ruff DJ001 fica silenciado com justificativa.
- "Outro" pode ser o serviço preferido; o `resolve_buttons` (tarefa 19) trata o caso.

## Consequências
- ➕ As tarefas 9, 10 e 19 reaproveitam o enum sem duplicar.
- ➖ Existe dependência de `accounts` para `library`. Se `library` algum dia precisar importar algo de `accounts`, o enum vai para `core/`.
- Mudar a lista de serviços exige migração em `accounts` e em `library`.
