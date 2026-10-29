# Music Library — requisitos e critérios de aceitação

Data: 29/10/2026. Fonte: [IDEIA.md](IDEIA.md) e decisões tomadas na análise de requisitos com o autor.

Este documento especifica a primeira versão utilizável (MVP) de uma biblioteca musical pessoal. Não escolhe tecnologias, arquitetura ou contratos de API e não autoriza implementação de funcionalidades.

## 1. Objetivo, público e limites

Permitir que o autor organize sua coleção por artista, encontre e sorteie álbuns, registre audições e avaliações e abra links de streaming. O projeto também apoia aprendizado prático de backend e portfólio, com disponibilidade estimada de 10 horas semanais e sem prazo definido.

Fluxo principal: **Biblioteca → Artista → Álbuns agrupados por tipo → Detalhes do álbum**.

O MVP inclui cadastro manual, edição, exclusão, busca, filtros por gênero e ano, estado de audição, avaliação única e sorteio. A biblioteca contém apenas registros adicionados pelo usuário.

Ficam fora do MVP: múltiplos usuários, histórico de audições, filtro por estado de audição, recomendações automáticas, importação de metadados ou discografias, integração com o RYM, reprodução interna e coleções temáticas como eixo de organização. Autenticação e publicação ainda não foram definidas.

## 2. Dados e vocabulário

| Conceito | Dados e significado |
| --- | --- |
| Artista | Nome obrigatório. Pode existir sem álbuns. |
| Álbum | Título, um artista existente, ano e um tipo de lançamento obrigatórios; zero ou mais gêneros e links. Inclui EPs para fins de organização. |
| Tipo de lançamento | Categoria do lançamento, diferente de gênero musical. Lista inicial: Estúdio, Ao vivo, Coletânea, EP e Outros. |
| Gênero | Classificação musical cadastrada manualmente junto ao álbum; vários gêneros podem coexistir. Não há integração ou taxonomia externa obrigatória. |
| Audição | Estado atual: não ouvido ou ouvido. Um novo álbum começa como não ouvido. |
| Avaliação | Uma nota e um comentário opcionais por álbum ouvido. Pode conter só nota, só comentário ou ambos. Ausência de ambos significa sem avaliação. |
| Link | Nome livre do serviço e endereço HTTP/HTTPS; no máximo um link por serviço por álbum. |

## 3. Requisitos funcionais (RF)

| ID | Requisito | Aceitação |
| --- | --- | --- |
| RF-01 | Cadastrar e editar artistas manualmente. | CA-01, CA-03 |
| RF-02 | Cadastrar e editar álbuns, incluindo artista, ano, tipo e gêneros. | CA-02, CA-03 |
| RF-03 | Listar artistas e permitir acessar seus álbuns agrupados por tipo e os detalhes de cada álbum. | CA-04 |
| RF-04 | Buscar artistas por nome e álbuns por título. | CA-05 |
| RF-05 | Filtrar álbuns por um gênero e um ano exatos, combinados com a busca. | CA-06 |
| RF-06 | Marcar e desmarcar álbuns como ouvidos. | CA-07, CA-09 |
| RF-07 | Registrar, editar e remover nota e comentário opcionais em uma avaliação única. | CA-08, CA-09 |
| RF-08 | Sortear um álbum entre os resultados da seleção atual. | CA-10 |
| RF-09 | Cadastrar, editar, remover e abrir links de streaming do álbum. | CA-11 |
| RF-10 | Excluir álbuns e artistas mediante confirmação, com remoção dos dados dependentes. | CA-12, CA-13 |

## 4. Regras de negócio (RN)

