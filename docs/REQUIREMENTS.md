# Requisitos — Biblioteca pessoal de álbuns

## 1. Objetivo e origem das decisões

Este documento especifica o MVP, a menor versão útil para testar a ideia. Não escolhe tecnologias nem descreve uma implementação.

**Problema:** os álbuns de interesse são encontrados nos streamings, mas falta uma biblioteca pessoal organizada para reencontrá-los e escolher o que ouvir.

**Usuário inicial:** o próprio dono da biblioteca, que utiliza principalmente serviços de streaming.

**Resultados esperados:** consultar a coleção por artista, distinguir álbuns que deseja ouvir daqueles que já ouviu e receber uma escolha aleatória quando estiver indeciso.

As decisões usam estas marcações:

| Marca | Significado | Como interpretar |
| --- | --- | --- |
| C — Confirmado | Escopo aceito na conversa. | Compõe a base acordada do MVP. |
| D — Derivado | Comportamento necessário para tornar o escopo observável e consistente. | A justificativa explica sua relação com o escopo. Não representa uma nova funcionalidade independente. |

Fontes das confirmações:

- O usuário descreveu uma biblioteca pessoal de álbuns, organizada por artista, para quem ouve principalmente em streamings.
- Considerou úteis situação de escuta, gênero e época, dando maior prioridade à situação de escuta; também pediu sorteio de um álbum da biblioteca.
- Aceitou começar sem gênero e época, mantendo artista, situação de escuta e sorteio.
- Confirmou o resumo do MVP: cadastro manual com título, artista e situação; consulta por artista; busca por título; filtro de situação; sorteio respeitando filtros; correção e armazenamento dos dados.
- Na revisão de 12/11/2026, resolveu L-01 a L-08 e aprovou a avaliação com 20 álbuns por uma semana. As decisões estão registradas na seção 9 e incorporadas às regras e aos critérios abaixo.
- Nessa revisão, ampliou o MVP para incluir exportação e restauração manual da coleção por arquivo, com substituição após confirmação e preservação dos dados em caso de falha.

## 2. Escopo e prioridades

**Dentro do MVP — C:**

1. Cadastrar manualmente título, artista e situação de escuta.
2. Consultar a biblioteca organizada por artista e buscar por título.
3. Filtrar por situação de escuta.
4. Sortear um álbum entre os resultados dos filtros ativos.
5. Corrigir os dados de um álbum.
6. Manter a coleção salva entre sessões de uso.
7. Exportar a coleção completa para cópia manual e restaurá-la a partir desse arquivo.

**Depois do MVP — C:** gênero e ano/década de lançamento.

**Fora do MVP — C:** integração com streaming, reprodução de áudio, recomendações automáticas, compartilhamento, sincronização, edição simultânea e backup automático.

**Sem requisito aprovado:** exclusão de álbuns, capas, links para streaming, contas de usuários e importação de fontes externas. Não devem ser incluídos automaticamente no escopo. A restauração aprovada utiliza o arquivo próprio da aplicação.

**Ambiente e restrições — C:** uso pessoal no navegador de um computador, em uma sessão por vez, no próprio perfil do sistema/navegador. Validar em versões estáveis atuais de Chrome e Firefox no computador do usuário, no momento da verificação. Não há promessa de isolamento em dispositivo compartilhado nem senha própria da aplicação. O projeto é de estudo, sem prazo fixo, com avanço em microtarefas conforme a disponibilidade e sem custos recorrentes obrigatórios no MVP.

**Justificativa do recorte:** a situação de escuta recebeu maior prioridade e permite testar uma decisão concreta: ouvir algo novo ou revisitar um álbum. O sorteio atende à indecisão. Gênero e época podem ser avaliados depois de observar o uso desse núcleo.

## 3. Dados e entradas

| Dado | Regra | Origem e justificativa |
| --- | --- | --- |
| Título | Texto obrigatório com pelo menos um caractere visível e no máximo 200 caracteres. | C: campo e limite aprovados. D: um valor vazio não permite identificar o álbum. |
| Artista | Texto obrigatório com pelo menos um caractere visível e no máximo 200 caracteres. | C: base da organização e limite aprovado. D: um valor vazio impediria essa organização. |
| Situação de escuta | Exatamente um valor: `quero ouvir` ou `já ouvi`. | C: os dois estados foram aceitos para o MVP. |
| Busca por título | Texto opcional com no máximo 200 caracteres; vazio ou apenas espaços significa ausência dessa restrição. | C: busca por título e limite aprovados. D: permitir voltar a consultar a coleção inteira. |
| Seleção de artista | Um artista da coleção ou todos. | C: seleção para consulta e sorteio aprovada. |
| Filtro de situação | `quero ouvir`, `já ouvi` ou todas as situações. | D: restringir a consulta sem impedir a visão da coleção inteira. |

