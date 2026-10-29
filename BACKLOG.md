# Music Library — backlog priorizado

Data: 29/10/2026. Fonte de verdade: [REQUIREMENTS.md](REQUIREMENTS.md).

**Decisão confirmada pelo autor: este será um projeto novo.** A comparação com o projeto anterior e a escolha entre evolução e nova versão estão resolvidas e não são tarefas pendentes. Essa decisão atualiza a premissa de planejamento, sem alterar os documentos de origem.

Este backlog organiza o trabalho; as escolhas técnicas confirmadas na B01 estão registradas em [DECISOES.md](DECISOES.md). O registro não autoriza implementar funcionalidades, instalar ferramentas ou publicar a aplicação. As **B01 e B02 estão concluídas** e as outras **29 tarefas estão pendentes**. O teste mínimo de infraestrutura foi executado na B02; os testes de produto descritos permanecem **planejados**.

## 1. Prioridades, dependências e forma de trabalho

- **P0 — preparação:** decidir tecnologias, interface e ambiente local; preparar o mínimo necessário para começar.
- **P1 — cadastro e navegação:** construir a primeira entrega intermediária com artistas e álbuns persistidos.
- **P2 — exploração e audição:** acrescentar busca, filtros, sorteio, audição e avaliação.
- **P3 — conclusão do MVP:** acrescentar links e exclusões e consolidar as evidências de aceitação.

P0 a P3 indicam sequência sugerida, não itens dispensáveis: todas as tarefas de produto listadas compõem o MVP. Uma prioridade menor não adia validação, persistência, integridade ou concorrência aplicáveis à tarefa atual.

As dependências indicam pré-requisitos de conclusão. Dentro de cada bloco, seguir a ordem sugerida; entre blocos independentes, o autor pode escolher a próxima tarefa respeitando os pré-requisitos. Após B09, exploração (B13–B17), audição (B18–B22) e links (B23–B25) podem avançar independentemente, após suas respectivas dependências. Isso permite escolhas de sequência; não exige execução simultânea ou múltiplos agentes.

Executar uma tarefa por vez com mentoria: o autor escreve testes e implementação, preferindo TDD — teste que falha, implementação mínima e melhoria da organização. Apresentar evidências e aguardar a decisão do autor antes da próxima tarefa. Se uma tarefa não couber em um ciclo curto de trabalho, subdividi-la preservando seus critérios e referências; não retirar testes para reduzir tamanho.

Disponibilidade de referência: 10 horas semanais, sem prazo definido. Não há estimativas de calendário aprovadas. O fluxo principal continua sendo **Biblioteca → Artista → Álbuns agrupados por tipo → Detalhes do álbum**. A interface escolhida na B01 usa navegador local, templates Django, HTML e CSS simples, conforme [DECISOES.md](DECISOES.md).

### Critérios comuns de conclusão

Aplicar a cada tarefa de produto, além de seus critérios específicos:

- Demonstrar os cenários correspondentes aos requisitos, com testes adequados e evidências registradas; tornar entradas e resultados observáveis para teste (RNF-05).
- Em operações que alteram dados, verificar persistência após encerramento e reinício normal, inclusive remoções (RNF-01, CA-14).
- Em validações e falhas, identificar o problema, permitir correção e não anunciar sucesso; preservar o estado anterior em vez de salvar parcialmente (RNF-02, RNF-03, CA-15).
- Preservar campos e vínculos não alterados; não criar álbuns sem artista nem avaliações ou links sem álbum (RNF-03).
- Onde houver unicidade, protegê-la também nas solicitações simultâneas pertinentes (RNF-04, CA-16).
- Ao acrescentar avaliação e links, ampliar os testes de edição e transferência de álbum para verificar preservação desses novos dados. Ao acrescentar álbuns, verificar que renomear o artista preserva seus vínculos.
- Manter limitações explícitas e critérios pendentes como pendentes. Os critérios comuns não transferem o trabalho de qualidade para as tarefas finais.

## 2. Preparação — P0

### B01 — Escolher tecnologias, interface e ambiente local