| ID | Regra |
| --- | --- |
| RN-01 | Comparações de duplicatas desconsideram maiúsculas/minúsculas, espaços nas extremidades e sequências de espaços. Acentos e pontuação não são removidos; nomes parecidos não são unificados automaticamente. |
| RN-02 | Não pode haver dois artistas com nomes equivalentes conforme RN-01. Homônimos distintos não são representados separadamente neste MVP. |
| RN-03 | Não pode haver dois álbuns com título equivalente, mesmo artista e mesmo ano. Mesmo título em outro artista ou ano é permitido. Edições distintas com essa mesma combinação não são diferenciadas. |
| RN-04 | Campos obrigatórios não podem estar vazios nem conter somente espaços. Ano deve ser inteiro entre 1 e 9999, inclusive; anos futuros são permitidos. O tipo deve pertencer à lista inicial. |
| RN-05 | Cada álbum pertence a exatamente um artista. Edição pode trocar o artista, desde que o destino exista e não gere duplicata. Alterar o nome do artista mantém seus vínculos com álbuns. |
| RN-06 | Um álbum pode ter vários gêneros. Rótulos vazios não são aceitos; gêneros equivalentes pela RN-01 não se repetem no mesmo álbum. |
| RN-07 | A página do artista mostra somente seus álbuns cadastrados, agrupados por tipo. Não busca nem pressupõe uma discografia completa. |
| RN-08 | Busca usa trecho do nome do artista ou título do álbum, conforme a listagem, sem diferenciar maiúsculas/minúsculas. Busca vazia não restringe resultados. |
| RN-09 | Filtros de gênero e ano são opcionais e se combinam com a busca por interseção: todos os critérios ativos devem ser atendidos. Gênero corresponde a um dos gêneros do álbum; ano corresponde ao valor exato. |
| RN-10 | A seleção de álbuns considera também o artista atual quando iniciada na página dele. Os filtros de álbuns não ocultam artistas da listagem geral. Limpar busca e filtros remove essas restrições, preservando o contexto do artista quando houver. |
| RN-11 | Artistas e títulos são ordenados alfabeticamente por padrão, sem diferenciar maiúsculas/minúsculas; empates entre títulos usam ano crescente. Não há ordenação personalizada no MVP. |
| RN-12 | Apenas álbuns ouvidos podem receber nota ou comentário. Estar ouvido não exige avaliação. A nota admite 0; 0,5; 1; 1,5; 2; 2,5; 3; 3,5; 4; 4,5; 5. Ausência de nota é diferente de zero. |
| RN-13 | Ao desmarcar como ouvido um álbum com nota ou comentário, informar que ambos serão apagados e pedir confirmação. Confirmar altera o estado e remove a avaliação; cancelar preserva tudo. Sem avaliação, a mudança é direta. |
| RN-14 | Cada álbum da seleção atual tem a mesma probabilidade de ser sorteado, independentemente de quantidade de gêneros, nota ou audição. Cada sorteio pode repetir resultados anteriores. Sortear não altera estado de audição nem avaliação. |
| RN-15 | Sem candidatos, informar que nenhum álbum atende à seleção e não retornar um álbum fora dela. Um único candidato sempre será o resultado. |
| RN-16 | Links exigem nome de serviço não vazio e URL absoluta HTTP/HTTPS com domínio ou host. Serviços equivalentes pela RN-01 não se repetem no álbum. Validar formato não significa verificar disponibilidade ou conteúdo do destino. |
| RN-17 | Antes de excluir um álbum, informar que avaliação e links também serão removidos. Antes de excluir um artista, informar quais álbuns serão afetados ou sua quantidade e que avaliações e links serão removidos. Cancelar preserva todos os dados. |
| RN-18 | Confirmar a exclusão de um álbum remove o álbum e seus dados dependentes. Confirmar a exclusão de um artista remove o artista e todos os seus álbuns com avaliações e links. Gêneros em outros álbuns e outros artistas não são afetados. Não há restauração prevista no MVP. |

## 5. Requisitos não funcionais (RNF)

| ID | Requisito verificável |
| --- | --- |
| RNF-01 | Persistir cadastros, alterações, estados e avaliações entre encerramento e reinício normal da aplicação. Verificação: CA-14. |
| RNF-02 | Rejeitar dados inválidos com mensagem que identifique o problema e permita correção; não apresentar sucesso quando a operação falhar. Verificação: CA-01 a CA-03, CA-08, CA-11 e CA-15. |
| RNF-03 | Manter consistência nas operações: exclusões e mudanças relacionadas devem ser concluídas integralmente ou preservar o estado anterior. Não deixar álbuns sem artista nem avaliações e links sem álbum. Verificação: CA-09, CA-12, CA-13 e CA-15. |
| RNF-04 | Preservar unicidade mesmo diante de solicitações simultâneas de cadastro ou edição. Verificação: CA-16. |
| RNF-05 | Tornar observáveis os comportamentos de validação, filtros, avaliação e sorteio para que possam ser verificados por testes. A escolha de ferramentas fica para a implementação. Verificação: cenários desta seção de aceitação. |

Não há metas numéricas de desempenho, disponibilidade ou capacidade aprovadas. Volume de dados, ambiente de execução, autenticação, acesso remoto e política de backup deverão ser definidos antes de qualquer publicação. Não se presume que um uso pessoal autorize exposição pública sem controle de acesso.

## 6. Critérios de aceitação