**C — Normalização para comparação:** ignorar diferenças entre maiúsculas/minúsculas, acentos e espaços excedentes ao buscar, agrupar artistas e verificar duplicatas. Desconsiderar espaços nas pontas e tratar sequências de espaços internos como um único espaço na comparação. Exemplo: ` ÁLBUM ` e `album` são equivalentes para comparação. Preservar a grafia informada para exibição, retirando espaços no início e no fim.

**Justificativa:** pequenas diferenças de digitação não devem dificultar a localização. O usuário aceitou que essas diferenças também não criem artistas ou álbuns distintos para agrupamento e duplicatas.

**C — Representação de artista:** um campo de texto por álbum, sem cadastro separado de integrantes ou participações. Um álbum com vários artistas pode usar um nome composto nesse campo; não haverá classificação independente por cada participante no MVP. Por exemplo, `Artista A e Artista B` forma um agrupamento próprio.

**C — Capacidade:** validar as operações do MVP com uma coleção de 10.000 álbuns. Esse é o volume de aceitação, não uma regra para rejeitar automaticamente o álbum seguinte. A tecnologia e o local de armazenamento, assim como o formato técnico do arquivo de recuperação, serão definidos no projeto da solução.

## 4. Requisitos funcionais — RF

Requisito funcional descreve algo que o usuário consegue fazer.

| ID | Requisito | Origem | Decisão e justificativa |
| --- | --- | --- | --- |
| RF-01 | Cadastrar manualmente um álbum com título, artista e situação de escuta. | C | Permitir construir a coleção sem depender de integração com serviços externos. |
| RF-02 | Consultar todos os álbuns organizados por artista e selecionar um artista para restringir a consulta. | C | A organização por artista é central ao problema; a seleção oferece um conjunto claro para consulta e sorteio. |
| RF-03 | Buscar álbuns por um trecho do título, usando a comparação descrita na seção 3. | C | Usar um trecho reduz a necessidade de lembrar o nome completo. |
| RF-04 | Filtrar a consulta por situação de escuta e retirar essa restrição quando desejado. | C / D | Distinguir o que o usuário quer ouvir do que já ouviu. |
| RF-05 | Sortear um álbum entre os resultados da consulta atual, respeitando todos os filtros e a busca ativos. | C / D | A escolha aleatória deve corresponder ao conjunto que o usuário está consultando. |
| RF-06 | Editar título, artista e situação de um álbum cadastrado. | C | Permitir correções e a mudança manual de situação após a escuta. |
| RF-07 | Recuperar a coleção salva ao encerrar e reabrir a aplicação no mesmo ambiente de uso. | C / D | Uma biblioteca precisa continuar disponível entre sessões. Isso não define armazenamento local, remoto ou sincronização. |
| RF-08 | Exportar a coleção completa, incluindo título, artista e situação de todos os álbuns, para um arquivo próprio da aplicação que o usuário possa guardar como cópia manual. | C | Permitir recuperação posterior sem backup automático. A exportação independe dos filtros ativos. |
| RF-09 | Restaurar a coleção a partir do arquivo próprio da aplicação, substituindo integralmente a coleção atual após validação completa e confirmação explícita do usuário. | C / D | Recuperar uma cópia sem mesclar coleções. Cancelamento, arquivo inválido ou falha devem preservar os dados anteriores. |

## 5. Regras de negócio — RN

Regra de negócio determina quais dados e comportamentos são permitidos, independentemente da tecnologia escolhida.

