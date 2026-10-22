# Music Library

Projeto educacional para organizar uma biblioteca pessoal de álbuns. No estado atual, possui a estrutura inicial do Django, conexão com PostgreSQL e um teste de isolamento do banco. As funcionalidades da biblioteca ainda não foram implementadas.

## Pré-requisitos

- Python 3.13.
- PostgreSQL 16 instalado e em execução.
- Git.
- Terminal Bash em Linux para os comandos abaixo.

Execute os comandos na raiz do projeto. Neste ambiente, `python` aponta para Python 3.13; confira com `python --version` e use `python3.13` na criação do ambiente se necessário.

## Ambiente virtual e dependências

O ambiente virtual mantém as dependências do projeto isoladas. Crie-o uma vez e ative-o:

```bash
python -m venv .venv
source .venv/bin/activate
```

Com o ambiente ativo, instale as versões registradas e confira as dependências:

```bash
python -m pip install -r requirements.txt
python -m pip check
```

Nos próximos terminais, basta ativar novamente a `.venv`.

Para desenvolver, instale as dependências de `requirements-dev.txt`, que inclui as dependências da aplicação e a versão fixada do Ruff:

```bash
python -m pip install -r requirements-dev.txt
```

Esse comando instala os pacotes na `.venv` ativa e pode acessar o índice de pacotes.

## Banco local

Se o usuário e o banco abaixo já existem, pule esta criação. Os comandos modificam o PostgreSQL local e pressupõem uma instalação com o usuário Linux `postgres` e acesso via `sudo`:

```bash
sudo -u postgres createuser --login --createdb --no-superuser --no-createrole --pwprompt music_library_dev
sudo -u postgres createdb --owner=music_library_dev music_library_dev
```

O primeiro comando pede uma senha nova. O usuário terá permissão para criar bancos, necessária para os testes locais, sem ser administrador do PostgreSQL. Essas permissões são destinadas ao desenvolvimento.

## Variáveis de ambiente

O arquivo `.env.example` documenta as seis variáveis necessárias e não contém credenciais reais. Ele é apenas um modelo: a aplicação não carrega arquivos `.env` automaticamente.

Defina as variáveis no mesmo terminal em que executará o Django:

```bash
export DB_NAME=music_library_dev
export DB_USER=music_library_dev
export DB_HOST=localhost
export DB_PORT=5432
read -r -s -p "Senha do banco: " DB_PASSWORD
export DB_PASSWORD
printf '\n'
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
```

Digite a senha criada para o usuário do banco. `read -s` oculta a digitação e evita escrever a senha diretamente no histórico de comandos. O último comando gera uma chave aleatória para o Django e a exporta sem exibi-la. Essa chave assina dados da aplicação; gerar outra invalida assinaturas anteriores e pode invalidar sessões. A geração em cada novo terminal é uma conveniência deste setup local; um ambiente persistente precisa manter sua própria chave protegida e estável.

As variáveis valem para a sessão atual; repita esta etapa em um novo terminal. A configuração exige `DJANGO_SECRET_KEY` e as cinco variáveis `DB_*`; se alguma estiver ausente, a inicialização apresentará erro.

Não coloque credenciais no código, no README ou em arquivos versionados. O `.gitignore` exclui `.env` e permite versionar `.env.example`.

## Migrações

Migrações são instruções versionadas para criar ou alterar tabelas. Confira a configuração e consulte o plano antes de aplicá-las:

```bash
python manage.py check --database default
python manage.py migrate --plan
```

Para aplicar as migrações no banco local configurado e conferir o resultado:

```bash
python manage.py migrate
python manage.py showmigrations
```

`migrate` modifica o banco. Em `showmigrations`, `[X]` indica uma migração aplicada.

## Servidor de desenvolvimento

```bash
python manage.py runserver 127.0.0.1:8000
```

Abra <http://127.0.0.1:8000/>. Nesta etapa, a página inicial padrão do Django é esperada. O servidor fica acessível apenas pela máquina local; encerre com `Ctrl+C`. Ele é destinado ao desenvolvimento.

## Teste do banco

Com a `.venv` ativa e as variáveis configuradas, execute:

```bash
python manage.py test config.test_database --verbosity 2
```

O Django cria `test_music_library_dev`, aplica as migrações, executa o teste e remove o banco de testes ao final. O teste confere o nome do banco conectado para verificar que está separado de `music_library_dev`.

Se aparecer uma pergunta para excluir um banco de testes já existente, interrompa e investigue antes de confirmar. Não use este procedimento com credenciais de produção.

## Lint e formatação

O Ruff verifica problemas comuns no código (lint) e padroniza sua formatação. As regras ficam em `ruff.toml`, com Python 3.13 como alvo, largura de referência de 88 caracteres e verificação da organização dos imports.

Na raiz do projeto, com as dependências de desenvolvimento instaladas, execute:

```bash
python -m ruff check --no-cache .
python -m ruff format --check --no-cache .
```

Esses comandos apenas verificam o código: não alteram arquivos nem acessam o banco. `--no-cache` evita gravar o cache do Ruff. Se houver apontamentos, os comandos retornam um código de saída diferente de zero.

Para reorganizar os imports e aplicar a formatação, execute:

```bash
python -m ruff check --select I --fix --no-cache .
python -m ruff format --no-cache .
```

Esses dois comandos modificam os arquivos Python. Revise as alterações e repita as verificações após aplicá-los. Lint e formatação complementam os testes, mas não verificam as regras de negócio ou a conexão com o banco.

## Integração contínua (CI)

O workflow [CI](.github/workflows/ci.yml) está preparado para executar no GitHub Actions em pushes e pull requests. Ele usa Ubuntu, Python 3.13 e um serviço PostgreSQL 16 temporário, aguardando o banco ficar disponível antes de iniciar as etapas.

As etapas instalam `requirements-dev.txt` e verificam dependências, lint, formatação, configuração Django e alterações de modelos sem migração. Por fim, `python manage.py test --noinput --verbosity 2` descobre e executa os testes, aplicando as migrações no banco de testes.

Os nomes dos bancos são iguais aos do ambiente local para atender ao teste existente, mas os bancos da CI ficam na máquina temporária do GitHub. A senha do banco e a `DJANGO_SECRET_KEY` presentes no workflow são valores públicos exclusivos de testes; não os reutilize fora da CI nem coloque credenciais reais nesse arquivo. O usuário criado pela imagem PostgreSQL é administrador apenas desse serviço temporário.

O workflow consulta o repositório com permissão de leitura e não publica a aplicação. Ele só poderá executar depois que os arquivos forem enviados a um repositório GitHub com Actions habilitado. A primeira execução remota ainda precisa ser verificada na aba **Actions**; a existência do arquivo não comprova que a CI passou. Antes de habilitar execuções, confira as cotas e os limites de gastos da conta.

## Planejamento

- [Escopo](PROJECT_SCOPE.md)
- [Requisitos](REQUIREMENTS.md)
- [Proposta de arquitetura](ARCHITECTURE.md)
- [Backlog](BACKLOG.md)