Os cenários descrevem comportamentos esperados; não representam testes já implementados ou executados.

### CA-01 — Cadastro de artista (RF-01)

- **Dado** um nome válido e ainda não cadastrado, **quando** cadastrar o artista, **então** ele aparece na biblioteca e pode ser acessado mesmo sem álbuns.
- **Dado** um nome vazio ou somente espaços, **quando** tentar cadastrar ou editar, **então** a operação é rejeitada com explicação e nenhum registro é alterado.

### CA-02 — Cadastro e edição de álbum (RF-02)

- **Dado** um artista existente e título, ano e tipo válidos, **quando** cadastrar um álbum sem gêneros, links ou avaliação, **então** ele é salvo como não ouvido e aparece no artista informado.
- **Dado** um campo obrigatório ausente, artista inexistente, ano fracionado ou fora de 1 a 9999 ou tipo desconhecido, **quando** salvar, **então** a operação é rejeitada sem alteração parcial.
- **Dado** um álbum existente, **quando** editar seus dados válidos ou transferi-lo para outro artista existente, **então** os detalhes e agrupamentos refletem a alteração, preservando audição, avaliação e links não alterados.
- **Dado** um álbum com vários gêneros válidos, **quando** salvar, **então** todos ficam associados a ele sem repetições equivalentes; gênero vazio é rejeitado.

### CA-03 — Duplicatas e conflitos de edição (RF-01, RF-02)

- **Dado** o artista `Iron Maiden`, **quando** tentar cadastrar ` iron   maiden `, **então** o cadastro é rejeitado como duplicata.
- **Dado** um álbum cadastrado, **quando** outro cadastro ou edição produzir o mesmo título normalizado, artista e ano, **então** a operação é rejeitada e os dados anteriores são preservados.
- **Dado** o mesmo título em outro artista ou ano, **quando** cadastrar, **então** a diferença permite o registro.
- **Dado** um artista existente, **quando** renomeá-lo para um nome válido e único, **então** seus álbuns permanecem vinculados; renomeá-lo para um nome já utilizado é rejeitado.

### CA-04 — Biblioteca e navegação (RF-03)

- **Dado** uma biblioteca vazia, **quando** abri-la, **então** é informado que não há artistas cadastrados.
- **Dado** um artista sem álbuns, **quando** acessá-lo, **então** é informado que ele não tem álbuns cadastrados.
- **Dado** um artista com álbuns de estúdio e ao vivo cadastrados, **quando** acessá-lo, **então** eles aparecem nos grupos correspondentes, sem incluir lançamentos não cadastrados.
- **Dado** uma listagem com vários artistas ou títulos, **quando** consultá-la, **então** a ordem segue RN-11 e cada álbum permite acessar seus detalhes.

### CA-05 — Busca (RF-04)

- **Dado** `Iron Maiden` cadastrado, **quando** buscar artistas por `MAID`, **então** esse artista é encontrado.
- **Dado** um título de álbum cadastrado, **quando** buscar álbuns por um trecho do título em outra capitalização, **então** o álbum é encontrado.
- **Dado** uma busca sem correspondências, **quando** consultar, **então** é exibido um estado vazio; **quando** limpar a busca, **então** ela deixa de restringir os resultados.

### CA-06 — Combinação de filtros (RF-05)

- **Dado** um álbum com os gêneros Heavy Metal e Hard Rock lançado em 1982, **quando** filtrar por Heavy Metal e 1982, **então** ele aparece uma única vez.
- **Dado** busca, gênero e ano ativos, **quando** consultar, **então** aparecem apenas álbuns que atendem a todos os critérios e ao artista atual, se houver.
- **Dado** filtros sem correspondências, **quando** consultar, **então** é informado que não há resultados; limpar os filtros recupera os álbuns do contexto atual sem modificar cadastros.

### CA-07 — Estado de audição (RF-06)

- **Dado** um álbum não ouvido, **quando** marcá-lo como ouvido sem preencher avaliação, **então** o estado é salvo e ele continua sem nota e comentário.
- **Dado** um álbum ouvido sem avaliação, **quando** desmarcá-lo, **então** ele passa a não ouvido.
- **Dado** um álbum já no estado solicitado, **quando** repetir a ação, **então** o estado permanece e não é criado histórico de audições.

### CA-08 — Avaliação opcional e escala (RF-07)