| ID | Regra | Origem | Justificativa |
| --- | --- | --- | --- |
| RN-01 | Não aceitar cadastro ou edição com título/artista ausente, vazio ou contendo apenas espaços, nem situação fora dos dois valores permitidos. | D | Evitar registros que não podem ser identificados ou classificados. |
| RN-02 | Cada álbum tem uma única situação de escuta. A mudança individual ocorre pela edição feita pelo usuário; uma restauração recupera as situações da cópia ao substituir a coleção. Consultar ou sortear não altera a situação. | C / D | Sortear um álbum não comprova que ele foi ouvido. |
| RN-03 | Combinar artista, busca por título e situação pela interseção; o álbum precisa atender a todas as restrições ativas. Sem restrições, considerar toda a biblioteca. | C | Tornar o conjunto apresentado e o conjunto elegível para sorteio previsíveis. |
| RN-04 | O resultado do sorteio deve pertencer à biblioteca e ao conjunto elegível no momento da ação. | C / D | Impedir resultados fora da seleção do usuário. |
| RN-05 | Todos os álbuns elegíveis têm a mesma chance em cada sorteio independente, que pode repetir o resultado anterior. Com um único elegível, sempre retornar esse álbum. | C | A prioridade dada à situação de escuta não representa um peso estatístico. Não há exclusão de resultados anteriores. |
| RN-06 | Se não houver álbum elegível, informar que não há resultado e não apresentar um álbum como se tivesse sido sorteado. | D | Um conjunto vazio não permite uma escolha válida. |
| RN-07 | Bloquear duplicatas com o mesmo título e artista após a normalização da seção 3, independentemente da situação de escuta. Mesmo título com artistas diferentes é permitido. | C | Evitar repetição acidental e aumento indevido da chance no sorteio. Edições diferentes do mesmo álbum não têm identificação própria no MVP. |
| RN-08 | Na edição, desconsiderar o próprio registro ao verificar duplicatas. Alterar apenas o álbum escolhido e atualizar sua posição nos resultados conforme os novos dados. | D | Salvar sem alterações deve ser possível; corrigir um artista não deve modificar outros álbuns. |
| RN-09 | Só confirmar cadastro, edição ou restauração depois de salvar integralmente. Em falha, informar que a operação não foi concluída e preservar os registros anteriores. | D | Evitar que o usuário acredite ter salvo algo que será perdido; uma restauração não pode deixar a coleção parcialmente substituída. |
| RN-10 | Falha ao ler a coleção não deve ser tratada como uma biblioteca vazia nem provocar sua sobrescrita. | D | Distinguir ausência de registros de impossibilidade de acessar os registros existentes. |
| RN-11 | Rejeitar título, artista ou busca com mais de 200 caracteres, identificando o campo e o limite, sem truncar silenciosamente. Não salvar cadastro/edição nem aplicar uma busca excedente. | C / D | Respeitar os limites aprovados sem alterar o texto para aparentar uma entrada válida. |
| RN-12 | Antes de substituir a coleção, validar o arquivo de restauração por completo: formato próprio da aplicação, campos obrigatórios, limites, situações permitidas e ausência de duplicatas segundo RN-07 dentro da cópia. | D | Um arquivo inválido não pode causar substituição parcial ou violar as regras da biblioteca. A coleção atual não é mesclada à cópia. |
| RN-13 | Informar que a restauração substituirá toda a coleção atual e exigir confirmação explícita antes de gravar. Cancelar deve preservar a coleção atual. | C / D | Tornar a substituição revisável pelo usuário antes da perda dos registros atuais. |
| RN-14 | Exportar todos os registros salvos, sem alterar a coleção. Confirmar a exportação somente após gerar o arquivo; em falha, informar que a cópia não foi concluída. | D | Filtros não podem produzir uma cópia incompleta apresentada como completa. |

## 6. Requisitos não funcionais — RNF

Requisito não funcional descreve uma qualidade ou restrição do funcionamento.

| ID | Requisito | Origem | Evidência esperada e justificativa |
| --- | --- | --- | --- |
| RNF-01 | Preservar os dados confirmados entre encerramento e reabertura no mesmo ambiente suportado. | C / D | Recuperar os valores cadastrados, editados e restaurados. Recuperação após perda dos dados depende de uma cópia manual previamente exportada e guardada pelo usuário; não há recuperação automática prometida. |
| RNF-02 | Comunicar validação, confirmação, ausência de resultados e falhas de leitura/gravação de forma distinguível. | D | O usuário deve saber se precisa corrigir dados, mudar filtros ou tentar novamente; verificar os cenários correspondentes da seção 7. |
| RNF-03 | As operações do MVP não devem exigir conta, autenticação ou acesso a APIs de streaming. | C / D | Uso pessoal no próprio perfil, sem senha da aplicação nem garantia de isolamento em dispositivo compartilhado. Não implica promessa de funcionamento sem internet. |
| RNF-04 | Tratar título, artista e busca como texto; seu conteúdo não pode executar comandos ou código. | D | São dados da biblioteca. Texto como `<script>` deve permanecer texto, sem execução. |
| RNF-05 | Apresentar campos, situações e mensagens em português brasileiro, identificando o campo que precisa de correção. | C | Facilitar o uso e permitir corrigir uma entrada sem interpretar mensagens técnicas. |
| RNF-06 | Suportar as operações do MVP com uma coleção de 10.000 álbuns no ambiente definido na seção 2. | C | Verificar cadastro, consulta, filtros, sorteio, edição, persistência, exportação e restauração nesse volume. |
| RNF-07 | Permitir todos os fluxos por teclado, com foco visível, campos com rótulos, contraste legível e mensagens que não dependam apenas de cor. | C | Verificar os fluxos de ponta a ponta nos dois navegadores suportados. |
| RNF-08 | O uso do MVP não deve exigir custos recorrentes. | C | Respeitar o orçamento aprovado para o projeto de estudo. |

