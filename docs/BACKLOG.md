# Backlog — Biblioteca pessoal de álbuns

Planejamento elaborado em 12/11/2026 a partir de [REQUIREMENTS.md](REQUIREMENTS.md), incluindo a revisão que acrescentou exportação e restauração manual ao MVP.

## 1. Base do plano e limites

- **Objetivo:** construir uma biblioteca pessoal que ajude a reencontrar álbuns e escolher o que ouvir.
- **Estado inicial do planejamento:** na elaboração deste plano, o diretório continha apenas `REQUIREMENTS.md`; ainda não havia implementação, ferramentas de teste ou repositório Git inicializado. A ausência de Git não autorizava inicializá-lo naquela etapa.
- **Decisões da solução:** no início do planejamento, tecnologias, local de armazenamento e formato técnico da cópia estavam em aberto. As tecnologias e o armazenamento foram definidos na BL-01, em [SOLUTION.md](SOLUTION.md); o contrato da cópia foi definido na BL-02, em [BACKUP_FORMAT.md](BACKUP_FORMAT.md), com as decisões de validação confirmadas pelo usuário e sem ampliar o escopo do MVP.
- **Ambiente aprovado:** navegador em computador, no próprio perfil, uma sessão por vez; Chrome e Firefox estáveis no momento da verificação, sem custos recorrentes obrigatórios.
- **Estado das entregas:** BL-01 e BL-02 concluídas por revisão documental; BL-03 concluída com execução local, testes das páginas iniciais e verificação de navegação no Chrome. Os fluxos da coleção ainda não foram implementados nem verificados; suas evidências pertencem às tarefas seguintes.
- **Ritmo:** uma microtarefa por vez, sem prazo fixo. Não há estimativas de duração enquanto as tecnologias e o ambiente de trabalho não forem escolhidos.

## 2. MVP, melhorias e exclusões

**MVP obrigatório:** cadastrar título, artista e situação; consultar por artista; buscar por título; filtrar por situação; sortear entre os resultados atuais; editar; recuperar dados entre sessões; exportar toda a coleção e restaurar uma cópia validada, com confirmação de substituição e preservação dos dados em falhas. Inclui as qualidades e os limites aprovados: português brasileiro, segurança no tratamento de texto, acessibilidade e capacidade de 10.000 álbuns.

**Depois do MVP:** gênero e ano/década de lançamento. AD-01 e AD-02 são tarefas de refinamento desses requisitos, sem autorização para implementá-los agora.

**Fora do MVP:** integração com streaming, reprodução, recomendações automáticas, compartilhamento, sincronização, edição simultânea e backup automático.

**Sem requisito aprovado:** exclusão de álbuns, capas, links para streaming, contas e importação de fontes externas. Restaurar o arquivo próprio da aplicação não autoriza outros tipos de importação. Não há promessa de funcionamento sem internet, senha própria ou isolamento em dispositivo compartilhado.

## 3. Como executar e verificar as tarefas

**Prioridades:** P0 resolve decisões e preparação que bloqueiam o desenvolvimento; P1 entrega e verifica o MVP; P2 refina melhorias posteriores. Todos os itens P0 e P1 são necessários para encerrar o MVP. A numeração indica uma ordem recomendada dentro dessas prioridades; apenas as dependências listadas são obrigatórias.

**Dependência** é uma tarefa que precisa estar concluída para outra começar. Quando uma tarefa não depende de outra, pode ser antecipada ou trabalhada separadamente; isso não exige trabalho simultâneo nem divisão entre pessoas.

**Fluxo por tarefa:** escolher o item, conferir seus exemplos, escrever um teste que falhe, implementar o mínimo para passar e melhorar a organização preservando o comportamento, quando esse ciclo fizer sentido. Esse é o ciclo TDD: RED → GREEN → REFACTOR. Decisões documentais, preparação do ambiente e avaliação de uso terão evidência apropriada, sem testes artificiais.

**Pronto por tarefa:** critérios atendidos, testes aplicáveis executados, evidência registrada com resultado real e riscos ou limitações conhecidos anotados. A pessoa desenvolvedora escreve os testes e a implementação, com apoio de mentoria. Escolher uma tarefa não autoriza automaticamente instalações, mudanças no Git, ações externas ou outras operações que exijam aprovação.

Desde a primeira interface, usar rótulos, foco visível, mensagens em português e conteúdo tratado como texto. Desde a primeira gravação, evitar confirmar sucesso antes de salvar. As tarefas específicas de falha e acessibilidade completam e verificam esses comportamentos; não são motivo para adiá-los. Marcos intermediários não significam que o MVP está pronto para receber a coleção real.

Os exemplos CA-01 a CA-33 e as regras de `REQUIREMENTS.md` são a fonte dos testes. Cada tarefa aponta os cenários principais; a matriz ao final ajuda a conferir a cobertura.

## 4. P0 — Decisões e preparação

### BL-01 — Escolher a solução mínima e o armazenamento

