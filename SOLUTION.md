# BL-01 — Solução em Python e armazenamento local

Decisão registrada em 12/11/2026 a partir de [REQUIREMENTS.md](REQUIREMENTS.md) e dos critérios da [BL-01 em BACKLOG.md](BACKLOG.md#bl-01--escolher-a-solução-mínima-e-o-armazenamento).

**Estado:** decisão documental. A aplicação ainda não foi implementada; as garantias descritas precisam ser verificadas nas tarefas correspondentes. A capacidade de 10.000 álbuns permanece uma hipótese.

## 1. Tecnologias e justificativa

| Escolha | Responsabilidade |
| --- | --- |
| Python | Linguagem da aplicação, das regras e da validação dos dados. |
| Django | Modelos de dados, acesso ao banco e templates, arquivos usados para gerar páginas HTML. |
| Django REST Framework (DRF) | Views, que recebem requisições, e serializers, que validam entradas; respostas HTML com `TemplateHTMLRenderer`. |
| HTML e CSS | Estrutura e aparência das páginas, com formulários nativos do navegador. |
| SQLite | Banco persistido em arquivo no computador do usuário. |

Python, Django e DRF atendem ao foco de aprendizado escolhido pelo usuário. Página, processamento e acesso ao banco ficam em um único projeto. O DRF pode gerar páginas e formulários HTML, conforme sua [documentação oficial](https://www.django-rest-framework.org/topics/html-and-forms/). Django sozinho seria uma alternativa mais simples; o DRF é mantido por escolha de aprendizado. SQLite dispensa administrar um serviço de banco separado e atende à proposta de armazenamento local de uma aplicação pessoal, conforme os [usos recomendados pelo SQLite](https://www.sqlite.org/whentouse.html). PostgreSQL acrescentaria preparação e manutenção sem uma necessidade aprovada neste MVP.

**Fluxo:** navegador → Django/DRF em Python → SQLite → página HTML devolvida ao navegador. Não haverá JavaScript nem aplicação de interface separada. Consultas usam GET; cadastro, edição e restauração usam POST. A navegação usa páginas completas e redirecionamentos; busca e filtros são aplicados ao enviar o formulário. Exportações são entregues como arquivos, e a seleção da cópia usa um campo de arquivo nativo.

Formulários POST devem incluir token e verificação CSRF, proteção contra envios indevidos a partir de outros sites. A verificação será explícita nas views, inclusive sem autenticação: a [documentação do DRF](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication) informa que `SessionAuthentication` não a exige para requisições anônimas. Apenas incluir o token no HTML não basta. Textos informados pelo usuário serão exibidos com o escape dos templates, sem serem interpretados como HTML.

## 2. Ambiente, persistência e leitura

A aplicação será executada no computador, com o servidor vinculado a `127.0.0.1`, acessível apenas localmente e usado em uma sessão por vez. Não exigirá conta, login, APIs de streaming, hospedagem ou serviço pago recorrente. O servidor precisa estar em execução para usar as páginas. Não se acrescenta uma promessa de funcionamento sem internet.

O arquivo SQLite terá um caminho fixo configurado na preparação local. Reabrir a aplicação deve usar o mesmo arquivo; os registros não dependerão do armazenamento do navegador. O arquivo com a coleção pessoal não deve ser versionado no Git. Versões compatíveis de Python, Django, DRF e SQLite e a preparação do banco serão verificadas na BL-03, sem instalações nesta entrega.

| Resultado da leitura | Comportamento obrigatório |
| --- | --- |
| Consulta concluída com zero registros | Informar coleção vazia e permitir cadastro. |
| Erro de acesso, banco ilegível ou falha na consulta | Informar falha de leitura e impedir gravações baseadas na suposição de coleção vazia. |

Após falha, uma nova leitura bem-sucedida é necessária para retomar as operações. Não devolver uma lista vazia como tratamento genérico de exceção, ignorar registros ilegíveis, recriar o banco ou inicializar uma nova coleção para mascarar o erro.

## 3. Gravação integral e restauração

Cadastro, edição e restauração terão suas alterações agrupadas com `transaction.atomic()`: uma transação confirma todas as alterações ou as desfaz em caso de falha. Os erros serão tratados fora do bloco transacional, incluindo falhas ao confirmar a transação. A mensagem de sucesso e o redirecionamento de sucesso só serão produzidos depois que o bloco externo terminar sem erro. Essa estratégia segue a [documentação de transações do Django](https://docs.djangoproject.com/en/5.2/topics/db/transactions/).

Uma falha deve informar que a operação não foi salva e preservar os registros anteriormente confirmados. O formulário pode manter os valores tentados para correção, distinguindo-os dos dados efetivamente salvos. Se a resposta não chegar ao navegador, será necessário reler a coleção antes de concluir se houve gravação ou repetir a tentativa.

Na restauração, o fluxo será:

1. Receber e validar o arquivo inteiro: formato, campos, limites, situações e duplicatas internas, conforme os requisitos.
2. Mostrar uma página avisando que toda a coleção será substituída e permitir confirmar ou cancelar, também para uma cópia vazia.
3. Somente após a confirmação, remover os registros anteriores e inserir todos os registros validados dentro de uma única transação. Não confirmar a remoção separadamente nem mesclar coleções.
4. Confirmar sucesso após concluir a transação; em falha, desfazer a substituição inteira. Cancelamento ou arquivo inválido não alteram a coleção.

A exclusão interna à substituição não acrescenta uma funcionalidade de exclusão de álbuns. O contrato do arquivo pertence à BL-02; exportação, validação e restauração serão implementadas nas tarefas próprias. Exportar deverá ler toda a coleção salva, independentemente dos filtros, e gerar o arquivo completo antes de confirmar sua geração.

## 4. Limitações e hipóteses a comprovar

- **Espaço e permissões:** são necessários acesso ao arquivo e ao diretório e espaço para o banco, os arquivos auxiliares da transação e os arquivos de exportação/restauração. Não haverá uma cota de armazenamento do navegador; o limite relevante será o ambiente local. A recuperação após perda do arquivo depende de uma cópia manual previamente exportada e guardada; não haverá backup automático.
- **Memória e envio de arquivos:** medir o processamento da coleção completa, a geração de páginas e a validação/exportação/restauração. Verificar limites de tamanho de requisições e arquivos do Django com uma cópia válida de 10.000 álbuns, inclusive textos de 200 caracteres e caracteres Unicode; ajustar a configuração quando necessário, sem inventar um limite de álbuns.
- **Comparações:** não presumir que os filtros de texto do SQLite implementam a normalização aprovada de caixa, acentos e espaços. Centralizar essa regra em Python nas tarefas correspondentes, preservando a grafia de exibição. A [documentação do Django sobre SQLite](https://docs.djangoproject.com/en/5.2/ref/databases/#substring-matching-and-case-sensitivity) descreve limitações nas comparações fora de ASCII.
- **Compatibilidade:** verificar todos os fluxos, arquivos, mensagens e acesso por teclado no Chrome e no Firefox estáveis do computador do usuário. Registrar versões e sistema; o resultado de um navegador não comprova o outro.
- **Volume:** executar as operações do MVP com 10.000 álbuns. Não há capacidade medida, tempo máximo aprovado nem rejeição automática acima desse volume. Edição simultânea e sincronização continuam fora do suporte.

## 5. Como provocar e observar falhas nas futuras verificações

Usar bancos descartáveis e dados sintéticos, separados da coleção pessoal. Estes são roteiros futuros, não testes executados.

| Cenário | Como provocar | O que observar |
| --- | --- | --- |
| Coleção vazia versus leitura indisponível — BL-07 | Consultar um banco de teste preparado sem registros; depois injetar um erro de banco na leitura e testar um arquivo ilegível em ambiente temporário. | Mensagens distintas; cadastro permitido somente no caso vazio; nenhuma gravação após leitura falhar; dados anteriores recuperáveis ao restabelecer o acesso. |
| Falha de cadastro ou edição — BL-08 e BL-16 | Injetar erro durante a gravação e na confirmação da transação, partindo de registros conhecidos. | Ausência de sucesso; comparar a coleção inteira antes, depois e após reabrir a conexão/aplicação. |
| Falha durante substituição — BL-21 | Injetar erro após remover os registros anteriores, após inserir parte dos novos e ao confirmar a transação. | A coleção anterior inteira deve reaparecer, sem mistura ou substituição parcial, inclusive após reabertura. |
| Gravação proibida ou sem espaço — BL-08, BL-16 e BL-21 | Usar uma conexão somente leitura; em outro banco descartável, limitar páginas com `max_page_count` e tentar uma gravação que exija crescimento. | Confirmar que a falha foi realmente provocada; informar operação não salva, preservar a coleção anterior e verificar sua leitura após reabrir. |
| Capacidade e recuperação — BL-25 a BL-27 | Preparar dados válidos reproduzíveis, cadastrar de 9.999 para 10.000 e exercitar consulta, filtros, sorteio, edição, reabertura, exportação e restauração. | Conferir contagens e conteúdo completo; registrar espaço, memória, limites de envio, ambiente e resultados separadamente nos dois navegadores. |

O mecanismo para limitar páginas é documentado em [SQLite: `max_page_count`](https://www.sqlite.org/pragma.html#pragma_max_page_count). As simulações verificam o tratamento das falhas previstas; não autorizam alterar permissões ou esgotar espaço da coleção real.

## 6. Revisão documental da BL-01

| Requisito | Decisão que o contempla | Comprovação futura |
| --- | --- | --- |
| RN-09 — Gravação integral | Transação única, erros tratados fora do bloco e sucesso após confirmação; substituição integral. | BL-08, BL-16 e BL-21. |
| RN-10 — Falha de leitura | Coleção vazia exige leitura bem-sucedida; falha não inicia nem sobrescreve coleção. | BL-07. |
| RNF-01 — Persistência e recuperação | Mesmo arquivo SQLite entre aberturas e recuperação por cópia manual. | BL-04, BL-14 e BL-17 a BL-21. |
| RNF-03 — Independência | Uso local sem conta, autenticação ou APIs de streaming. | BL-03 e BL-28. |
| RNF-06 — Capacidade | Hipótese explícita de 10.000 álbuns, com limites locais e de envio identificados. | BL-25 a BL-27. |
| RNF-08 — Custos | Execução local sem hospedagem ou serviço recorrente obrigatório. | BL-03 e BL-28. |

**Resultado da revisão:** os critérios documentais da BL-01 estão contemplados nesta decisão, com riscos e verificações futuras identificados. Foram revisados os requisitos, o backlog e as referências oficiais citadas. Não foram implementados fluxos, instaladas dependências ou executados testes funcionais; preservação dos dados, capacidade e compatibilidade ainda não foram comprovadas em execução.