Não há metas numéricas aprovadas de tempo de resposta ou disponibilidade. A capacidade de aceitação é de 10.000 álbuns; a amostra de 20 álbuns da seção 10 avalia a utilidade do produto e não é um limite de capacidade.

## 7. Critérios de aceitação

Cada cenário usa **Dado** para o contexto, **Quando** para a ação e **Então** para o resultado observável. São especificações para verificação futura; não representam testes executados. As propostas revisadas foram confirmadas e incorporadas aos cenários.

### RF-01 — Cadastro

**CA-01 — Cadastro válido — C / D**

- **Dado** que título, artista e uma das situações permitidas foram informados;
- **Quando** o usuário salvar e a gravação for concluída;
- **Então** confirmar o cadastro e disponibilizar o álbum na biblioteca com os valores informados, retirando espaços nas pontas de título e artista para exibição.

**CA-02 — Entrada inválida — D**

- **Dado** que título ou artista está ausente, vazio ou só com espaços, ou a situação não é permitida;
- **Quando** houver tentativa de salvar;
- **Então** identificar o dado inválido e não criar um registro parcial.

**CA-03 — Duplicata — C; RN-07**

- **Dado** um álbum já cadastrado com título `Álbum  Exemplo` (dois espaços internos) e artista `Artista A`;
- **Quando** houver tentativa de cadastrar ` album exemplo ` de `ARTISTA A`, mesmo com outra situação;
- **Então** informar a duplicidade e manter um único registro.

**CA-04 — Mesmo título, outro artista — C; RN-07**

- **Dado** um álbum chamado `Encontro`, de `Artista A`;
- **Quando** o usuário cadastrar `Encontro`, de `Artista B`, com os demais dados válidos;
- **Então** permitir o cadastro e manter os dois álbuns separados.

### RF-02 — Consulta por artista

**CA-05 — Biblioteca organizada — C / D**

- **Dado** que existem álbuns de pelo menos dois artistas;
- **Quando** o usuário consultar toda a biblioteca;
- **Então** permitir identificar os álbuns de cada artista e distinguir títulos e situações de escuta.

**CA-06 — Seleção e agrupamento — C**

- **Dado** que existem álbuns cadastrados para `Artista A`, ` artista a ` e `Artista B`;
- **Quando** o usuário consultar o primeiro artista;
- **Então** reunir os dois primeiros na mesma seleção e não incluir os álbuns de `Artista B`.

**CA-07 — Biblioteca inicialmente vazia — D**

- **Dado** que ainda não existe álbum cadastrado;
- **Quando** o usuário abrir a biblioteca;
- **Então** informar que não há álbuns e permitir iniciar um cadastro.

### RF-03 — Busca por título

**CA-08 — Correspondência parcial — C**

- **Dado** o álbum `Canção do Dia`, de `Artista A`;
- **Quando** o usuário buscar ` CANCAO `, sem outras restrições;
- **Então** incluir esse álbum no resultado.

**CA-09 — Busca vazia ou sem correspondência — C / D**

- **Dado** que uma busca está restringindo a consulta;
- **Quando** o usuário apagar o texto ou deixá-lo apenas com espaços;
- **Então** retirar somente a restrição de título, preservando artista e situação selecionados.
- **Dado** que nenhum título corresponde a uma busca preenchida;
- **Quando** a consulta for aplicada;
- **Então** informar a ausência de resultados sem alterar os registros salvos.

### RF-04 — Filtro de situação

**CA-10 — Uma situação ou todas — C / D**

- **Dado** que a biblioteca contém álbuns nas duas situações;
- **Quando** o usuário selecionar `quero ouvir` ou `já ouvi`;
- **Então** apresentar apenas os álbuns dessa situação que atendam às demais restrições ativas.
- **Quando** selecionar todas as situações;
- **Então** retirar apenas essa restrição, preservando artista e busca.