- [x] Concluída
- **Estado:** decisão documental registrada e revisada em [SOLUTION.md](SOLUTION.md), em 12/11/2026. As verificações de implementação, falhas e capacidade permanecem nas tarefas correspondentes.
- **Objetivo:** registrar uma decisão curta que permita começar sem comprometer a preservação dos dados.
- **Dependências:** nenhuma.
- **Critérios de aceitação:** escolher as tecnologias e o armazenamento com justificativa para uso no navegador, uma sessão, ausência de conta e custos recorrentes obrigatórios; explicar como distinguir coleção vazia de falha de leitura e como salvar ou substituir a coleção integralmente, sem deixar alterações parciais; identificar restrições de espaço e compatibilidade que precisarão de comprovação com 10.000 álbuns.
- **Testes/evidência:** revisar a decisão contra RN-09, RN-10 e RNF-01, RNF-03, RNF-06 e RNF-08; registrar como provocar e observar falhas nas futuras verificações. Uma capacidade ainda não medida deve ficar indicada como hipótese.
- **Riscos:** escolher armazenamento que não permita preservar a coleção em falhas; depender de serviço pago; transformar a decisão em uma arquitetura maior que o necessário.

### BL-02 — Definir o contrato do arquivo de cópia

- [x] Concluída
- **Estado:** contrato definido e revisado em [BACKUP_FORMAT.md](BACKUP_FORMAT.md), em 12/11/2026. Conferidas a sintaxe dos cinco exemplos JSON e, por revisão documental, as regras e a correspondência com CA-26 a CA-31 e o caso de cópia vazia. Exportação, validação e restauração ainda dependem de implementação e testes nas tarefas correspondentes.
- **Objetivo:** descrever o que torna um arquivo próprio válido para exportação e restauração.
- **Dependências:** BL-01.
- **Critérios de aceitação:** definir estrutura, identificação do formato e política para formatos incompatíveis; representar título, artista e situação de todos os registros e uma coleção vazia; prever validação integral de limites, valores e duplicatas; deixar explícito que restaurar substitui, sem mesclar. Preservar a grafia de exibição prevista nos requisitos. Não adicionar campos de produto nem exigir recursos não aprovados.
- **Testes/evidência:** apresentar exemplos mínimos de cópia válida, vazia, incompatível e inválida; conferir que o contrato permite CA-26 a CA-31 e o caso de cópia vazia da seção 8.
- **Riscos:** formato ambíguo ou incapaz de recuperar os mesmos dados; aceitar apenas uma parte de um arquivo inválido; inventar suporte a formatos externos.

### BL-03 — Preparar uma execução local verificável

- [x] Concluída
- **Estado:** estrutura inicial implementada e verificada em 12/11/2026 na branch `feat/bl-03-execucao-local`. Preparação e comandos de uso documentados no [README.md](../README.md).
- **Objetivo:** conseguir abrir a aplicação no ambiente escolhido e executar uma primeira verificação útil.
- **Dependências:** BL-01.
- **Critérios de aceitação:** documentar os comandos mínimos para executar e verificar o projeto; abrir a estrutura inicial em português, com acesso ao início do cadastro; preparar apenas as ferramentas necessárias. Obter aprovação antes de instalações, configurações ou mudanças no Git que venham a ser necessárias.
- **Testes/evidência:** executar o comando documentado e uma verificação de abertura da aplicação; registrar o resultado e o ambiente. Essa abertura não comprova persistência nem os fluxos do MVP.
- **Riscos:** instalar ferramentas sem necessidade; depender de configuração não documentada; gerar funcionalidades fora do escopo.

**Evidências da execução:**

| Verificação | Resultado observado |
| --- | --- |
| Ambiente | Ubuntu 24.04.3 LTS, Linux x86_64; Python 3.12.3; SQLite 3.45.1; Google Chrome 146.0.7680.164. |
| Preparação | `.venv` criada; Django 5.2.19, DRF 3.18.3, asgiref 3.13.0 e sqlparse 0.6.1 instalados; versões fixadas em `requirements.txt`. |
| Banco | `python manage.py migrate` aplicou as migrações iniciais do Django em `BASE_DIR / "db.sqlite3"`. Nenhum modelo de álbum foi criado. |
| RED | `python manage.py test --verbosity 2`: dois testes falharam com `404 != 200` antes de implementar as rotas. |
| GREEN | O mesmo comando passou com dois testes `SimpleTestCase`: HTML, idioma, títulos e links das duas páginas. O runner informou que o banco não foi utilizado. |
| Configuração e dependências | `python manage.py check`: nenhuma ocorrência; `python -m pip check`: nenhuma dependência incompatível. |
| Abertura | `python manage.py runserver 127.0.0.1:8000` iniciou o servidor local. As páginas `/` e `/albuns/novo/` responderam HTTP 200. |
| Navegação no Chrome | Automação via Chrome DevTools Protocol em modo headless, com perfil temporário: início → cadastro → início usando Tab/Enter. O cadastro mostrou “Cadastro em preparação”. |
| Foco e apresentação | Nos dois links, `:focus-visible` ativo e contorno sólido de 3 px; capturas das páginas inspecionadas em viewport de 1280 × 800. |
| Arquivos locais | Conferido com `git check-ignore` que `.venv`, banco SQLite, arquivos auxiliares e `.env` ficam fora do versionamento. A chave é recebida por `DJANGO_SECRET_KEY`. |

**Limites da evidência:** verificação de navegador automatizada, sem avaliação manual por uma pessoa. Firefox não foi verificado. A execução local e as migrações iniciais não comprovam cadastro, leitura da coleção, persistência de álbuns, proteção dos futuros formulários POST ou capacidade de 10.000 álbuns. Esses comportamentos permanecem nas tarefas correspondentes.

## 5. P1 — Primeira coleção persistida com segurança

