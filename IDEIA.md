# Music Library — definição inicial

Documento de descoberta do projeto, consolidado em 29/10/2026. Não define tecnologias nem autoriza implementação.

## Contexto e motivação

O projeto será uma biblioteca musical pessoal, organizada principalmente por artista. A proposta combina o interesse do autor por música e descoberta de álbuns com aprendizado prático de desenvolvimento backend e construção de portfólio para o primeiro emprego.

Disponibilidade estimada: 10 horas semanais, sem prazo pessoal definido. O desenvolvimento deve acontecer em pequenas etapas, com foco em aprendizado e autonomia.

Atualmente, o autor descobre álbuns no Rate Your Music (RYM), usando um custom chart com os melhores álbuns de todos os tempos segundo seus 50 usuários mais compatíveis. Ouve os álbuns no streaming e não mantém uma lista própria dos que pretende ouvir.

Não foi identificada uma dificuldade concreta para escolher álbuns no chart atual. A motivação do projeto é ter uma biblioteca própria bem organizada, com sorteio, avaliações e links para audição.

## Proposta

Uma biblioteca pessoal de álbuns que permita:

- Organizar os álbuns adicionados por artista e tipo de lançamento.
- Buscar e filtrar a coleção por gênero e ano.
- Sortear um álbum para ouvir.
- Registrar se um álbum foi ouvido e uma avaliação opcional.
- Acessar os álbuns nos serviços de streaming por links cadastrados.

O usuário inicial é o próprio autor. Uma experiência para múltiplos usuários não foi definida.

## Organização e navegação

A referência de organização por artista é a experiência imaginada a partir do Apple Music, sem compromisso de reproduzir sua interface.

Fluxo principal:

**Biblioteca → Artista → Álbuns agrupados por tipo → Detalhes do álbum**

### Exemplo: Iron Maiden

Ao entrar na página do Iron Maiden, os álbuns adicionados aparecem separados em grupos como:

- Estúdio.
- Ao vivo.
- Coletâneas.
- Outros tipos pertinentes, como EPs.

Filtros por gênero e ano ajudam a explorar a coleção.

**A página do artista exibe somente os álbuns adicionados à biblioteca, não sua discografia completa.**

Tipo de lançamento e gênero musical são conceitos diferentes. Um álbum poderá ter mais de um gênero. A lista definitiva de tipos ainda será detalhada.

## Primeira versão utilizável (MVP)

MVP significa a menor versão que já permite experimentar a proposta na prática.

| Parte | Comportamento proposto |
| --- | --- |
| Cadastro | Cadastrar artistas e álbuns manualmente. |
| Biblioteca | Navegar pelos artistas e pelos álbuns adicionados. |
| Página do artista | Agrupar os álbuns por tipo de lançamento. |
| Busca e filtros | Buscar artistas e álbuns por nome e filtrar álbuns por gênero e ano. |
| Audições | Marcar álbuns como ouvidos. |
| Avaliações | Registrar nota e comentário opcionais. |
| Sorteio | Sortear um álbum entre os que atendem aos filtros selecionados. |
| Streaming | Guardar e abrir links cadastrados para os serviços de streaming. |

O objetivo inicial é organizar uma parte da coleção pessoal e usar a biblioteca para apoiar e registrar audições.

## Regras e princípios já identificados

- Cada artista apresenta somente os álbuns adicionados pelo usuário.
- Os álbuns são agrupados por tipo de lançamento na página do artista.
- Gênero e ano complementam a navegação como filtros.
- O sorteio respeita os filtros selecionados.
- Um álbum sem avaliação não equivale a um álbum de que o usuário não gostou.
- Nota e comentário são opcionais.
- Os links levam aos serviços externos de streaming; reprodução dentro do aplicativo não faz parte do escopo inicial.

## Evoluções a investigar

- Buscar e importar informações de artistas e álbuns de uma fonte externa.
- Descobrir novos álbuns usando as avaliações como um dos sinais de preferência.
- Usar a situação de audição como filtro, por exemplo para sortear apenas álbuns ainda não ouvidos.

Para encontrar álbuns fora da biblioteca, será necessário investigar uma fonte externa de candidatos. Nenhuma integração, disponibilidade de API ou viabilidade técnica foi verificada nesta etapa. A primeira versão não depende de importar o chart do RYM.

## Fora do escopo inicial

- Recomendações automáticas de novos álbuns.
- Importação automática de informações ou de discografias completas.
- Integração com o chart do Rate Your Music.
- Reprodução de música dentro do aplicativo.
- Coleções temáticas como eixo principal de organização.

## Aprendizado e portfólio

O foco profissional é desenvolvimento backend. O projeto oferece oportunidades para praticar:

- Modelagem de dados: relações entre artistas, álbuns, gêneros e avaliações.
- Consultas com busca e combinação de filtros.
- Validação de regras de negócio.
- Sorteio aplicado a uma seleção de dados.
- Testes de comportamentos reais.
- Integrações externas em uma etapa posterior, caso sejam úteis e viáveis.

Tecnologias, arquitetura e estrutura de arquivos ainda não foram escolhidas.

## Decisões pendentes

- Evoluir o Music Library existente ou iniciar uma nova versão, após comparar o código atual com esta proposta.
- Escolher qual função justifica o primeiro uso e será a primeira pequena entrega.
- Definir a escala de notas.
- Detalhar como representar os estados de audição.
- Definir campos obrigatórios do cadastro e tratamento de duplicatas.
- Detalhar os filtros, a ordenação e o comportamento do sorteio quando não houver resultados.
- Definir os serviços de streaming desejados e como cadastrar seus links.
- Refinar requisitos e critérios de aceitação antes de implementar.

## Forma de trabalho

- Mentoria em português brasileiro, com explicação breve dos termos técnicos.
- Microtarefas e dicas progressivas; o autor escreve testes e implementação.
- Preferência por TDD (escrever um teste que falha, implementar o necessário para passar e depois melhorar a organização) quando adequado.
- Uma etapa por vez, com evidências antes de avançar.
- Não reestruturar o projeto nem alterar arquivos fora do escopo sem autorização.

## Próximo passo

Comparar esta proposta com o Music Library existente e decidir se ele será evoluído ou se haverá uma nova versão. Em seguida, escolher a primeira pequena entrega com base no uso pessoal esperado.