**CA-11 — Combinação de restrições — C; RN-03**

- **Dado** o álbum A: `Encontro`, `Artista A`, `quero ouvir`; B: `Encontro`, `Artista B`, `quero ouvir`; C: `Noite`, `Artista A`, `quero ouvir`; D: `Outro Encontro`, `Artista A`, `já ouvi`;
- **Quando** o usuário selecionar `Artista A`, buscar `encontro` e filtrar por `quero ouvir`;
- **Então** o conjunto de resultados conterá somente o álbum A.

### RF-05 — Sorteio

**CA-12 — Respeitar a consulta — C / D**

- **Dado** que a consulta atual possui álbuns elegíveis e exclui outros por artista, título ou situação;
- **Quando** o usuário solicitar um sorteio;
- **Então** apresentar título, artista e situação de um único álbum elegível, sem modificar os registros.

**CA-13 — Sem restrições — D**

- **Dado** que há álbuns na biblioteca e não há restrições ativas;
- **Quando** houver um sorteio;
- **Então** o resultado poderá ser qualquer álbum da biblioteca, inclusive um marcado como `já ouvi`.

**CA-14 — Um ou nenhum elegível — D**

- **Dado** que existe exatamente um álbum elegível;
- **Quando** houver um sorteio;
- **Então** apresentar esse álbum.
- **Dado** que a biblioteca está vazia ou os filtros não encontram álbuns;
- **Quando** houver tentativa de sorteio;
- **Então** informar a ausência de opções, sem apresentar um resultado anterior como um novo sorteio.

**CA-15 — Repetição permitida — C; RN-05**

- **Dado** que um álbum foi sorteado e continua elegível;
- **Quando** houver outro sorteio;
- **Então** esse álbum continuará elegível, sem obrigação de alternar resultados.

A igualdade de chances de RN-05 deve ser verificável pela regra de seleção adotada. Observar poucos sorteios, ou exigir contagens exatamente iguais, não comprova nem refuta essa propriedade. A estratégia de verificação será definida junto à implementação.

### RF-06 — Edição

**CA-16 — Corrigir um álbum — C / D**

- **Dado** um álbum cadastrado;
- **Quando** o usuário alterar título, artista ou situação e a gravação for concluída;
- **Então** confirmar a edição, manter apenas o registro atualizado e preservar os demais álbuns.

**CA-17 — Efeito nos filtros — D**

- **Dado** um álbum visível no filtro `quero ouvir`;
- **Quando** sua situação for alterada e salva como `já ouvi`;
- **Então** retirá-lo dos resultados desse filtro e dos próximos sorteios desse conjunto, mantendo-o disponível ao consultar `já ouvi`.

**CA-18 — Edição inválida ou duplicada — C / D**

- **Dado** um álbum existente;
- **Quando** uma edição produzir dados inválidos ou duplicar outro álbum segundo RN-07;
- **Então** informar o motivo e preservar os dados anteriores sem confirmar a edição.
- **Quando** os valores forem salvos sem alterações;
- **Então** o próprio álbum não será considerado uma duplicata.

### RF-07 e RNF-01 — Persistência

**CA-19 — Reabertura — C / D**

- **Dado** que cadastros, edições ou restauração receberam confirmação de gravação;
- **Quando** a aplicação for encerrada e reaberta no mesmo ambiente suportado;
- **Então** recuperar os valores mais recentes confirmados, incluindo as situações de escuta.

Persistir a seleção de filtros e o último sorteio não faz parte desse requisito.

### Falhas e tratamento dos dados

**CA-20 — Falha de gravação — D; RN-09 / RNF-02**

- **Dado** que a gravação não pode ser concluída, inclusive por falta de espaço ou permissão;
- **Quando** o usuário tentar cadastrar, editar ou restaurar;
- **Então** informar que a operação não foi salva, não emitir confirmação de sucesso e preservar os registros previamente confirmados.

**CA-21 — Falha de leitura — D; RN-10 / RNF-02**

- **Dado** que uma coleção existente não pode ser lida;
- **Quando** a aplicação tentar abri-la;
- **Então** informar a falha, distinguir esse estado de uma coleção vazia e não substituir os dados existentes por uma biblioteca vazia.

**CA-22 — Independência de streaming — D; RNF-03**

- **Dado** que o usuário não conectou uma conta de streaming;
- **Quando** cadastrar, consultar, editar, sortear, exportar ou restaurar álbuns;
- **Então** essas operações não exigirão autorização ou comunicação com APIs de streaming.