### BL-04 — Cadastrar um álbum válido e recuperá-lo ao reabrir

- [ ] Concluída
- **Objetivo:** completar a primeira fatia vertical: formulário, gravação e visualização do álbum após reabertura.
- **Dependências:** BL-03.
- **Critérios de aceitação:** informar título, artista e uma das duas situações; retirar espaços nas pontas de título e artista, preservando a grafia restante; confirmar somente após salvar; mostrar os valores salvos e recuperá-los ao encerrar e reabrir no mesmo ambiente.
- **Testes/evidência:** CA-01 e a parte de cadastro de CA-19, com exemplos nas duas situações; verificar que os dados exibidos são os efetivamente gravados.
- **Riscos:** exibir sucesso antes da gravação; salvar apenas em memória; modificar a grafia além da regra aprovada.

### BL-05 — Rejeitar campos inválidos e acima do limite no cadastro

- [ ] Concluída
- **Objetivo:** impedir registros incompletos e explicar como corrigir cada entrada.
- **Dependências:** BL-04.
- **Critérios de aceitação:** rejeitar título/artista ausente, vazio ou só com espaços; rejeitar situação diferente de `quero ouvir` e `já ouvi`; aceitar textos válidos de 200 caracteres e rejeitar 201 sem truncar nem criar registros parciais; identificar o campo e o limite em português.
- **Testes/evidência:** CA-02, CA-24 e cadastro de CA-25, incluindo a verificação da coleção antes e depois de cada rejeição.
- **Riscos:** validar apenas o formulário e permitir dados inválidos no salvamento; cortar texto silenciosamente; mostrar erro sem indicar o campo.

### BL-06 — Bloquear duplicatas usando a comparação aprovada

- [ ] Concluída
- **Objetivo:** impedir álbuns equivalentes sem impedir o mesmo título com outro artista.
- **Dependências:** BL-05.
- **Critérios de aceitação:** comparar título e artista ignorando caixa, acentos, espaços nas pontas e espaços internos excedentes; bloquear o par equivalente independentemente da situação; permitir mesmo título com artista diferente. Usar a mesma regra nas futuras consultas, edições e restaurações, sem alterar a grafia exibida além da remoção de espaços nas pontas.
- **Testes/evidência:** CA-03 e CA-04; exemplos combinando as diferenças de escrita e as duas situações.
- **Riscos:** normalizações diferentes em cada operação; bloquear títulos iguais de artistas distintos; tratar situações diferentes como álbuns diferentes.

### BL-07 — Distinguir biblioteca vazia de falha de leitura

- [ ] Concluída
- **Objetivo:** abrir uma coleção nova sem colocar dados inacessíveis em risco.
- **Dependências:** BL-04.
- **Critérios de aceitação:** quando não houver registros, informar a ausência e permitir cadastrar; quando a leitura de uma coleção falhar, apresentar erro distinto e não sobrescrever os dados como se estivessem vazios. Nenhuma gravação pode partir da suposição de que a leitura malsucedida representa uma coleção vazia.
- **Testes/evidência:** CA-07 e CA-21; simular leitura indisponível ou dados ilegíveis e verificar que a coleção original permanece intacta após nova abertura.
- **Riscos:** usar uma lista vazia como resposta genérica a qualquer erro; causar perda de dados no próximo cadastro.

### BL-08 — Preservar a coleção em falha de cadastro

- [ ] Concluída
- **Objetivo:** tornar observável a diferença entre cadastro salvo e tentativa que falhou.
- **Dependências:** BL-04.
- **Critérios de aceitação:** se a gravação falhar, informar que o álbum não foi salvo; não confirmar sucesso nem deixar registro parcial; manter os registros previamente confirmados, inclusive ao reabrir.
- **Testes/evidência:** cadastro de CA-20, com falha controlada de gravação, inclusive condição equivalente a falta de espaço ou permissão conforme o armazenamento escolhido.
- **Riscos:** atualizar apenas a tela e aparentar persistência; perder outros registros ao regravar a coleção.

## 6. P1 — Consultar, escolher e corrigir

### BL-09 — Organizar e selecionar álbuns por artista

- [ ] Concluída
- **Objetivo:** reencontrar a coleção de um artista.
- **Dependências:** BL-06, BL-07.
- **Critérios de aceitação:** identificar os grupos por artista, títulos e situações; reunir nomes equivalentes pela normalização aprovada; selecionar um artista ou todos; tratar um nome composto, como `Artista A e Artista B`, como um agrupamento próprio, sem separar participantes.
- **Testes/evidência:** CA-05 e CA-06, mais nome composto e retirada da seleção; conferir que consultar não altera registros nem situações.
- **Riscos:** criar artistas distintos por diferenças de escrita; incluir álbuns de outro agrupamento; acrescentar um cadastro independente de artistas.

### BL-10 — Buscar por trecho do título

- [ ] Concluída
- **Objetivo:** localizar um álbum mesmo sem lembrar seu título completo.
- **Dependências:** BL-09.
- **Critérios de aceitação:** usar a normalização aprovada e correspondência parcial; aceitar busca de até 200 caracteres; rejeitar 201 sem aplicar a busca excedente ou truncar; apagar a busca ou informar só espaços retira apenas essa restrição; ausência de correspondências tem mensagem própria e preserva a coleção.
- **Testes/evidência:** CA-08, CA-09 e busca de CA-25; combinar busca com artista selecionado e verificar a preservação dessa seleção ao limpar o texto.
- **Riscos:** aplicar comparação diferente da usada nas duplicatas; perder outras seleções; confundir nenhum resultado com coleção vazia.

