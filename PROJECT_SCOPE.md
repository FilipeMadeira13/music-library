# Music Library — Escopo do projeto

Status: aprovado pelo proprietário do projeto.

## 1. Problema

Organizar uma biblioteca pessoal de álbuns e escolher o que ouvir exige uma experiência que reúna navegação por artista, seleção intencional e acesso aos serviços de streaming escolhidos pelo usuário.

O projeto centralizará essa organização e oferecerá sorteio de álbuns para facilitar decisões e redescobertas dentro da própria coleção.

## 2. Público e necessidades

A primeira versão atenderá exclusivamente ao proprietário da biblioteca, que deseja:

- Manter uma coleção pessoal de álbuns.
- Navegar por artista e pesquisar na coleção.
- Acessar a mesma biblioteca em vários dispositivos.
- Escolher os serviços de streaming utilizados.
- Sortear um álbum para ouvir.

O projeto também tem finalidade educacional: será desenvolvido em etapas pequenas, priorizando compreensão e autonomia.

## 3. Objetivos e restrições

- Entregar uma biblioteca pessoal funcional e acessível em vários dispositivos.
- Validar a utilidade da organização e do sorteio no uso cotidiano.
- Priorizar aprendizado, sem prazo fixo.
- Trabalhar com orçamento zero, sem contratar serviços pagos.
- Não definir tecnologias antes de avaliar requisitos e alternativas.

## 4. MVP — funcionalidades essenciais

MVP é a menor versão que permite testar se o produto resolve o problema.

| ID | Requisito funcional |
|---|---|
| RF01 | Buscar álbuns em um catálogo externo e adicioná-los à biblioteca |
| RF02 | Cadastrar manualmente álbuns não encontrados no catálogo |
| RF03 | Consultar, editar e remover álbuns da biblioteca |
| RF04 | Organizar os álbuns por artista, incluindo “Vários artistas” |
| RF05 | Pesquisar na biblioteca por título ou artista |
| RF06 | Cadastrar os serviços de streaming desejados |
| RF07 | Associar manualmente links de streaming aos álbuns e abrir esses destinos |
| RF08 | Sortear um álbum da biblioteca |
| RF09 | Persistir a coleção e disponibilizar os mesmos dados em vários dispositivos |
| RF10 | Restringir a consulta e a alteração da biblioteca ao proprietário |

O cadastro manual terá título e artista obrigatórios. Links serão opcionais. Outros metadados dependerão da avaliação do catálogo e da necessidade real de uso.

## 5. Regras de negócio

- A biblioteca contém apenas álbuns adicionados pelo usuário.
- Ouvir um álbum não altera seu estado nem o remove.
- Edições padrão, deluxe e remasterizadas contam como o mesmo álbum.
- Links para diferentes edições podem pertencer à mesma entrada.
- A inclusão de uma edição equivalente não deve gerar duplicata após confirmação do usuário.
- Coletâneas podem ser agrupadas em “Vários artistas”.
- Todos os álbuns têm a mesma chance no sorteio.
- Resultados consecutivos podem se repetir.
- A ausência de links não impede cadastrar ou sortear um álbum.
- A aplicação abre serviços externos; não reproduz música.

## 6. Requisitos de qualidade

- Interface utilizável em computador e celular.
- Operações principais acessíveis por teclado, com campos identificados.
- Dados preservados entre sessões e disponíveis nos dispositivos utilizados.
- Mensagens claras para falhas de catálogo, salvamento e carregamento.
- Nenhuma confirmação de salvamento quando a operação falhar.
- Acesso à biblioteca protegido contra terceiros.
- Alterações simultâneas não devem sobrescrever dados silenciosamente; o comportamento será definido no desenho técnico.

## 7. Critérios de aceitação

| Cenário | Resultado esperado |
|---|---|
| Dado um resultado de catálogo, quando adicionado | O álbum aparece no agrupamento correspondente |
| Dada uma busca sem resultado ou com falha | O cadastro manual permanece disponível |
| Dados título e artista válidos, quando cadastrados manualmente | O álbum é salvo |
| Dada uma edição confirmada como equivalente | Ela não cria uma segunda entrada na biblioteca |
| Dado um link válido associado a um serviço, quando selecionado | O destino externo é aberto |
| Dada uma biblioteca não vazia, quando solicitado o sorteio | Um álbum pertencente à biblioteca é apresentado |
| Dada uma biblioteca vazia, quando solicitado o sorteio | A interface orienta a adicionar um álbum |
| Dada uma alteração salva em um dispositivo, quando a biblioteca é carregada em outro | A alteração está disponível |
| Dada uma tentativa de acesso sem autorização | A biblioteca não é exibida nem alterada |

## 8. Fora do MVP

Importação e sincronização com bibliotecas de streaming, descoberta automática de links, reprodução de áudio, histórico de audição, recomendações externas, etiquetas, múltiplas coleções, compartilhamento, cadastro público e funcionamento sem internet.

Exportação e recuperação de dados serão avaliadas como próximas melhorias.

## 9. Riscos, dependências e limitações

| Ponto | Impacto |
|---|---|
| Catálogo externo | Disponibilidade, condições de uso, limites e cobertura precisam ser verificados |
| Orçamento zero | Pode limitar hospedagem, armazenamento e integrações |
| Edições equivalentes | Metadados podem exigir confirmação e correção manual |
| Links manuais | Exigem manutenção pelo usuário e podem deixar de funcionar |
| Uso em vários dispositivos | Exige armazenamento compartilhado e controle de acesso |
| Dependência de rede | O MVP não garante funcionamento sem conexão |
| Perda de dados | Estratégia de recuperação precisa ser avaliada antes do uso definitivo |

Nenhum catálogo, serviço de hospedagem ou mecanismo de autenticação foi escolhido ou validado nesta etapa.

## 10. Objetivos mensuráveis

Metas iniciais propostas:

- Organizar uma biblioteca piloto de 30 álbuns, incluindo coletâneas e edições equivalentes.
- Encontrar um álbum conhecido em até 15 segundos.
- Adicionar um álbum encontrado no catálogo em até um minuto, em condições normais de conexão.
- Confirmar acesso à mesma coleção em dois dispositivos.
- Utilizar o sorteio para escolher pelo menos três audições em duas semanas.
- Ao concluir cada etapa, explicar a decisão técnica e demonstrar o comportamento implementado.