**CA-23 — Dados tratados como texto — D; RNF-04**

- **Dado** um título contendo símbolos ou texto como `<script>`;
- **Quando** ele for salvo, exibido ou usado na busca;
- **Então** seu conteúdo será tratado como texto, sem execução de código ou comandos.

**CA-24 — Mensagens compreensíveis — C; RNF-05**

- **Dado** um título obrigatório em branco;
- **Quando** o usuário tentar salvar;
- **Então** apresentar em português uma mensagem que identifique o título como o dado a corrigir.

### Limites de entrada

**CA-25 — Limite de caracteres — C / D; RN-11**

- **Dado** um título, artista ou busca com exatamente 200 caracteres, atendendo às demais regras;
- **Quando** o usuário cadastrar, editar ou buscar, conforme o campo;
- **Então** aceitar a entrada sem cortar seu conteúdo.
- **Dado** um desses campos com 201 caracteres;
- **Quando** houver tentativa de salvar ou aplicar a busca;
- **Então** identificar o campo e o limite de 200 caracteres em português, sem truncar o conteúdo, salvar dados inválidos ou aplicar a busca excedente.

### RF-08 e RF-09 — Cópia manual e recuperação

**CA-26 — Exportação completa — C / D; RN-14**

- **Dado** que existem álbuns nas duas situações e filtros que ocultam parte da coleção;
- **Quando** o usuário exportar e a geração do arquivo for concluída;
- **Então** disponibilizar um arquivo próprio da aplicação com título, artista e situação de todos os registros salvos, confirmar a exportação e preservar a coleção atual.

**CA-27 — Falha de exportação — D; RN-14 / RNF-02**

- **Dado** que a coleção não pode ser lida integralmente ou o arquivo não pode ser gerado;
- **Quando** houver tentativa de exportação;
- **Então** informar que a cópia não foi concluída, sem confirmar sucesso, apresentar uma cópia parcial como completa ou alterar os dados da coleção.

**CA-28 — Restauração válida — C / D; RN-09 / RN-12 / RN-13**

- **Dado** um arquivo exportado válido e uma coleção atual com registros diferentes;
- **Quando** o usuário selecionar o arquivo, a validação completa for concluída, o usuário confirmar a substituição e a gravação terminar;
- **Então** confirmar a restauração e disponibilizar exatamente os álbuns da cópia, com seus títulos, artistas e situações, sem mesclar os registros anteriores.
- **Quando** a aplicação for encerrada e reaberta no mesmo ambiente;
- **Então** recuperar a coleção restaurada.

**CA-29 — Cancelamento da restauração — C / D; RN-13**

- **Dado** um arquivo válido selecionado para restauração;
- **Quando** a aplicação informar que substituirá integralmente a coleção e o usuário cancelar;
- **Então** manter os registros anteriores sem confirmar restauração ou gravar a cópia sobre eles.

**CA-30 — Arquivo inválido — D; RN-12**

- **Dado** um arquivo ilegível, incompatível com o formato próprio, com campos obrigatórios ausentes, valores inválidos, textos acima do limite ou duplicatas dentro da cópia segundo RN-07;
- **Quando** houver tentativa de restauração;
- **Então** rejeitar o arquivo por completo, informar o motivo e preservar a coleção atual, sem restaurar parcialmente os registros válidos.

**CA-31 — Falha durante a restauração — D; RN-09**

- **Dado** que o usuário confirmou uma restauração válida;
- **Quando** ocorrer falha durante a gravação;
- **Então** informar que a restauração não foi salva, não confirmar sucesso e preservar integralmente a coleção anteriormente confirmada, inclusive após reabrir a aplicação.

### Capacidade e acessibilidade

**CA-32 — Coleção com 10.000 álbuns — C; RNF-06**

- **Dado** uma coleção de 10.000 álbuns válidos com diferentes artistas e situações, no ambiente suportado;
- **Quando** forem exercitados cadastro até esse volume, consulta, busca, filtros combinados, sorteio, edição, reabertura, exportação e restauração;
- **Então** atender aos critérios funcionais correspondentes, preservando os dados e mantendo o sorteio dentro do conjunto elegível.

Esse cenário deve ser verificado em Chrome e Firefox nas versões estáveis atuais no momento da verificação. Não exige tempos numéricos de resposta nem impõe rejeição acima desse volume.

**CA-33 — Uso por teclado e comunicação visual — C; RNF-07**