- **Dado** um álbum ouvido, **quando** salvar apenas nota, apenas comentário ou ambos, **então** os campos informados são persistidos em sua única avaliação.
- **Dado** um álbum ouvido, **quando** salvar nota 0, 0,5 ou 5, **então** ela é aceita; **quando** informar -0,5, 5,5, 3,2 ou valor não numérico, **então** a operação é rejeitada.
- **Dado** um álbum não ouvido, **quando** tentar salvar nota ou comentário, **então** a operação é rejeitada e informa que é necessário marcá-lo como ouvido.
- **Dado** um álbum avaliado, **quando** editar a nota ou comentário, **então** a avaliação existente é atualizada; **quando** remover ambos, **então** fica sem avaliação e continua ouvido.
- **Dado** um comentário vazio ou apenas espaços, **quando** salvar, **então** ele é tratado como ausente. Uma nota ausente é exibida como sem nota, nunca como zero.

### CA-09 — Desmarcação com avaliação (RF-06, RF-07)

- **Dado** um álbum ouvido com nota ou comentário, **quando** solicitar marcar como não ouvido, **então** é solicitada confirmação com aviso de remoção de ambos.
- **Dado** essa confirmação, **quando** cancelar, **então** audição e avaliação são preservadas; **quando** confirmar, **então** o álbum passa a não ouvido e sua nota e comentário são removidos juntos.

### CA-10 — Sorteio (RF-08)

- **Dado** uma seleção não vazia, **quando** sortear, **então** o resultado pertence à seleção atual, considerando busca, filtros e contexto do artista.
- **Dado** exatamente um candidato, **quando** sortear várias vezes, **então** ele é sempre retornado; repetição não é tratada como erro.
- **Dado** zero candidatos, **quando** sortear, **então** é informado que não há álbuns elegíveis e nenhum álbum externo à seleção é retornado.
- **Dado** vários candidatos, inclusive álbuns com vários gêneros ou avaliações diferentes, **quando** verificar a regra de seleção, **então** cada álbum participa uma única vez e tem a mesma probabilidade. A verificação não exige frequências exatamente iguais em uma amostra aleatória finita.
- **Dado** qualquer resultado, **quando** concluir o sorteio, **então** audição e avaliação não mudam.

### CA-11 — Links de streaming (RF-09)

- **Dado** um álbum, serviço com nome válido e URL absoluta HTTP/HTTPS, **quando** salvar o link, **então** ele pode ser consultado e aberto no serviço externo.
- **Dado** um link para Spotify, **quando** cadastrar outro para ` spotify ` no mesmo álbum, **então** a duplicata é rejeitada; cadastrar outro serviço é permitido.
- **Dado** nome vazio, URL sem host ou esquema diferente de HTTP/HTTPS, **quando** salvar, **então** a operação é rejeitada.
- **Dado** um link cadastrado, **quando** editar ou remover, **então** a mudança é persistida sem afetar o álbum ou outros links; edição que conflite com outro serviço é rejeitada.
- **Dado** um endereço com formato válido cujo destino está indisponível, **quando** consultar o álbum, **então** o cadastro continua disponível; a aplicação não promete disponibilidade do serviço externo nem reprodução interna.

### CA-12 — Exclusão de álbum (RF-10)

- **Dado** um álbum com avaliação e links, **quando** solicitar exclusão, **então** é informado o impacto e solicitada confirmação.
- **Dado** a confirmação, **quando** cancelar, **então** todos os dados permanecem; **quando** confirmar, **então** álbum, avaliação e links são removidos, sem excluir seu artista nem outros álbuns.

### CA-13 — Exclusão de artista (RF-10)

- **Dado** um artista com vários álbuns, **quando** solicitar exclusão, **então** a confirmação explicita os álbuns afetados ou sua quantidade e a remoção de avaliações e links.
- **Dado** a confirmação, **quando** cancelar, **então** todos os dados permanecem; **quando** confirmar, **então** artista, seus álbuns e dados dependentes são removidos integralmente, sem afetar outros artistas.
- **Dado** um artista sem álbuns, **quando** confirmar sua exclusão, **então** apenas o artista é removido.

### CA-14 — Persistência (RNF-01)

- **Dado** operações de cadastro, edição, audição, avaliação ou exclusão concluídas com sucesso, **quando** encerrar e reiniciar normalmente a aplicação, **então** o estado resultante é mantido, inclusive a ausência dos registros excluídos.

### CA-15 — Falhas e referências desatualizadas (RNF-02, RNF-03)