### BL-11 — Filtrar por situação de escuta

- [ ] Concluída
- **Objetivo:** escolher entre álbuns que quer ouvir, já ouviu ou ambos.
- **Dependências:** BL-09.
- **Critérios de aceitação:** permitir `quero ouvir`, `já ouvi` e todas; respeitar o artista selecionado; voltar a todas remove apenas a restrição de situação. Filtrar nunca altera a situação dos registros.
- **Testes/evidência:** CA-10 com e sem artista selecionado; incluir coleção formada somente por álbuns já ouvidos.
- **Riscos:** usar a situação como preferência implícita em vez de filtro; reiniciar seleções ao trocar de situação.

### BL-12 — Combinar artista, busca e situação

- [ ] Concluída
- **Objetivo:** fazer a consulta representar exatamente todas as restrições ativas.
- **Dependências:** BL-10, BL-11.
- **Critérios de aceitação:** usar interseção: o álbum precisa atender a cada restrição ativa; sem restrições, incluir toda a biblioteca; retirar uma restrição preserva as outras; diferenciar ausência de resultados de ausência de registros.
- **Testes/evidência:** CA-11 com os quatro álbuns especificados; combinações de zero, uma, duas e três restrições, incluindo limpeza isolada de cada uma.
- **Riscos:** combinar filtros por união; calcular consulta e futuros elegíveis do sorteio por regras diferentes.

### BL-13 — Sortear um álbum da consulta atual

- [ ] Concluída
- **Objetivo:** obter uma escolha aleatória coerente com o que está sendo consultado.
- **Dependências:** BL-12.
- **Critérios de aceitação:** retornar um único elegível com título, artista e situação; sem restrições, considerar toda a biblioteca; com um elegível, retornar esse álbum; sem elegíveis, informar a ausência sem apresentar resultado anterior como novo. Não alterar registros; permitir repetição; dar a cada elegível a mesma chance em sorteios independentes.
- **Testes/evidência:** CA-12 a CA-15; controlar a fonte de aleatoriedade nos testes para verificar os limites e o mapeamento para os elegíveis; revisar a regra de seleção para justificar chances iguais. Uma amostra pequena ou contagens exatamente iguais não servem como prova estatística.
- **Riscos:** sortear uma lista desatualizada; favorecer posições ou situações; excluir resultados anteriores sem autorização.

### BL-14 — Editar os dados de um álbum e persistir a alteração

- [ ] Concluída
- **Objetivo:** corrigir título, artista ou situação sem afetar os demais álbuns.
- **Dependências:** BL-06, BL-09.
- **Critérios de aceitação:** aplicar as validações e os limites do cadastro; verificar duplicatas ignorando o próprio registro; permitir salvar sem mudanças; atualizar somente o escolhido após a gravação; manter os dados anteriores se a entrada for inválida ou duplicar outro álbum; recuperar a edição após reabertura.
- **Testes/evidência:** CA-16, CA-18, edição de CA-19 e CA-25; editar cada campo separadamente, incluindo novo artista, e conferir os demais registros.
- **Riscos:** criar um segundo registro em vez de editar; considerar o próprio álbum duplicado; alterar outros álbuns do mesmo artista.

### BL-15 — Atualizar consulta e elegíveis após uma edição

- [ ] Concluída
- **Objetivo:** refletir imediatamente a mudança de título, artista ou situação na consulta e nos próximos sorteios.
- **Dependências:** BL-13, BL-14.
- **Critérios de aceitação:** remover dos resultados um álbum que deixou de atender aos filtros, preservando-o na coleção; atualizar agrupamento e correspondência de título; próximos sorteios usam os dados salvos atuais. Não manter um resultado antigo apresentado como um novo sorteio válido.
- **Testes/evidência:** CA-17 e RN-08; mudar situação, artista e título com restrições ativas; reencontrar o registro na consulta correspondente aos novos dados e verificar sua elegibilidade.
- **Riscos:** manter listas antigas para consulta ou sorteio; confundir saída do filtro com exclusão do álbum.

### BL-16 — Preservar os dados em falha de edição

- [ ] Concluída
- **Objetivo:** impedir que uma correção malsucedida substitua o último estado confirmado.
- **Dependências:** BL-08, BL-14.
- **Critérios de aceitação:** uma falha de gravação não confirma edição nem altera o álbum persistido ou os demais registros; informar que a operação não foi salva e recuperar os valores anteriores ao reabrir.
- **Testes/evidência:** edição de CA-20; provocar a falha depois de preencher uma alteração válida e conferir a coleção integral antes, depois e após reabertura.
- **Riscos:** manter a alteração apenas na interface como se tivesse sido salva; restaurar parte dos dados e perder outros registros.

## 7. P1 — Exportar e restaurar com preservação dos dados

### BL-17 — Exportar a coleção completa

- [ ] Concluída
- **Objetivo:** gerar uma cópia manual dos dados salvos, inclusive de uma biblioteca vazia.
- **Dependências:** BL-02, BL-07.
- **Critérios de aceitação:** gerar um arquivo no formato próprio com todos os títulos, artistas e situações salvos, mesmo com filtros ativos; disponibilizá-lo sem alterar a coleção; confirmar a exportação somente após a geração. Uma coleção vazia produz uma cópia válida, não uma falha.
- **Testes/evidência:** CA-26; comparar conteúdo e quantidade com a coleção salva, incluindo registros ocultos por filtros; verificar a cópia vazia conforme a seção 8 dos requisitos.
- **Riscos:** exportar somente resultados visíveis; omitir situação ou registros; afirmar que o usuário guardou o arquivo quando apenas a geração foi concluída.