- **Dado** o uso da aplicação em cada navegador suportado;
- **Quando** o usuário percorrer cadastro, consulta, filtros, sorteio, edição, exportação e restauração usando apenas o teclado;
- **Então** permitir concluir e cancelar as ações quando aplicável, com foco visível, campos identificados por rótulos e sem depender do mouse.
- **Quando** houver instruções, validação, confirmação, ausência de resultados ou falhas;
- **Então** apresentar texto com contraste legível e informação compreensível sem depender apenas de cor.

## 8. Casos de borda, permissões e concorrência

| Caso | Tratamento especificado | Referência |
| --- | --- | --- |
| Zero álbuns ou nenhum resultado após filtros | Informar a ausência de resultados; não produzir sorteio inválido. | CA-07, CA-09, CA-14 |
| Um único álbum elegível | O sorteio retorna esse álbum. | CA-14 |
| Somente álbuns já ouvidos | Participam quando o filtro permite; não participam de `quero ouvir`. | CA-10, CA-13 |
| Mesmo título, artistas diferentes | Permitir os dois registros. | RN-07, CA-04 |
| Mesmo título e artista em edições diferentes | Não distinguir edições no MVP; bloquear título e artista equivalentes. | RN-07 |
| Maiúsculas, acentos ou espaços diferentes | Comparar como equivalentes, preservando a grafia de exibição e retirando espaços nas pontas. | Seção 3, CA-03, CA-06, CA-08 |
| Novo artista informado na edição | O álbum muda de agrupamento; os demais registros permanecem iguais. | RN-08, CA-16 |
| Alteração que faz o álbum sair do filtro atual | Atualizar consulta e próximos sorteios; não apagar o álbum. | CA-17 |
| Gravação sem permissão ou espaço | Não confirmar sucesso nem perder registros anteriores. | CA-20 |
| Coleção inacessível ou ilegível | Não confundir com coleção vazia nem sobrescrever dados. | CA-21 |
| Permissões de usuários | Uso pessoal no próprio perfil do sistema/navegador, sem contas, papéis de acesso ou senha da aplicação. Não há garantia de isolamento em dispositivo compartilhado. | RNF-03, L-05 |
| Duas janelas, sessões ou dispositivos editando ao mesmo tempo | Fora do suporte do MVP: validar uma sessão por vez, sem prometer sincronização ou resolução de conflitos. | L-04 |
| Muitos álbuns ou textos extensos | Validar capacidade com 10.000 álbuns e rejeitar campos acima de 200 caracteres com mensagem explícita, sem truncamento silencioso. | CA-25, CA-32 |
| Filtros ativos durante a exportação | Exportar a coleção completa, incluindo registros ocultos pelos filtros. | CA-26 |
| Cópia de uma coleção vazia | Permitir exportar e restaurar uma coleção vazia válida; a substituição também exige confirmação e deixa a biblioteca vazia. | RF-08, RF-09, RN-13 |
| Arquivo inválido ou falha na restauração | Rejeitar a operação inteira, informar a falha e preservar a coleção anterior. | CA-30, CA-31 |
| Perda dos dados do ambiente de uso | Recuperação depende de arquivo válido previamente exportado e guardado pelo usuário; não há backup automático. | RNF-01, RF-08, RF-09 |

## 9. Lacunas resolvidas e decisões confirmadas

Todas as lacunas L-01 a L-08 foram resolvidas com o usuário na revisão de 12/11/2026. O encerramento é documental e não representa implementação ou verificação das funcionalidades.