- **Estado / prioridade:** Concluída em 29/10/2026 / P0.
- **Objetivo:** definir o mínimo técnico necessário para começar um projeto novo.
- **Dependências:** nenhuma.
- **Aceitação:** registrar linguagem, ferramentas de execução e testes, persistência, interface inicial e estrutura mínima, com justificativas compatíveis com aprendizado de backend e uso por uma pessoa. Explicar como executar localmente e como verificar os comportamentos dos requisitos. Não exigir interface gráfica, API pública ou hospedagem.
- **Verificação planejada:** revisar se as escolhas suportam persistência, operações integrais, unicidade concorrente e testes controláveis de falhas e sorteio; obter a decisão do autor, sem instalar nada nesta tarefa.
- **Evidência de conclusão:** escolhas confirmadas pelo autor e registradas em [DECISOES.md](DECISOES.md), incluindo justificativas, estrutura mínima, execução local prevista, estratégias de verificação e limitações do SQLite. Revisão documental realizada, sem instalações ou execução de testes de produto; preparação e comprovação do ambiente permanecem na B02.
- **Risco principal:** adotar complexidade sem benefício para o MVP.
- **Referências:** seção 8 dos requisitos; RNF-01, RNF-03, RNF-04, RNF-05.

### B02 — Preparar ambiente mínimo de desenvolvimento