### BL-18 — Comunicar falhas de exportação sem cópia parcial

- [ ] Concluída
- **Objetivo:** impedir que um arquivo incompleto pareça uma recuperação confiável.
- **Dependências:** BL-17.
- **Critérios de aceitação:** se a leitura completa ou a geração do arquivo falhar, informar que a cópia não foi concluída; não confirmar sucesso, não apresentar cópia parcial como completa e preservar a coleção.
- **Testes/evidência:** CA-27, simulando separadamente falha de leitura e de geração; verificar ausência de confirmação e integridade dos registros.
- **Riscos:** ignorar um erro em parte da coleção; emitir sucesso antes de terminar o arquivo.

### BL-19 — Validar todo o arquivo antes de permitir restauração

- [ ] Concluída
- **Objetivo:** distinguir uma cópia íntegra de um arquivo que deve ser rejeitado por completo.
- **Dependências:** BL-02, BL-06, BL-07.
- **Critérios de aceitação:** selecionar e ler o arquivo próprio; validar formato, todos os registros, campos, situações, limites e duplicatas internas conforme RN-07; aceitar coleção vazia válida; informar o motivo da rejeição sem gravar nada. Não comparar com a coleção atual para impedir duplicatas entre coleções, pois a operação futura será de substituição, não mesclagem.
- **Testes/evidência:** CA-30 com cada categoria de erro; colocar um registro inválido no fim de uma cópia com registros válidos e verificar que nenhum foi restaurado; testar duplicatas normalizadas com situações diferentes e mesmo título com artistas distintos.
- **Riscos:** validar só os primeiros registros; começar a gravar durante a leitura; rejeitar uma cópia válida por coincidência com dados atuais.

### BL-20 — Restaurar após confirmação ou cancelar sem mudanças

- [ ] Concluída
- **Objetivo:** recuperar exatamente a cópia escolhida, com uma decisão explícita antes de substituir os dados.
- **Dependências:** BL-08, BL-17, BL-19.
- **Critérios de aceitação:** só após validação completa, avisar que toda a coleção atual será substituída; exigir confirmação antes de gravar; cancelar preserva a coleção e não confirma restauração; confirmar uma cópia válida substitui integralmente os registros, sem mesclar, e só informa sucesso após salvar. A coleção restaurada deve reaparecer após reabertura. A mesma confirmação é obrigatória para uma cópia vazia.
- **Testes/evidência:** CA-28, CA-29 e restauração de CA-19; exportar uma coleção, modificar os dados e restaurar a cópia para conferir os mesmos títulos, artistas e situações; repetir com cópia vazia e com cancelamento.
- **Riscos:** confirmar de forma implícita; mesclar sem autorização; manter registros anteriores; considerar confirmação suficiente antes de concluir a gravação.

### BL-21 — Preservar a coleção inteira em falha de restauração

- [ ] Concluída
- **Objetivo:** garantir substituição integral ou preservação integral do último estado confirmado.
- **Dependências:** BL-20.
- **Critérios de aceitação:** uma falha de gravação após confirmar uma cópia válida informa que a restauração não foi salva; não confirma sucesso nem deixa a coleção parcialmente substituída; mantém todos os dados anteriores, inclusive após reabertura.
- **Testes/evidência:** CA-31 e restauração de CA-20; provocar falha nos pontos de gravação relevantes ao mecanismo escolhido, inclusive após o início da tentativa de substituição quando aplicável; comparar a coleção anterior inteira e reabrir a aplicação.
- **Riscos:** apagar a coleção atual antes de garantir a substituição; preservar somente alguns registros; aparentar recuperação na tela sem persistência íntegra.

## 8. P1 — Verificar o MVP no ambiente suportado

### BL-22 — Verificar texto seguro em todos os caminhos de entrada

- [ ] Concluída
- **Objetivo:** comprovar que dados da biblioteca não são executados como código.
- **Dependências:** BL-15, BL-18, BL-21.
- **Critérios de aceitação:** título, artista e busca permanecem texto no cadastro, consulta, edição e sorteio; texto vindo de restauração segue o mesmo tratamento; exportar e restaurar preserva os valores válidos sem executá-los. Corrigir eventuais pontos que escapem ao tratamento já adotado nas tarefas anteriores.
- **Testes/evidência:** CA-23 e RNF-04, com símbolos, acentos e exemplos como `<script>` nos caminhos aplicáveis; conferir agrupamentos, mensagens e exibição de dados restaurados.
- **Riscos:** tratar dados restaurados como confiáveis; montar conteúdo executável a partir de entradas; remover texto válido para encobrir o problema.

### BL-23 — Verificar teclado e mensagens nos fluxos da biblioteca