| ID | Tema | Decisão confirmada | Referências |
| --- | --- | --- | --- |
| L-01 | Duplicatas e edições diferentes. | Um registro por título e artista equivalentes, independentemente da situação. Mesmo título com outro artista é permitido; edições não têm identificação própria. | RN-07, RN-08, CA-03, CA-04, CA-18 |
| L-02 | Comparação, consulta e vários artistas. | Ignorar maiúsculas, acentos e espaços excedentes nas comparações; preservar grafia de exibição, retirando espaços nas pontas. Busca parcial e filtros por interseção. Um campo de artista, com nomes compostos formando agrupamento próprio. | Seção 3, RF-02, RF-03, RN-03 |
| L-03 | Plataforma, capacidade e entradas. | Navegador no computador; validar 10.000 álbuns. Até 200 caracteres em título, artista e busca, com rejeição explícita do excesso. Sem meta numérica de desempenho aprovada. | Seções 2 e 3, RN-11, RNF-06, CA-25, CA-32 |
| L-04 | Uso simultâneo. | Uma sessão por vez. Edição simultânea, sincronização e resolução de conflitos ficam fora do suporte do MVP. | Seções 2 e 8 |
| L-05 | Privacidade e recuperação. | Uso pessoal no próprio perfil, sem senha da aplicação ou garantia de isolamento em dispositivo compartilhado. Exportação completa e restauração manual por arquivo próprio, substituindo após validação e confirmação; preservar dados anteriores em cancelamento ou falha. Sem backup automático. | RF-08, RF-09, RN-09, RN-12 a RN-14, RNF-01, RNF-03 |
| L-06 | Sorteio. | Chances iguais em sorteios independentes, com repetição permitida. | RN-05, CA-15 |
| L-07 | Restrições e acessibilidade. | Projeto de estudo sem prazo fixo, microtarefas conforme disponibilidade e sem custos recorrentes obrigatórios. Chrome e Firefox estáveis atuais no computador do usuário. Teclado, foco visível, rótulos, contraste legível e mensagens independentes de cor. | Seção 2, RNF-06 a RNF-08, CA-32, CA-33 |
| L-08 | Idioma e mensagens. | Português brasileiro, com indicação do campo que precisa de correção. | RNF-05, CA-24, CA-25 |

Tecnologia, local de armazenamento e formato técnico do arquivo de recuperação ficam para o projeto da solução. A escolha deverá atender a estes requisitos sem ampliar o escopo. Não há funcionalidades pendentes de aprovação nesta revisão.

## 10. Validação do produto e definição de pronto

### Validação da utilidade — confirmada, a realizar

Usar uma coleção de 20 álbuns reais, com diferentes artistas e situações, durante uma semana. Observar se o usuário consegue:

1. Reencontrar um álbum por artista ou trecho do título.
2. Consultar apenas os álbuns que quer ouvir.
3. Sortear uma opção dentro do conjunto desejado.
4. Atualizar a situação e reencontrar o álbum depois de reabrir a aplicação.

Registrar dificuldades e exemplos em que foi necessário voltar à organização anterior. A amostra e a duração foram aprovadas para avaliar a utilidade; não são limites do produto nem metas de velocidade. A verificação técnica deve usar também uma coleção de 10.000 álbuns. Cumprir os critérios funcionais não comprova, por si só, a utilidade da biblioteca.

### Pronto para orientar a implementação

- O usuário revisou e aprovou as propostas que afetam o comportamento do MVP; as decisões estão incorporadas neste documento.
- As lacunas L-01 a L-08 foram resolvidas, sem escolher tecnologias por este documento.
- Os exemplos dos critérios orientam os casos de teste. A coleção de 20 álbuns reais deverá ser reunida para a avaliação de utilidade.

### Pronto para considerar o MVP implementado — verificação futura

- Todos os requisitos confirmados e derivados possuem evidência de atendimento aos critérios aplicáveis.
- Foram verificados persistência após reabertura, limites e entradas inválidas, conjuntos vazios, filtros combinados, elegibilidade do sorteio e preservação dos dados nas falhas previstas.
- Foram verificadas exportação completa e restauração com confirmação, cancelamento, arquivo inválido e falha de gravação, preservando os dados anteriores quando aplicável.
- Foram verificados capacidade com 10.000 álbuns e fluxos por teclado, rótulos, foco, contraste e mensagens independentes de cor em Chrome e Firefox nos ambientes registrados na verificação.
- O uso do MVP atende à restrição de ausência de custos recorrentes obrigatórios.
- Os resultados da verificação e eventuais limitações foram registrados sem afirmar ausência de bugs.
- O usuário realizou uma avaliação de uso e registrou se a biblioteca ajuda nos dois problemas definidos.
- Funcionalidades fora do escopo não são exigidas para concluir o MVP.

## 11. Estado desta entrega e próxima ação

Esta entrega é uma revisão documental. As lacunas L-01 a L-08 foram resolvidas, as propostas revisadas foram confirmadas e o escopo passou a incluir exportação e restauração manual. Não houve implementação da aplicação nem execução de testes de funcionalidades. A avaliação de utilidade e a verificação técnica continuam pendentes.

**Próxima ação do usuário:** escolher a próxima etapa de projeto da solução e planejamento das microtarefas. Reunir os 20 álbuns reais antes da avaliação de utilidade.

**Revisão ativa:** por que a amostra de 20 álbuns durante uma semana avalia a utilidade, enquanto o cenário com 10.000 álbuns verifica a capacidade? E por que a restauração precisa validar todo o arquivo antes de substituir a coleção?