- **Dado** uma falha ao salvar ou excluir, **quando** a operação não puder ser concluída integralmente, **então** o estado anterior é preservado e a falha é informada sem mensagem de sucesso.
- **Dado** um artista ou álbum já removido, **quando** tentar consultá-lo ou alterá-lo por uma referência antiga, **então** é informado que ele não existe, sem recriação automática ou alteração de outro registro.
- **Dado** exclusão de artista ou desmarcação com limpeza de avaliação, **quando** ocorrer falha em uma parte da operação, **então** nenhuma parte é confirmada isoladamente.

### CA-16 — Cadastros simultâneos (RNF-04)

- **Dado** duas solicitações simultâneas que criariam artistas ou álbuns duplicados, **quando** forem processadas, **então** no máximo um registro é criado e o conflito é informado na outra solicitação.
- **Dado** edições simultâneas que produziriam a mesma identificação de artista ou álbum, **quando** forem processadas, **então** a unicidade é preservada e a edição conflitante é rejeitada.

## 7. Origem das decisões e premissas adotadas

### Confirmado pelo autor nesta análise

- Fechar as principais lacunas agora, em vez de apenas registrá-las como pendências.
- Cadastro enxuto, com um artista por álbum e bloqueio de duplicatas por nome do artista ou título/artista/ano.
- Estado ouvido/não ouvido e avaliação única, disponível apenas para álbuns ouvidos.
- Notas de 0 a 5 em passos de 0,5; nota e comentário opcionais.
- Filtro por um gênero e um ano exatos, combinado com busca; sorteio uniforme com repetições permitidas e aviso para seleção vazia.
- Edição e exclusão no MVP; excluir artista remove seus álbuns e dados dependentes após confirmação.
- Desmarcar álbum avaliado exige confirmação e limpa nota e comentário.
- Nome de serviço e URL livres, com um link por serviço em cada álbum.

### Premissas propostas no plano aprovado

- Lista inicial de tipos, intervalo de anos e ordenação padrão descritos neste documento.
- Busca parcial sem distinção de maiúsculas/minúsculas e normalização de espaços para duplicatas.
- Gêneros informados manualmente; não exigir taxonomia externa ou limite arbitrário de tamanho da coleção.
- Uso inicial por uma pessoa. Nenhuma infraestrutura, interface gráfica ou mecanismo de autenticação foi escolhido.

### Convenções mínimas para tornar os critérios verificáveis

- Comentário vazio equivale a ausente; não remover acentos ou pontuação na identificação de duplicatas.
- Não repetir um gênero equivalente no mesmo álbum; não multiplicar a chance de um álbum por seus gêneros.
- Filtros e sorteio na página do artista permanecem limitados àquele artista.
- Alterações válidas preservam dados não alterados; falhas não deixam operações parciais.

Essas convenções detalham o comportamento documental e devem ser revistas caso o uso pessoal demonstre outra necessidade. Nenhuma delas constitui escolha de tecnologia.

## 8. Pendências e definição de pronto

### Pendências para etapas futuras

- Comparar esta proposta com o Music Library anterior e decidir entre evolução e nova versão. Nesta pasta, durante a análise, foi encontrado somente `IDEIA.md`, sem código ou repositório Git disponível para comparação.
- Escolher a primeira pequena entrega; este documento especifica o MVP completo, sem exigir implementá-lo de uma vez.
- Definir tecnologias, arquitetura, interface e ambiente de execução.
- Antes de publicação, definir autenticação, permissões, exposição dos dados, backup e metas operacionais.
- Revisitar homônimos, edições, colaborações entre artistas, histórico de audições e filtro por audição somente se forem incorporados a uma etapa posterior.

### Pronto para concluir a especificação

- Cada funcionalidade possui identificação, regras e critérios observáveis.
- Decisões confirmadas, premissas e pendências estão diferenciadas.
- Casos inválidos, duplicatas, seleção vazia, exclusões, falhas e concorrência relevante estão documentados.
- O documento permanece independente de tecnologias e não amplia o MVP com integrações externas.

### Pronto para aceitar uma futura entrega implementada

- Os critérios correspondentes à pequena entrega escolhida são demonstrados com evidências e testes adequados.
- Validações, persistência e integridade aplicáveis à entrega são verificadas, incluindo falhas relevantes.
- Nenhum critério pendente é apresentado como concluído; limitações são registradas.
- O autor escreve testes e implementação com mentoria, preferindo o ciclo TDD: teste que falha, implementação mínima e melhoria da organização.

### Revisão ativa de aprendizado

Ao revisar este documento, explique com suas palavras: qual é a diferença entre o requisito de sortear um álbum, a regra de respeitar os filtros e um cenário que comprova essa regra? Essa revisão não condiciona a entrega documental.