- [ ] Concluída
- **Objetivo:** concluir cadastro, consulta, filtros, sorteio e edição com comunicação compreensível e acesso por teclado.
- **Dependências:** BL-15, BL-16.
- **Critérios de aceitação:** percorrer e concluir os fluxos nos dois navegadores suportados; cancelar quando aplicável; manter foco visível, campos com rótulos e contraste legível; validação, sucesso, ausência de resultados e falhas usam texto em português, sem depender apenas de cor. Corrigir os problemas encontrados.
- **Testes/evidência:** parte correspondente de CA-33, CA-24 e RNF-02/RNF-05; roteiro manual só com teclado, registrando sistema, versões dos navegadores e resultados, incluindo estados de erro e limites.
- **Riscos:** verificar somente o caminho de sucesso; mensagens sem relação clara com o campo; foco perdido após atualização da consulta.

### BL-24 — Verificar teclado e mensagens na cópia e recuperação

- [ ] Concluída
- **Objetivo:** tornar exportação e restauração completas acessíveis também sem mouse.
- **Dependências:** BL-18, BL-21.
- **Critérios de aceitação:** selecionar arquivo, entender a validação e o aviso de substituição, confirmar ou cancelar e compreender sucesso ou falha por teclado; manter foco visível, rótulos, contraste e mensagens em português independentes de cor, nos dois navegadores. Corrigir os problemas encontrados.
- **Testes/evidência:** parte correspondente de CA-33 e RNF-02/RNF-05, cobrindo arquivo inválido, cancelamento, cópia vazia e falhas de exportação/restauração; registrar ambientes e resultados.
- **Riscos:** prender o foco na confirmação; tornar cancelamento inacessível; apresentar falhas apenas por cor ou mensagem técnica.

### BL-25 — Preparar dados reproduzíveis para verificar a capacidade

- [ ] Concluída
- **Objetivo:** dispor de uma coleção sintética válida para testar 10.000 álbuns sem usar dados pessoais.
- **Dependências:** BL-02, BL-06.
- **Critérios de aceitação:** preparar dados de teste reproduzíveis com diferentes artistas e situações, títulos válidos e sem duplicatas normalizadas; permitir começar com 9.999 e cadastrar o próximo para atingir 10.000; permitir conferir a coleção completa antes e depois das operações. A preparação pertence aos testes e não adiciona importação externa ao produto.
- **Testes/evidência:** verificar contagem, validade dos campos, diversidade e unicidade do par normalizado; documentar como preparar o ambiente e comparar os resultados sem sobrescrever uma coleção pessoal.
- **Riscos:** duplicatas ou dados inválidos ocultarem problemas de capacidade; executar a preparação sobre dados reais; criar uma funcionalidade extra de importação.

### BL-26 — Verificar as operações com 10.000 álbuns no Chrome

- [ ] Concluída
- **Objetivo:** comprovar a capacidade aprovada no Chrome estável do momento da verificação.
- **Dependências:** BL-16, BL-22, BL-23, BL-24, BL-25.
- **Critérios de aceitação:** cadastrar até atingir 10.000, consultar, buscar, combinar filtros, sortear, editar, reabrir, exportar e restaurar, atendendo aos critérios correspondentes; preservar dados e elegibilidade. Não criar rejeição automática acima de 10.000 nem inventar um tempo máximo de resposta como requisito.
- **Testes/evidência:** CA-32 no Chrome; registrar versão, sistema, roteiro, resultados e eventuais limitações; comparar os dados exportados e restaurados e conferir contagens e valores persistidos.
- **Riscos:** conferir apenas a quantidade na tela; não verificar integridade após restauração; supor que o resultado de outro navegador se aplica ao Chrome.

### BL-27 — Verificar as operações com 10.000 álbuns no Firefox

- [ ] Concluída
- **Objetivo:** comprovar a capacidade aprovada de forma independente no Firefox estável do momento da verificação.
- **Dependências:** BL-16, BL-22, BL-23, BL-24, BL-25.
- **Critérios de aceitação:** cumprir o mesmo conjunto de operações e condições de BL-26 no Firefox, incluindo cadastro até 10.000, reabertura e recuperação; não introduzir limite artificial de quantidade nem meta numérica de velocidade.
- **Testes/evidência:** CA-32 no Firefox; registrar versão, sistema, resultados e limitações; conferir dados completos e elegíveis, sem considerar o teste no Chrome como substituto.
- **Riscos:** diferenças de armazenamento, arquivos e foco entre navegadores; validar somente uma abertura superficial da aplicação.

### BL-28 — Consolidar as evidências técnicas e liberar a avaliação de uso

- [ ] Concluída
- **Objetivo:** verificar que o núcleo completo pode ser avaliado com dados reais sem confundir planejamento com comprovação.
- **Dependências:** BL-26, BL-27.
- **Critérios de aceitação:** relacionar CA-01 a CA-33 aos resultados reais; conferir RN-01 a RN-14 e RNF-01 a RNF-08, incluindo ausência de conta, autenticação, APIs de streaming e custos recorrentes obrigatórios; registrar limitações e pendências. Só iniciar a avaliação quando os critérios técnicos obrigatórios estiverem atendidos; não declarar o MVP concluído antes da avaliação de utilidade.
- **Testes/evidência:** revisão da matriz abaixo e das evidências das tarefas; CA-22 nos fluxos do MVP e conferência das dependências/custos escolhidos em BL-01. Registrar o que não foi verificado, sem afirmar ausência de bugs.
- **Riscos:** trocar evidência por checklist marcado sem execução; tratar capacidade ou testes funcionais como prova de utilidade; exigir publicação ou deploy sem requisito.

## 9. P1 — Avaliar a utilidade e encerrar o ciclo

