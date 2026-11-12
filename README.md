# Biblioteca pessoal de álbuns

Aplicação de estudo em Python, Django, Django REST Framework e SQLite, com
páginas HTML em português brasileiro. A BL-03 entrega a página inicial e uma
página introdutória de cadastro. Formulário, gravação e consulta da coleção
serão implementados nas próximas tarefas do [backlog](docs/BACKLOG.md).

## Preparar o ambiente local

Execute os comandos na raiz deste repositório, em um terminal Bash.
É necessário Python 3.12 com `venv` e `pip`, além de um navegador.
A instalação das dependências requer acesso à internet.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --no-cache-dir -r requirements.txt
```

As dependências estão fixadas em `requirements.txt`, incluindo Django 5.2.19 e
DRF 3.18.3. SQLite é acessado pelo módulo `sqlite3` do Python; não é necessário
instalar um serviço de banco separado.

## Configurar e preparar o banco

No mesmo terminal, gere uma chave local sem gravá-la no repositório:

```bash
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
python manage.py migrate
```

O comando `migrate` cria as tabelas iniciais do Django no arquivo
`db.sqlite3`, na raiz do projeto. Não cria álbuns nem uma conta de usuário.
O banco e a `.venv` são ignorados pelo Git. Reaberturas usam o mesmo caminho
de banco, independentemente do diretório de onde o Python for chamado.

Ao abrir outro terminal, ative novamente a `.venv` e defina
`DJANGO_SECRET_KEY` antes de executar qualquer comando do Django.
Para esta etapa, pode gerar outra chave: ainda não há sessões de uso com
dados a preservar. A aplicação apresenta uma orientação se a variável não
estiver definida.

## Verificar e executar

```bash
python manage.py check
python manage.py test
python manage.py runserver 127.0.0.1:8000
```

Abra <http://127.0.0.1:8000/> no navegador. Use `Tab` para focar o link
**Cadastrar álbum** e `Enter` para abrir `/albuns/novo/`. Confira o aviso
**Cadastro em preparação**; use `Tab` e `Enter` no link
**Voltar para a biblioteca**. Os links devem mostrar um contorno de foco.
Encerre o servidor com `Ctrl+C`.

Os dois testes usam `SimpleTestCase`: verificam respostas HTML, idioma,
títulos e links das páginas, sem permitir acesso ao banco. Não verificam
cadastro ou persistência de álbuns.

O servidor é de desenvolvimento, com `DEBUG=True`, para uso local em
`127.0.0.1`. Não é uma configuração de publicação. A aplicação não exige
login, conta ou integração com streaming.

## Decisões e evidências

- [Requisitos](docs/REQUIREMENTS.md)
- [Solução escolhida](docs/SOLUTION.md)
- [Contrato da cópia](docs/BACKUP_FORMAT.md)
- [Backlog e evidências da BL-03](docs/BACKLOG.md#bl-03--preparar-uma-execução-local-verificável)
