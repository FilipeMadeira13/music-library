# 0007 — Genéricos do `django-stubs` só sob `TYPE_CHECKING`

- **Status:** Aceita (2026-11-26, tarefa 3, commit `3a098a1`)
- **Complementa:** a [ADR 0002](0002-gate-de-qualidade-estrito.md) (mypy strict com `django-stubs`)

## Contexto
Com mypy strict, `UserAdmin`, `BaseUserCreationForm` e `UserChangeForm` precisam de parâmetro de tipo (`[User]`), mas essas classes só são genéricas no `django-stubs`: em runtime, `UserAdmin[User]` lança `TypeError`. A saída usual, `django_stubs_ext.monkeypatch()` no `settings.py`, exigiria `django-stubs-ext` como dependência de runtime, e hoje ele só existe no ambiente de dev (vem com `django-stubs`).

## Decisão
- A classe base parametrizada é um alias definido sob `if TYPE_CHECKING:`; fora dele, o alias aponta para a classe sem parâmetro. A classe concreta herda do alias:
  ```python
  if TYPE_CHECKING:
      _UserAdminBase = DjangoUserAdmin[User]
  else:
      _UserAdminBase = DjangoUserAdmin
  ```
- O padrão está em `accounts/admin.py` e `accounts/forms.py` e vale para os próximos admins, forms e serializers que precisarem de genéricos só dos stubs.

## Consequências
- ➕ Nenhuma dependência nova em runtime; o mypy enxerga o tipo correto.
- ➖ Quatro linhas de boilerplate por classe base. Se os casos se multiplicarem, reavaliar `django-stubs-ext` + `monkeypatch()` em runtime.