### BL-29 — Reunir os 20 álbuns reais para avaliação

- [ ] Concluída
- **Objetivo:** preparar a amostra aprovada para observar o uso cotidiano.
- **Dependências:** nenhuma; pode ser antecipada enquanto as decisões técnicas são trabalhadas.
- **Critérios de aceitação:** o usuário escolhe 20 álbuns reais com diferentes artistas e situações e reúne título, artista e situação; a seleção não exige integração com streaming nem publicação dos dados.
- **Testes/evidência:** conferir os 20 exemplos e a variedade necessária aos quatro objetivos da seção 10 dos requisitos; não usar essa amostra para comprovar capacidade.
- **Riscos:** selecionar só um artista ou uma situação; confundir o tamanho da amostra com um limite da aplicação.

### BL-30 — Usar a biblioteca durante uma semana e registrar dificuldades

- [ ] Concluída
- **Objetivo:** observar se o MVP ajuda a reencontrar álbuns e decidir o que ouvir.
- **Dependências:** BL-28, BL-29.
- **Critérios de aceitação:** durante uma semana, usar os 20 álbuns para reencontrar por artista e trecho do título, consultar o que quer ouvir, sortear dentro do conjunto desejado e mudar situação com reabertura posterior; registrar dificuldades, exemplos concretos e situações em que precisou voltar à organização anterior. Usar registros breves ao longo da semana, sem impor uma quantidade diária de ações.
- **Testes/evidência:** relato do uso real, com período e exemplos, conforme a seção 10; separar dificuldades de uso de falhas técnicas. A semana é o período aprovado de observação, não uma estimativa de desenvolvimento.
- **Riscos:** substituir observação por impressão genérica; interpretar poucas ocorrências do sorteio como teste de igualdade de chances; ampliar escopo durante a avaliação.

### BL-31 — Revisar o resultado e decidir o próximo ciclo

- [ ] Concluída
- **Objetivo:** encerrar o MVP com uma conclusão sustentada e uma próxima decisão do usuário.
- **Dependências:** BL-30.
- **Critérios de aceitação:** consolidar evidências técnicas e avaliação de utilidade; registrar se a biblioteca ajudou nos dois problemas, o que dificultou o uso e quais pendências existem; só considerar implementado se a definição de pronto de `REQUIREMENTS.md` estiver atendida. Pendências obrigatórias voltam para a tarefa correspondente; melhorias propostas precisam ser escolhidas antes de implementar.
- **Testes/evidência:** revisão da definição de pronto da seção 10 e dos registros de BL-28/BL-30; nenhuma conclusão de utilidade deve ser inventada caso o relato seja negativo ou inconclusivo.
- **Riscos:** declarar conclusão com critério obrigatório pendente; transformar uma sugestão em autorização para nova funcionalidade.

## 10. P2 — Refinamentos depois do MVP

### AD-01 — Refinar a inclusão de gênero

- [ ] Concluída
- **Objetivo:** especificar uma melhoria já prevista para depois do MVP, caso o usuário a priorize após observar o uso.
- **Dependências:** BL-31 e escolha explícita dessa próxima etapa pelo usuário.
- **Critérios de aceitação:** registrar os casos de uso, regras de preenchimento e consulta que o usuário confirmar; definir exemplos e o efeito nos dados existentes e nas cópias antes de criar tarefas de implementação. Não presumir taxonomia, múltiplos gêneros ou novo filtro sem decisão.
- **Testes/evidência:** revisão documental com exemplos aceitos, rejeitados e álbuns anteriores à melhoria. Os testes da funcionalidade só poderão ser definidos após esse refinamento.
- **Riscos:** complicar o cadastro sem benefício observado; inventar regras ainda não aprovadas.

### AD-02 — Refinar ano/década de lançamento

- [ ] Concluída
- **Objetivo:** especificar como época ajudaria a reencontrar ou escolher álbuns, se o usuário priorizar essa melhoria.
- **Dependências:** BL-31 e escolha explícita dessa próxima etapa pelo usuário; independente de AD-01.
- **Critérios de aceitação:** decidir com o usuário quais dados de época informar, quais consultas serão úteis e como tratar dados desconhecidos e registros antigos; avaliar efeito nas cópias e definir critérios antes de planejar implementação. Não escolher automaticamente entre ano, década ou ambos.
- **Testes/evidência:** revisão documental com exemplos confirmados e casos de borda; os testes de implementação dependem dessas regras futuras.
- **Riscos:** criar precisão desnecessária; presumir ano de uma edição quando o MVP não distingue edições.

## 11. Marcos, dependências e oportunidades de independência

| Marco | Itens concluídos | Resultado observável |
| --- | --- | --- |
| M0 — Base decidida | BL-01 a BL-03 | Decisões mínimas e execução local verificáveis. |
| M1 — Cadastro protegido | M0 e BL-04 a BL-08 | Cadastro válido persiste; entradas inválidas, duplicatas e falhas não aparentam sucesso nem apagam dados. |
| M2 — Biblioteca consultável | M1 e BL-09 a BL-16 | Consulta combinada, sorteio e edição coerentes com os dados salvos. |
| M3 — Cópia e recuperação | M1 e BL-17 a BL-21 | Exportação integral e restauração validada e confirmada, com preservação em cancelamento ou falha. |
| M4 — Verificação técnica | M2, M3 e BL-22 a BL-28 | Evidências dos critérios técnicos, capacidade e acessibilidade nos dois navegadores; pronto para avaliar uso. |
| M5 — Avaliação concluída | M4 e BL-29 a BL-31 | Uma semana de uso registrada e decisão sobre conclusão ou pendências do MVP. |

