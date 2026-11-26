# 0003 — Fuso horário de exibição `America/Fortaleza`

- **Status:** Aceita (2026-11-25, commit `7cb4357`)
- **Substitui:** a linha "i18n" da seção 6 de [requisitos.md](../requisitos.md), que previa `America/Sao_Paulo`

## Contexto
O bootstrap (`b85399a`) configurou `TIME_ZONE = "America/Fortaleza"` em `config/settings.py`, enquanto os requisitos pediam `America/Sao_Paulo`. Ao sincronizar a documentação com o código, era preciso escolher um dos dois.

## Decisão
- O fuso de exibição é `America/Fortaleza`. O código fica como está e os requisitos foram ajustados.
- O banco continua guardando datas em UTC (`USE_TZ = True`).

## Consequências
- ➕ Os requisitos, o plano e o código dizem a mesma coisa.
- Desde 2019, nenhum dos dois fusos tem horário de verão e ambos estão em UTC−3, então hoje não há diferença nos horários exibidos. A diferença só apareceria em datas históricas anteriores a 2019 ou se o horário de verão voltar a valer no Sudeste.
- Se no futuro houver usuários em outros fusos, a saída é um fuso por usuário (ativado por middleware), não trocar este valor.
