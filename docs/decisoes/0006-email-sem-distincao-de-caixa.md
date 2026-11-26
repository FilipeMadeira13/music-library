# 0006 — E-mail sem distinção de maiúsculas e restrições do `User` no banco

- **Status:** Aceita (2026-11-26, tarefa 3, revisão do commit `33d7955`)
- **Complementa:** o `User` do [plano.md §2](../plano.md#2-modelo-de-dados) (`email unique, login`) e a [ADR 0005](0005-enum-service-em-library.md)

## Contexto
O `BaseUserManager.normalize_email` do Django só põe o **domínio** em minúsculas, e `unique=True` compara o texto exato. Assim, `Ana@x.com` e `ana@x.com` viravam duas contas (fere "e-mail duplicado" da US01), o login falhava se a caixa digitada fosse outra e o vínculo por e-mail do OAuth (tarefa 7) podia não casar. O allauth trata isso nos formulários dele, mas `createsuperuser`, admin, shell e services passam por fora. Além disso, `preferred_service` só era validado em `full_clean()`, e aceitava `""` e `NULL` como "sem preferido".

## Decisão
- O e-mail é guardado **inteiro em minúsculas e sem espaços nas pontas**: `UserManager.normalize_email` faz isso, e `User.save()`, `User.clean()` e `get_by_natural_key` passam por ele.
- `_create_user` rejeita e-mail vazio ou mal formatado (`validate_email`) com `ValueError`.
- No banco: `UniqueConstraint(Lower("email"))`, que cobre escritas sem `save()` (`update()`, SQL), e `CheckConstraint` que aceita só `Service.values` ou `NULL` em `preferred_service`.
- A migração `0002` normaliza as linhas existentes antes de criar as restrições.
- O admin ganha um `UserAdmin` baseado em e-mail (`accounts/admin.py`, `accounts/forms.py`).

## Consequências
- ➕ Um e-mail, uma conta, qualquer que seja a caixa; o login e o vínculo OAuth não dependem de como o usuário digita.
- ➖ Endereços cuja parte local diferencia caixa (permitido pela RFC 5321, raríssimo na prática) passam a ser o mesmo.
- Adicionar um serviço ao enum exige migração que recria o `CheckConstraint` (já era preciso pelas `choices`).