O caminho de dependências começa em BL-01 → BL-03 → BL-04. BL-02 pode avançar após BL-01 sem aguardar a preparação local. Depois das bases:

- BL-05, BL-07 e BL-08 podem ser tratadas separadamente após BL-04.
- BL-10 e BL-11 são independentes entre si; BL-12 faz a combinação completa.
- BL-14 pode começar antes do sorteio; BL-15 depende dos dois fluxos.
- BL-17 e BL-19 podem avançar separadamente quando suas dependências estiverem prontas; BL-20 integra o ciclo de exportar e restaurar.
- M3 não depende de concluir M2 e pode ser antecipado para reduzir o risco de recuperação.
- BL-23 e BL-24 verificam grupos distintos de fluxos; BL-26 e BL-27 verificam navegadores distintos, sem dependência entre si.
- BL-29 pode começar imediatamente, mas a avaliação de uso depende de M4.

As dependências não implicam tecnologia, separação em serviços ou arquitetura específica. Uma tarefa com muitos caminhos de erro pode ser executada em exemplos de teste sucessivos, mantendo o mesmo objetivo e sem iniciar o próximo item automaticamente.

## 12. Rastreabilidade dos requisitos

Rastreabilidade é a ligação entre um requisito e a tarefa que o entrega ou verifica. A tabela é um mapa de trabalho futuro; não comprova atendimento.

| Requisito | Tarefas principais | Critérios de aceitação de referência |
| --- | --- | --- |
| RF-01 — Cadastro | BL-04 a BL-08 | CA-01 a CA-04, CA-20, CA-24, CA-25 |
| RF-02 — Artista | BL-07, BL-09 | CA-05 a CA-07 |
| RF-03 — Busca | BL-10, BL-12 | CA-08, CA-09, CA-11, CA-25 |
| RF-04 — Situação | BL-11, BL-12 | CA-10, CA-11 |
| RF-05 — Sorteio | BL-13, BL-15 | CA-12 a CA-15, CA-17 |
| RF-06 — Edição | BL-14 a BL-16 | CA-16 a CA-18, CA-20, CA-25 |
| RF-07 — Reabertura | BL-04, BL-07, BL-08, BL-14, BL-16, BL-20, BL-21 | CA-19 a CA-21, CA-28, CA-31 |
| RF-08 — Exportação | BL-02, BL-17, BL-18 | CA-26, CA-27; cópia vazia da seção 8 |
| RF-09 — Restauração | BL-02, BL-19 a BL-21 | CA-28 a CA-31; cópia vazia da seção 8 |
| RN-01, RN-07, RN-08, RN-11 — Validação e identidade | BL-05, BL-06, BL-10, BL-14, BL-15, BL-19 | CA-02 a CA-04, CA-16 a CA-18, CA-25, CA-30 |
| RN-02 a RN-06 — Situação, filtros e sorteio | BL-09 a BL-15 | CA-05, CA-06, CA-08 a CA-18 |
| RN-09, RN-10 — Preservação e leitura | BL-01, BL-04, BL-07, BL-08, BL-14, BL-16, BL-20, BL-21 | CA-01, CA-16, CA-19 a CA-21, CA-28, CA-31 |
| RN-12 a RN-14 — Cópia e recuperação | BL-02, BL-17 a BL-21 | CA-26 a CA-31 |
| RNF-01 — Persistência e recuperação | BL-01, BL-04, BL-07, BL-08, BL-14, BL-16 a BL-21 | CA-19 a CA-21, CA-26 a CA-31 |
| RNF-02, RNF-05 — Comunicação e idioma | BL-05, BL-07, BL-08, BL-10 a BL-13, BL-16, BL-18 a BL-24 | CA-02, CA-07, CA-09, CA-14, CA-18, CA-20, CA-21, CA-24, CA-25, CA-27 a CA-31, CA-33 |
| RNF-03, RNF-08 — Independência e custo | BL-01, BL-03, BL-28 | CA-22 e restrições das seções 2 e 6 |
| RNF-04 — Conteúdo como texto | Todas as entradas e exibições; revisão em BL-22 | CA-23 |
| RNF-06 — Capacidade | BL-01, BL-25 a BL-27 | CA-32 |
| RNF-07 — Acessibilidade | Todas as interfaces; revisão em BL-23, BL-24 | CA-33 |
| Avaliação de utilidade — Seção 10 | BL-29 a BL-31 | 20 álbuns reais, uma semana e exemplos de uso registrados |

## 13. Próxima ação e revisão ativa

**Próxima microtarefa recomendada: BL-04.** Com as decisões BL-01/BL-02 e a execução inicial da BL-03 verificadas, o próximo passo recomendado é cadastrar um álbum válido e recuperá-lo ao reabrir. As páginas introdutórias não comprovam os fluxos da coleção.

**Decisão que cabe ao usuário:** escolher iniciar BL-04 ou outro item já desbloqueado. A conclusão da BL-03 não inicia automaticamente outra tarefa nem autoriza mudanças adicionais no Git.

**Revisão ativa:** por que uma resposta HTTP 200 e dois testes `SimpleTestCase` passando ainda não demonstram que um álbum foi salvo e pode ser recuperado ao reabrir?
