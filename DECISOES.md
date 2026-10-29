# Music Library — decisões técnicas da B01

Data: 29/10/2026. Escolhas confirmadas pelo autor e registro autorizado nesta conversa.
Referências: [B01 do backlog](BACKLOG.md#b01--escolher-tecnologias-interface-e-ambiente-local) e [requisitos](REQUIREMENTS.md).

## 1. Escolhas e justificativas

O projeto será uma aplicação local para uma pessoa, desenvolvida em pequenas etapas para aprender backend. As escolhas abaixo definem o mínimo para começar; a preparação do ambiente pertence à B02.

| Parte | Decisão | Justificativa e alternativa considerada |
| --- | --- | --- |
| Linguagem | Python 3.12 | Aproveita o ambiente disponível e a preferência do autor. JavaScript/TypeScript foi apresentado como alternativa. |
| Framework | Django 5.2 LTS | Integra persistência, formulários, templates e testes. LTS significa suporte prolongado. Flask permitiria montar esses componentes separadamente, com mais decisões de integração. |
| Persistência | SQLite em arquivo | Dispensa um servidor separado e permite estudar relações, SQL e transações. PostgreSQL acrescentaria administração de serviço e credenciais. |
| Interface | Navegador local com templates Django, HTML e CSS simples | Permite usar a coleção com páginas e formulários. Terminal e API HTTP foram considerados; o autor escolheu navegador. |
| Ambiente | Linux no WSL2, `venv/` e `pip` | Usa ferramentas padrão do Python para isolar dependências. Poetry foi considerado, mas não escolhido. |
| Testes | Ferramentas nativas do Django, baseadas em `unittest` | Permitem testar regras, persistência e requisições sem acrescentar outra dependência de testes. |

Usar a correção disponível mais recente da série Django 5.2 na B02 e registrar versões exatas das dependências em `requirements.txt`. Registrar também as versões efetivamente usadas de Python e SQLite. A série Python 3.12 foi escolhida; a versão 3.12.3 observada não é uma exigência de fixação e eventuais atualizações dependem da aprovação correspondente.

A documentação oficial informa compatibilidade do Django 5.2 com Python 3.12 e suporte estendido da série até abril de 2028: [compatibilidade](https://docs.djangoproject.com/en/5.2/faq/install/) e [versões suportadas](https://www.djangoproject.com/download/).

## 2. Interface e estrutura mínima

Fluxo principal: **Biblioteca → Artista → Álbuns agrupados por tipo → Detalhes do álbum**.

Na B02 foram criados o projeto Django de configuração (`config`) e o app de biblioteca (`library`), registrado em `INSTALLED_APPS`. Nas tarefas de produto, usar páginas próprias com navegação, formulários, mensagens de validação e confirmações das operações previstas nos requisitos. O painel administrativo do Django não substitui esse fluxo.

Estrutura prevista: `manage.py` na raiz; configurações em `config/`; modelos, formulários, views, URLs, migrações, templates, arquivos estáticos e testes em `library/`. Criar os componentes conforme necessários às tarefas, sem antecipar todas as funcionalidades. O banco local será `db.sqlite3`; testes usarão banco separado.

- **Modelos e restrições:** representam dados, vínculos e unicidade no banco. O ORM é a ferramenta que traduz operações Python em consultas ao banco.
- **Formulários:** validam entradas e apresentam erros que permitam correção.
- **Views:** recebem requisições, coordenam as operações e devolvem páginas. Templates apresentam os resultados; CSS define a aparência.
- **Transações:** agrupam alterações relacionadas para que sejam salvas integralmente ou desfeitas em falha. Usar `transaction.atomic()` nas operações que exigem essa proteção.
- **Testes:** verificam regras e resultados observáveis, incluindo persistência e respostas da interface, com dados isolados da coleção pessoal.

Não haverá contrato de API pública nesta etapa. A interface escolhida usa páginas renderizadas pelo servidor, sem aplicação frontend separada. Hospedagem, autenticação e acesso remoto exigem planejamento próprio antes de publicação.

## 3. Execução local

Com o projeto criado, as dependências instaladas e o ambiente virtual `venv/` preparado na B02, ativar o ambiente na raiz do projeto:

```bash
source venv/bin/activate
```

Na primeira configuração, se ainda não existir `.env`, copiar o modelo:

```bash
cp -n .env.example .env
python -B -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

O comando Python exibe uma chave aleatória. No arquivo `.env`, preencher `DJANGO_SECRET_KEY='chave-gerada'`, substituindo o texto entre aspas pelo resultado e mantendo as aspas simples. Elas preservam caracteres especiais, como `#`, no carregamento pelo `python-dotenv`. Manter a chave entre execuções. O `.env` é ignorado pelo Git e não deve ser compartilhado; o `.env.example` contém apenas o nome da variável, sem segredo real. Uma variável `DJANGO_SECRET_KEY` já definida no ambiente tem prioridade sobre o `.env`.

Sem uma chave preenchida, operações do Django que usam assinatura falham com `ImproperlyConfigured: The SECRET_KEY setting must not be empty.` O teste de idioma e `manage.py check` não comprovam que essa configuração está completa. Para conferir o carregamento e uma operação de assinatura sem exibir a chave nem acessar o banco:

```bash
python -B manage.py shell -c 'from django.core.signing import Signer; s = Signer(); assert s.unsign(s.sign("verificacao-local")) == "verificacao-local"; print("Assinatura verificada.")'
```

Depois de configurar a chave, iniciar a aplicação:

```bash
python -B manage.py migrate
python -B manage.py runserver 127.0.0.1:8000 --noreload
```

`migrate` aplica as migrações — alterações versionadas da estrutura do banco — ao banco local; as 18 migrações internas foram aplicadas pelo autor na B02. Acessar `http://127.0.0.1:8000/` no navegador e encerrar o servidor com `Ctrl+C`. A opção `-B` evita gravar cache de bytecode do Python; `--noreload` desativa o reinício automático quando arquivos mudam.

Para executar os testes, com o ambiente ativado:

```bash
python -B manage.py check
python -B manage.py test
```

Na B02, o executor de testes usou SQLite separado em memória. Os testes de concorrência usarão configuração específica com SQLite de teste em arquivo, nunca o banco da coleção. O servidor de desenvolvimento fica restrito ao endereço local.

## 4. Como verificar os requisitos nas tarefas futuras

| Comportamento | Estratégia planejada |
| --- | --- |
| Persistência — RNF-01, CA-14 | Salvar em SQLite em arquivo; encerrar e reiniciar normalmente e conferir dados alterados e removidos. |
| Integridade e falhas — RNF-02, RNF-03, CA-15 | Proteger vínculos e usar transações nas alterações relacionadas. Provocar falhas controladas entre etapas e verificar reversão integral, ausência de registros órfãos e mensagem sem sucesso falso. |
| Unicidade concorrente — RNF-04, CA-16 | Guardar chaves normalizadas conforme RN-01 e protegê-las com restrições únicas no banco, inclusive a combinação título/artista/ano. Testar criações e edições conflitantes com conexões independentes em banco de teste em arquivo. |
| Sorteio — RNF-05, CA-10 | Produzir uma seleção em que cada álbum apareça uma vez e permitir substituir a fonte de aleatoriedade nos testes. Verificar seleção vazia, candidato único, filtros, probabilidades uniformes pela regra de seleção e preservação dos dados, sem exigir frequências exatas numa amostra. |
| Interface — RNF-02, RNF-05 | Usar o cliente de testes do Django para verificar requisições, mensagens e confirmações; complementar com navegação manual no navegador. Substituir chamadas externas nos testes de abertura de links. |

SQLite admite gravações concorrentes limitadas e pode retornar bloqueio. Restrições únicas são necessárias; validar previamente no formulário não basta. Nas tarefas pertinentes, verificar espera por bloqueios e tratamento de conflitos, sem anunciar sucesso indevido nem aceitar duplicatas. Um erro de bloqueio isolado não comprova o cenário CA-16: os testes devem demonstrar a unicidade e a comunicação do conflito exigidas pelo requisito.

As restrições e transações são recursos disponíveis, não garantias automáticas de que a implementação estará correta. Referências técnicas: [transações](https://docs.djangoproject.com/en/5.2/topics/db/transactions/), [limitações do SQLite](https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes) e [testes do Django](https://docs.djangoproject.com/en/5.2/topics/testing/overview/).

## 5. Evidências e limites das etapas

Na exploração da B01 foram observados Linux no WSL2, Python 3.12.3 e SQLite 3.45.1 acessível pelo Python. Os módulos `venv` e `pip` estavam disponíveis; Django não foi encontrado no interpretador consultado. Isso não comprova a criação de um ambiente virtual nem o funcionamento da aplicação.

A pasta continha os documentos `IDEIA.md`, `REQUIREMENTS.md` e `BACKLOG.md`, sem repositório Git disponível. A B01 registra decisões; não inicializa Git, instala dependências, cria o projeto ou executa testes. Todos os cenários de produto acima permanecem planejados, sem comportamento implementado ou comprovado.

### B02 — ambiente verificado em 29/10/2026

- **Verificado pelo agente:** ambiente virtual `venv/`, Python 3.12.3, SQLite 3.45.1 e Django 5.2.18 instalado; versões exatas das dependências em `requirements.txt`; estrutura `config/` e `library/`, com o app reconhecido pelo Django.
- **Verificações executadas pelo agente:** `python -B manage.py check` sem problemas identificados e `python -B manage.py test` com 1 teste aprovado, `TestLanguageSystem.test_language_pt_br`, usando banco separado em memória. O teste verifica `LANGUAGE_CODE == 'pt-br'` e demonstra que a infraestrutura de testes executa; não comprova funcionalidades da biblioteca. `pip check` também passou na primeira revisão, antes da atualização de Django 5.2 para 5.2.18.
- **Reverificação após documentar a chave local:** `manage.py check` sem problemas identificados, 1 teste aprovado em banco separado em memória e `pip check` sem dependências incompatíveis. A assinatura e sua verificação passaram com a configuração local existente, sem exibir a chave. Também foi validado o conteúdo do `.env.example` preenchido somente em memória com uma chave temporária entre aspas simples, incluindo `#`, carregada pelo `python-dotenv`; a assinatura passou sem alterar o `.env` local. Essa checagem adicional não foi adicionada à suíte de testes.
- **Evidência fornecida pelo autor:** saída de `python -B manage.py runserver 127.0.0.1:8000 --noreload` com inicialização, resposta HTTP 200 para `GET /` e encerramento por `Ctrl+C`. O servidor informou 18 migrações pendentes; depois, o autor forneceu a saída de `python manage.py migrate` com todas as 18 migrações internas aplicadas com sucesso.
- **Limites:** o agente não executou o servidor nem as migrações locais; esses resultados foram conferidos pelas saídas enviadas pelo autor. Não foi demonstrado novo início do servidor após as migrações. A página inicial padrão e o teste de idioma não demonstram cadastro, persistência de artistas ou outros comportamentos de produto; esses cenários permanecem nas próximas tarefas.

**Conclusão:** B01 e B02 concluídas. **Próxima tarefa:** B03, cadastrar artista. O autor continuará responsável por escrever testes e implementação com mentoria.

Revisão breve de aprendizado: por que validar um nome antes de salvar não substitui uma restrição de unicidade no banco quando duas solicitações chegam simultaneamente?