- **Estado / prioridade:** Concluída em 29/10/2026 / P0.
- **Objetivo:** permitir iniciar a aplicação e executar verificações localmente.
- **Dependências:** B01.
- **Aceitação:** após as aprovações específicas necessárias para instalações e alterações, preparar somente o ambiente escolhido e registrar os passos de execução. Configuração de Git, se proposta, exige autorização própria; não é pré-requisito documental deste backlog.
- **Verificação planejada:** iniciar e encerrar a aplicação e executar um teste mínimo de funcionamento da infraestrutura de testes, com resultados registrados e sem serviços de produção.
- **Evidência de conclusão:** ambiente virtual `venv/`, Python 3.12.3, SQLite 3.45.1 e Django 5.2.18; dependências fixadas em `requirements.txt`; projeto `config/` e app `library/` registrado. O agente executou `manage.py check` sem problemas identificados e `manage.py test` com 1 teste aprovado em banco separado em memória. O autor forneceu a saída do servidor local iniciado com `runserver 127.0.0.1:8000 --noreload` (com a opção Python `-B`), resposta HTTP 200 para `GET /` e encerramento com `Ctrl+C`; em seguida, forneceu a saída de `manage.py migrate` com as 18 migrações internas aplicadas com sucesso. Passos e limites registrados em [DECISOES.md](DECISOES.md#5-evidências-e-limites-das-etapas).
- **Risco principal:** ambiente não reproduzível ou preparação maior que a primeira entrega.
- **Referências:** seção 8 dos requisitos; RNF-05.

## 3. Cadastro e navegação — P1

### B03 — Cadastrar artista

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** salvar um artista manualmente, mesmo sem álbuns.
- **Dependências:** B02.
- **Aceitação:** aceitar nome válido; permitir consultar o artista criado; rejeitar nome ausente, vazio ou somente espaços com explicação e sem alteração de registros. Persistir o cadastro.
- **Testes planejados:** cadastro válido e consulta sem álbuns; entradas inválidas; reinício; falha de gravação sem sucesso falso. A listagem completa é B05 e o bloqueio de duplicatas é B04; esta fatia isolada ainda não conclui RF-01.
- **Risco principal:** aceitar dados inválidos ou apresentar cadastro que não foi salvo.
- **Referências:** RF-01; RN-04; RNF-01, RNF-02, RNF-03; CA-01, CA-14, CA-15.

### B04 — Bloquear artistas duplicados

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** preservar a identificação única dos artistas.
- **Dependências:** B03.
- **Aceitação:** comparar nomes desconsiderando capitalização, espaços nas extremidades e sequências de espaços; não remover acentos ou pontuação nem unificar nomes parecidos. Não representar homônimos distintos neste MVP. Rejeitar duplicata sem alterar o registro existente.
- **Testes planejados:** `Iron Maiden` versus ` iron   maiden `; nomes distintos por acentos ou pontuação; duas criações simultâneas equivalentes produzem no máximo um registro e informam conflito na outra solicitação.
- **Risco principal:** duplicatas sob concorrência ou unificação indevida de nomes.
- **Referências:** RF-01; RN-01, RN-02; RNF-02, RNF-04; CA-03, CA-16.

### B05 — Listar e acessar artistas

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** abrir a biblioteca e acessar um artista cadastrado.
- **Dependências:** B04.
- **Aceitação:** ordenar artistas alfabeticamente sem distinguir capitalização; informar biblioteca vazia e artista sem álbuns; mostrar somente registros cadastrados.
- **Testes planejados:** biblioteca vazia, vários nomes com capitalizações diferentes, acesso a artista sem álbuns e ausência de registros externos à biblioteca.
- **Risco principal:** navegação incoerente ou expectativa de discografia importada.
- **Referências:** RF-03; RN-07, RN-11; CA-04.

### B06 — Editar nome do artista

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** corrigir o nome preservando a identidade e os vínculos do artista.
- **Dependências:** B04.
- **Aceitação:** renomear para nome válido e único; rejeitar vazio e duplicata, incluindo conflitos simultâneos; preservar vínculos com álbuns quando disponíveis e manter dados anteriores em falha.
- **Testes planejados:** edição válida e persistência; manter o próprio nome sem falso conflito; vazio e duplicata; duas edições que convergem para nome equivalente; preservação dos vínculos ampliada em B07 e B09.
- **Risco principal:** romper vínculos ou violar unicidade na edição.
- **Referências:** RF-01; RN-01, RN-02, RN-04, RN-05; RNF-01, RNF-02, RNF-03, RNF-04; CA-01, CA-03, CA-14, CA-15, CA-16.

### B07 — Cadastrar álbum com dados obrigatórios

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** registrar um lançamento associado a exatamente um artista existente.
- **Dependências:** B04.
- **Aceitação:** exigir título não vazio, artista existente, ano inteiro entre 1 e 9999 e um tipo entre Estúdio, Ao vivo, Coletânea, EP e Outros. Aceitar anos futuros. Salvar como não ouvido, sem gêneros, links ou avaliação, e permitir consultar o vínculo com o artista.
- **Testes planejados:** cadastro mínimo e reinício; campos ausentes ou com espaços; artista inexistente; limites 1 e 9999; ano futuro, fracionado e fora da faixa; tipo desconhecido; falha sem álbum parcial. Se B06 já estiver concluída, verificar também renomeação do artista com álbum vinculado.
- **Risco principal:** álbum inválido ou sem artista.
- **Referências:** RF-02; RN-04, RN-05, RN-12; RNF-01, RNF-02, RNF-03; CA-02, CA-14, CA-15.

### B08 — Bloquear álbuns duplicados

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** proteger a combinação título equivalente, artista e ano.
- **Dependências:** B07.
- **Aceitação:** aplicar RN-01 ao título; rejeitar a mesma combinação; permitir mesmo título em outro artista ou ano. Não diferenciar edições com a mesma combinação.
- **Testes planejados:** duplicata com variações de capitalização e espaços; títulos com acentos ou pontuação distintos; outro artista e outro ano; duas criações simultâneas equivalentes geram no máximo um registro com conflito informado.
- **Risco principal:** duplicidade concorrente ou bloqueio de lançamento permitido.
- **Referências:** RF-02; RN-01, RN-03; RNF-02, RNF-04; CA-03, CA-16.

### B09 — Navegar pelos álbuns e seus detalhes

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** completar o fluxo da biblioteca até os detalhes do álbum.
- **Dependências:** B05, B08.
- **Aceitação:** mostrar somente álbuns cadastrados do artista, agrupados pelos cinco tipos permitidos; ordenar títulos alfabeticamente sem distinguir capitalização e desempatar por ano crescente; permitir acessar os detalhes. Não oferecer ordenação personalizada.
- **Testes planejados:** artista vazio, tipos diferentes, títulos com diferentes capitalizações, títulos equivalentes em anos distintos e detalhes correspondentes ao álbum escolhido. Se B06 estiver concluída, verificar preservação dos vínculos e navegação após renomear artista.
- **Risco principal:** listar álbuns de outro artista ou detalhes do registro errado.
- **Referências:** RF-03; RN-05, RN-07, RN-11; CA-03, CA-04.

### B10 — Editar título, ano e tipo do álbum

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** corrigir dados do álbum sem perder informações não alteradas.
- **Dependências:** B09.
- **Aceitação:** refletir alterações válidas nos detalhes, ordem e agrupamento; manter o próprio cadastro sem falso conflito; rejeitar dados inválidos e duplicatas, inclusive em edições simultâneas. Preservar demais campos.
- **Testes planejados:** mudança de título, ano e tipo; valores inválidos; conflito com outro álbum; edições simultâneas que convergem para a mesma combinação; falha preservando dados anteriores; reinício. Ampliar preservação quando gêneros, audição, avaliação e links forem adicionados.
- **Risco principal:** apagar dados não editados ou violar unicidade.
- **Referências:** RF-02; RN-01, RN-03, RN-04, RN-11; RNF-01, RNF-02, RNF-03, RNF-04; CA-02, CA-03, CA-14, CA-15, CA-16.

### B11 — Transferir álbum para outro artista

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** corrigir o artista de um álbum existente.
- **Dependências:** B10.
- **Aceitação:** exigir destino existente e ausência de duplicata; atualizar os vínculos e as listagens dos dois artistas integralmente; preservar dados não alterados.
- **Testes planejados:** transferência válida e reinício; destino inexistente; conflito de título/artista/ano no destino; transferências simultâneas que produziriam duplicata; falha preservando origem e destino. Ampliar preservação para avaliação e links quando disponíveis.
- **Risco principal:** álbum sem artista, vínculo duplicado ou perda de dados.
- **Referências:** RF-02; RN-03, RN-05; RNF-01, RNF-02, RNF-03, RNF-04; CA-02, CA-03, CA-14, CA-15, CA-16.

### B12 — Informar e editar gêneros do álbum

- **Estado / prioridade:** Pendente / P1.
- **Objetivo:** classificar o álbum manualmente com zero ou mais gêneros.
- **Dependências:** B10.
- **Aceitação:** permitir informar gêneros no cadastro e na edição; rejeitar rótulo vazio ou somente espaços; impedir gêneros equivalentes repetidos no mesmo álbum conforme RN-01. Não exigir taxonomia externa. Preservar demais campos e gêneros de outros álbuns.
- **Testes planejados:** zero, um e vários gêneros; equivalentes com espaços e capitalização distintos; acentos e pontuação preservados; rótulo inválido sem gravação parcial; remoção de gênero e reinício.
- **Risco principal:** repetição de gêneros ou alteração de outros álbuns.
- **Referências:** RF-02; RN-01, RN-06; RNF-01, RNF-02, RNF-03; CA-02, CA-14, CA-15.

**Marco 1 — cadastro e navegação:** B01–B12 concluídas. Cadastrar, navegar, editar e transferir artistas e álbuns com gêneros, preservando os dados entre reinícios. É uma entrega intermediária; ainda não representa o MVP completo.

## 4. Exploração da coleção — P2

### B13 — Buscar artistas pelo nome

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** encontrar artistas cadastrados por um trecho do nome.
- **Dependências:** B05.
- **Aceitação:** busca parcial sem distinguir capitalização; busca vazia não restringe; informar ausência de resultados; limpar recupera a listagem ordenada.
- **Testes planejados:** `MAID` encontra `Iron Maiden`; trecho sem correspondência; busca vazia; limpeza sem alterar cadastros.
- **Risco principal:** ocultar registros válidos ou aplicar regras de duplicata indevidamente à busca.
- **Referências:** RF-04; RN-08, RN-11; CA-05.

### B14 — Buscar álbuns pelo título

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** encontrar álbuns por trecho do título na coleção ou no artista atual.
- **Dependências:** B09.
- **Aceitação:** busca parcial sem distinguir capitalização; informar ausência de resultados; busca vazia não restringe; limpar preserva o contexto do artista, quando houver, e a ordenação padrão.
- **Testes planejados:** título em outra capitalização, resultados globais e limitados ao artista, busca sem correspondência, vazio e limpeza.
- **Risco principal:** incluir álbuns de outro artista no contexto atual.
- **Referências:** RF-04; RN-08, RN-10, RN-11; CA-05.

### B15 — Filtrar álbuns por gênero

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** restringir a seleção a um gênero escolhido.
- **Dependências:** B12, B14.
- **Aceitação:** gênero opcional corresponde a um dos gêneros do álbum; combinar com busca e artista atual; mostrar cada álbum uma vez; não ocultar artistas da biblioteca geral; tratar seleção vazia e remoção do filtro.
- **Testes planejados:** álbum com Heavy Metal e Hard Rock encontrado uma vez pelo gênero escolhido; outro gênero não corresponde; interseção com busca; contexto do artista; limpar sem alterar cadastros.
- **Risco principal:** multiplicar resultados por quantidade de gêneros.
- **Referências:** RF-05; RN-09, RN-10; CA-06.

### B16 — Filtrar por ano e combinar critérios

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** combinar busca, um gênero e um ano exato na seleção de álbuns.
- **Dependências:** B15.
- **Aceitação:** filtros opcionais; todos os critérios ativos devem ser atendidos, além do artista atual quando houver; seleção vazia é informada; limpar busca e filtros preserva somente o contexto do artista, sem modificar cadastros.
- **Testes planejados:** cada critério isolado e combinado; Heavy Metal em 1982; álbum que falha em apenas um critério é excluído; resultados únicos; limpeza e ausência de correspondência.
- **Risco principal:** usar união em vez de interseção ou perder o contexto.
- **Referências:** RF-05; RN-09, RN-10; CA-06.

### B17 — Sortear um álbum da seleção atual

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** ajudar a escolher um álbum entre os resultados atuais.
- **Dependências:** B16.
- **Aceitação:** respeitar busca, gênero, ano e artista; cada álbum participa uma vez com igual probabilidade, independentemente dos gêneros, audição ou avaliação; permitir repetições. Com zero candidatos, avisar sem retornar álbum externo; com um, retornar sempre esse álbum. Não alterar audição ou avaliação.
- **Testes planejados:** seleção com zero, um e vários candidatos; combinações de filtros e contexto; controlar a fonte aleatória para verificar seleção uniforme entre candidatos únicos, sem exigir frequências exatamente iguais em amostra finita. Ao concluir B18–B22, ampliar cenários para estados e avaliações diferentes e comprovar preservação desses dados.
- **Risco principal:** sorteio enviesado ou fora da seleção atual.
- **Referências:** RF-08; RN-09, RN-10, RN-14, RN-15; RNF-05; CA-10.

## 5. Audição e avaliação — P2

### B18 — Marcar e desmarcar audição sem avaliação

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** registrar o estado atual ouvido/não ouvido, sem histórico.
- **Dependências:** B09.
- **Aceitação:** marcar ouvido não exige avaliação; desmarcar sem avaliação é direto; repetir a ação mantém o estado sem criar histórico; persistir o resultado.
- **Testes planejados:** transições nos dois sentidos; repetir cada estado solicitado; álbum ouvido sem nota ou comentário; reinício e falha sem alteração parcial. Preservar a confirmação de B22 quando avaliação passar a existir.
- **Risco principal:** criar efeitos adicionais ao repetir uma ação.
- **Referências:** RF-06; RN-12, RN-13; RNF-01, RNF-03; CA-07, CA-14, CA-15.

### B19 — Registrar e editar nota opcional

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** avaliar um álbum ouvido com uma nota opcional.
- **Dependências:** B18.
- **Aceitação:** aceitar somente em álbum ouvido; permitir escala de 0 a 5 em passos de 0,5; distinguir ausência de zero; criar ou atualizar a avaliação única, preservando campos não alterados. Ampliar testes de edição e transferência de álbum para preservar audição e nota.
- **Testes planejados:** todos os valores da escala, incluindo 0, 0,5 e 5; rejeitar -0,5, 5,5, 3,2 e não numérico; impedir nota em não ouvido com mensagem útil; editar sem criar segunda avaliação; reinício e falha.
- **Risco principal:** confundir zero com ausência ou avaliar álbum não ouvido.
- **Referências:** RF-07; RN-12; RNF-01, RNF-02, RNF-03, RNF-05; CA-02, CA-08, CA-14, CA-15.

### B20 — Registrar e editar comentário opcional

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** permitir avaliação com só comentário, só nota ou ambos.
- **Dependências:** B19.
- **Aceitação:** exigir álbum ouvido; comentário vazio ou somente espaços equivale a ausente; atualizar avaliação existente e preservar nota não alterada. Ampliar testes de edição e transferência do álbum para preservar comentário.
- **Testes planejados:** comentário isolado, junto da nota, edição preservando nota zero, remoção por texto vazio ou espaços, rejeição em não ouvido, persistência e falha. Se B17 estiver concluída, testar sorteio sem alterar avaliação nem favorecer álbuns por nota ou audição.
- **Risco principal:** apagar nota ao editar comentário ou criar avaliação duplicada.
- **Referências:** RF-07; RN-12, RN-14; RNF-01, RNF-02, RNF-03, RNF-05; CA-02, CA-08, CA-10, CA-14, CA-15.

### B21 — Remover avaliação sem mudar audição

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** retirar nota e comentário, juntos ou separadamente.
- **Dependências:** B20.
- **Aceitação:** remover só um campo preserva o outro; ausência de ambos significa sem avaliação; álbum continua ouvido e sem segunda avaliação; ausência de nota nunca aparece como zero.
- **Testes planejados:** remover nota mantendo comentário; remover comentário mantendo nota zero; remover ambos; reinício e falha preservando o estado anterior.
- **Risco principal:** remover mais dados que o solicitado ou alterar audição.
- **Referências:** RF-07; RN-12; RNF-01, RNF-03; CA-08, CA-14, CA-15.

### B22 — Desmarcar álbum avaliado com confirmação

- **Estado / prioridade:** Pendente / P2.
- **Objetivo:** mudar para não ouvido com remoção consciente e integral da avaliação.
- **Dependências:** B21.
- **Aceitação:** avisar que nota e comentário serão apagados; cancelar preserva tudo; confirmar muda estado e remove ambos integralmente. Sem avaliação, manter a mudança direta de B18.
- **Testes planejados:** só nota, só comentário e ambos; cancelamento; confirmação; nota zero também exige confirmação; falha entre as mudanças preserva todo o estado anterior; reinício.
- **Risco principal:** perda de avaliação sem confirmação ou operação parcial.
- **Referências:** RF-06, RF-07; RN-13; RNF-01, RNF-02, RNF-03; CA-07, CA-09, CA-14, CA-15.

**Marco 2 — exploração e registro de audição:** Marco 1 e B13–B22 concluídos. Buscar, filtrar, sortear e registrar audições e avaliações, incluindo os testes cruzados de preservação na edição e no sorteio.

## 6. Links e exclusões — P3

### B23 — Cadastrar e consultar links

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** guardar links de serviços de streaming no álbum.
- **Dependências:** B09.
- **Aceitação:** exigir nome de serviço não vazio e URL absoluta HTTP/HTTPS com domínio ou host; permitir serviços distintos; bloquear serviço equivalente conforme RN-01 no mesmo álbum, mas permitir em outro álbum. Não depender da disponibilidade do destino. Ampliar testes de edição e transferência do álbum para preservar links quando essas operações estiverem disponíveis.
- **Testes planejados:** HTTP e HTTPS válidos; nome vazio ou espaços; URL relativa, sem host ou com outro esquema; `Spotify` versus ` spotify `; serviços diferentes; destino indisponível não impede consultar cadastro; reinício e falha de gravação.
- **Risco principal:** aceitar URL inválida ou duplicar serviço.
- **Referências:** RF-09; RN-01, RN-16; RNF-01, RNF-02, RNF-03; CA-02, CA-11, CA-14, CA-15.

### B24 — Editar e remover links

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** corrigir serviço e endereço ou retirar um link.
- **Dependências:** B23.
- **Aceitação:** aplicar as validações também na edição; rejeitar conflito com outro serviço do álbum; remover somente o link escolhido; preservar álbum e demais links; persistir alterações.
- **Testes planejados:** editar serviço e URL; manter o próprio serviço sem falso conflito; URL inválida e serviço duplicado preservam dados anteriores; remover um entre vários; reinício e falhas ao salvar ou remover.
- **Risco principal:** alterar outro link ou salvar edição inválida.
- **Referências:** RF-09; RN-01, RN-16; RNF-01, RNF-02, RNF-03; CA-11, CA-14, CA-15.

### B25 — Abrir link de streaming

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** permitir acessar o endereço cadastrado no serviço externo.
- **Dependências:** B23.
- **Aceitação:** disponibilizar abertura externa pela interface escolhida; não implementar reprodução interna; destino indisponível não remove cadastro nem impede consultar álbum; não prometer disponibilidade ou conteúdo do serviço.
- **Testes planejados:** verificar o endereço exato encaminhado à abertura externa com um substituto de teste; demonstrar a ação pela interface local de forma controlada, sem depender da disponibilidade real de um provedor.
- **Risco principal:** consulta depender de resposta do serviço externo.
- **Referências:** RF-09; RN-16; CA-11.

### B26 — Excluir álbum mediante confirmação

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** remover um álbum e seus dependentes com impacto explícito.
- **Dependências:** B22, B24.
- **Aceitação:** avisar remoção da avaliação e dos links; cancelar preserva tudo; confirmar remove álbum e dependentes integralmente; preservar artista, outros álbuns e gêneros associados a outros álbuns. Sem restauração prevista no MVP.
- **Testes planejados:** álbum com e sem avaliação/links; cancelamento; confirmação; gêneros compartilhados com outro álbum; falha em parte da exclusão mantém todos os dados; reinício confirma ausência dos removidos.
- **Risco principal:** exclusão parcial ou remoção de dados de outros álbuns.
- **Referências:** RF-10; RN-17, RN-18; RNF-01, RNF-02, RNF-03; CA-12, CA-14, CA-15.

### B27 — Excluir artista mediante confirmação

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** remover artista, seus álbuns e dependentes integralmente.
- **Dependências:** B26.
- **Aceitação:** apresentar quais álbuns ou sua quantidade e a remoção de avaliações e links; cancelar preserva tudo; confirmar remove somente o artista e seus dependentes; artista sem álbuns também pode ser excluído. Preservar outros artistas, álbuns e seus gêneros.
- **Testes planejados:** artista vazio; vários álbuns com avaliações e links; cancelamento; confirmação; dados de outros artistas preservados; falha em parte da operação não confirma nenhuma remoção; reinício.
- **Risco principal:** perda parcial ou exclusão de dados de outros artistas.
- **Referências:** RF-10; RN-17, RN-18; RNF-01, RNF-02, RNF-03; CA-13, CA-14, CA-15.

## 7. Verificação final do MVP — P3

Estas tarefas integram e ampliam verificações realizadas nas entregas anteriores. Não substituem os testes de cada tarefa.

### B28 — Tratar referências antigas

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** informar inexistência de artista ou álbum removido sem efeitos indevidos.
- **Dependências:** B27.
- **Aceitação:** consultar ou alterar por referência antiga informa que o registro não existe; não recria dados nem modifica outro registro. Recusar novas relações com artista ou álbum removido.
- **Testes planejados:** consultar e editar artista/álbum excluído; cadastrar ou transferir álbum para artista removido; tentar registrar audição, avaliação ou link em álbum removido; verificar ausência de recriação e de dependentes órfãos.
- **Risco principal:** recriação acidental ou referências inválidas.
- **Referências:** RF-01, RF-02, RF-06, RF-07, RF-09; RN-05; RNF-02, RNF-03; CA-15.

### B29 — Verificar persistência do fluxo completo

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** comprovar persistência integrada de todos os dados do MVP.
- **Dependências:** B06, B11, B17, B25, B27.
- **Aceitação:** após cadastro, edição, transferência, mudança de gêneros, audição, avaliação, links e exclusões concluídas, reiniciar normalmente e obter o estado resultante, inclusive ausência de registros excluídos. Consultas e sorteios não devem mudar dados.
- **Testes planejados:** cenário integrado com mais de um artista e álbuns, alterações e exclusões; reinício real do ambiente local de teste e conferência dos dados remanescentes e removidos.
- **Risco principal:** sucesso aparente com dados mantidos apenas na memória.
- **Referências:** RF-01, RF-02, RF-06, RF-07, RF-08, RF-09, RF-10; RN-14, RN-18; RNF-01; CA-14.

### B30 — Verificar falhas e consistência entre operações

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** consolidar a proteção contra alterações parciais no fluxo integrado.
- **Dependências:** B28, B29.
- **Aceitação:** em falhas relevantes ao salvar, transferir, desmarcar ou excluir, manter estado anterior integral, mensagem útil e ausência de sucesso falso; não deixar dependentes órfãos.
- **Testes planejados:** simular falhas em gravações e nas etapas relacionadas da transferência, limpeza de avaliação, exclusão de álbum e exclusão de artista; conferir estado completo antes/depois e mensagem apresentada. Reutilizar cenários existentes e ampliar somente lacunas identificadas.
- **Risco principal:** testes isolados passarem enquanto o fluxo integrado permite estado parcial.
- **Referências:** RNF-02, RNF-03, RNF-05; CA-09, CA-12, CA-13, CA-15.

### B31 — Revisar evidências de aceitação

- **Estado / prioridade:** Pendente / P3.
- **Objetivo:** decidir a aceitação do MVP com cobertura rastreável e limitações explícitas.
- **Dependências:** B13, B30.
- **Aceitação:** relacionar todos os cenários CA-01 a CA-16 às evidências; revisar também RF, RN e RNF na matriz abaixo; confirmar testes cruzados de preservação e sorteio. Não declarar o MVP concluído com critério obrigatório pendente.
- **Testes e verificações planejados:** executar os testes pertinentes do MVP; conferir criações e edições simultâneas conflitantes de artistas e álbuns, incluindo transferência, com unicidade preservada e conflitos informados; conferir validação, seleção vazia, cancelamentos e falhas; registrar resultados e lacunas reais.
- **Risco principal:** confundir existência de teste planejado com comportamento demonstrado.
- **Referências:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-10; RNF-01, RNF-02, RNF-03, RNF-04, RNF-05; CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07, CA-08, CA-09, CA-10, CA-11, CA-12, CA-13, CA-14, CA-15, CA-16.

**Marco 3 — MVP completo:** todas as 31 tarefas concluídas com critérios demonstrados, falhas e concorrência verificadas e limitações registradas. Publicação não faz parte deste marco.

## 8. Matriz de cobertura planejada

As relações abaixo indicam onde o comportamento será entregue ou verificado; não indicam conclusão. Critérios comuns também se aplicam às tarefas pertinentes.

| Referência | Tarefas principais |
| --- | --- |
| RF-01 | B03, B04, B06 |
| RF-02 | B07, B08, B10, B11, B12 |
| RF-03 | B05, B09 |
| RF-04 | B13, B14 |
| RF-05 | B15, B16 |
| RF-06 | B18, B22 |
| RF-07 | B19, B20, B21, B22 |
| RF-08 | B17 |
| RF-09 | B23, B24, B25 |
| RF-10 | B26, B27 |
| RN-01 | B04, B08, B12, B23, B24 |
| RN-02 | B04, B06 |
| RN-03 | B08, B10, B11 |
| RN-04 | B03, B06, B07, B10 |
| RN-05 | B06, B07, B11, B28 |
| RN-06 | B12 |
| RN-07 | B05, B09 |
| RN-08 | B13, B14 |
| RN-09 | B15, B16, B17 |
| RN-10 | B14, B15, B16, B17 |
| RN-11 | B05, B09, B10, B13, B14 |
| RN-12 | B07, B18, B19, B20, B21 |
| RN-13 | B18, B22 |
| RN-14 | B17, B20, B29 |
| RN-15 | B17 |
| RN-16 | B23, B24, B25 |
| RN-17 | B26, B27 |
| RN-18 | B26, B27 |
| RNF-01 | Tarefas de alteração de dados, B29 |
| RNF-02 | Tarefas de validação e alteração de dados, B28, B30 |
| RNF-03 | Tarefas de alteração de dados, B22, B26, B27, B28, B30 |
| RNF-04 | B04, B06, B08, B10, B11, B31 |
| RNF-05 | Critérios comuns, B01, B02, B17, B19, B20, B30, B31 |
| CA-01 | B03, B06 |
| CA-02 | B07, B10, B11, B12, B19, B20, B23 |
| CA-03 | B04, B06, B08, B10, B11 |
| CA-04 | B05, B09 |
| CA-05 | B13, B14 |
| CA-06 | B15, B16 |
| CA-07 | B18, B22 |
| CA-08 | B19, B20, B21 |
| CA-09 | B22, B30 |
| CA-10 | B17, B20 |
| CA-11 | B23, B24, B25 |
| CA-12 | B26, B30 |
| CA-13 | B27, B30 |
| CA-14 | Tarefas de alteração de dados, B29 |
| CA-15 | Critérios comuns, B22, B26, B27, B28, B30 |
| CA-16 | B04, B06, B08, B10, B11, B31 |

## 9. Evoluções posteriores e limites

**Possibilidades a investigar depois do MVP, sem tarefas de implementação autorizadas:** histórico de audições, filtro por estado de audição, homônimos, edições distintas, colaborações entre artistas, importação de metadados ou discografias e recomendações automáticas. A inclusão futura depende de nova análise e critérios próprios.

**Fora do MVP:** múltiplos usuários, integração com RYM, reprodução interna e coleções temáticas como eixo de organização. A coleção inicial contém somente registros adicionados manualmente pelo usuário.

**Antes de qualquer publicação:** definir autenticação, permissões, exposição de dados, acesso remoto, política de backup, volume esperado, ambiente de hospedagem e metas operacionais de desempenho, disponibilidade e capacidade. Não presumir que uso pessoal autoriza exposição pública. Essas decisões exigem planejamento separado e não bloqueiam o uso local do MVP; nenhuma infraestrutura é escolhida aqui.

## 10. Próxima ação e revisão de aprendizado

**Próxima tarefa sugerida: B03 — cadastrar artista.** O ambiente mínimo foi verificado na B02. Começar pelo teste de cadastro válido, respeitando os critérios da B03 e a mentoria em pequenas etapas; o autor escreve testes e implementação. A conclusão da preparação não comprova funcionalidades de produto.

Ao final de cada ciclo, explicar com as próprias palavras: qual regra foi protegida por um teste, qual resultado comprova isso e qual dependência permite escolher a tarefa seguinte? A revisão apoia o aprendizado e não condiciona a entrega documental deste backlog.
