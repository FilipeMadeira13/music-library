# Music Library — Especificação de requisitos

**Status:** aprovada pelo proprietário como base para avaliação técnica e arquitetura, com as pendências técnicas explícitas da seção 8.
**Fonte:** [PROJECT_SCOPE.md](PROJECT_SCOPE.md), escopo aprovado pelo proprietário, e esclarecimentos posteriores do proprietário sobre versões, serviços e artistas.
**Data:** 22/10/2026.

## 1. Como interpretar este documento

Esta especificação detalha o escopo aprovado sem escolher tecnologias ou fornecedores. Incorpora as regras esclarecidas posteriormente pelo proprietário e identifica a solução para exclusão de serviços cuja escolha ele delegou. Os identificadores RF01–RF10 preservam os do escopo. RN identifica regra de negócio; RNF, requisito não funcional; CA, critério de aceitação; P, decisão pendente.

- **Confirmado:** comportamento expresso no escopo ou nos esclarecimentos do proprietário.
- **Escolha delegada:** solução definida dentro da autorização do proprietário e incluída na aprovação deste documento.
- **Derivado:** condição necessária para cumprir um comportamento do escopo, sem definir sua implementação.
- **Pendente:** decisão ainda não tomada; não autoriza implementação de uma opção presumida.

Os critérios abaixo são verificáveis por observação ou teste. Onde uma decisão pendente afeta o resultado, a aceitação completa depende de resolvê-la. A especificação está completa quanto à cobertura do escopo, mas ainda não está fechada para implementação de todos os detalhes.

## 2. Contexto, ator e limites

O único ator autorizado é o proprietário da biblioteca. Catálogo e serviços de streaming são sistemas externos. Ter vários dispositivos não significa ter vários usuários ou bibliotecas.

O produto permite organizar uma coleção pessoal de álbuns, pesquisar e navegar por artista, manter links manuais e sortear o que ouvir. O orçamento para serviços contratados é zero; não há prazo fixo nem tecnologia aprovada.

Ficam fora do MVP: importação e sincronização com bibliotecas de streaming, descoberta automática de links, reprodução de áudio, histórico de audição, recomendações externas, etiquetas, múltiplas coleções, compartilhamento, cadastro público e funcionamento sem internet. Exportação e recuperação pela interface continuam fora do MVP. Por decisão posterior do proprietário, a proteção operacional deve prever cópias de segurança e restauração por procedimento técnico orientado, conforme seção 7.4. Sua viabilidade gratuita deve ser validada e uma restauração demonstrada antes do uso definitivo.

## 3. Dados, entradas e saídas gerais

| Informação | Entradas e obrigatoriedade | Saídas e restrições |
|---|---|---|
| Álbum | Título, artista e ano original obrigatórios; resultado selecionado no catálogo na inclusão externa | Entrada da biblioteca, consultável, editável e removível; não representa cada edição como álbum distinto |
| Artista ou agrupamento | Artista informado ou obtido do catálogo; possibilidade de “Vários artistas” | Artista principal como agrupamento padrão quando identificado; colaborações podem aparecer sob vários artistas; nomes preservados, sem união automática de homônimos; navegação alfabética e agrupamentos vazios ocultos |
| Edição equivalente | Identificação de possível equivalência e confirmação do proprietário | Uma única entrada com uma versão escolhida por álbum; o proprietário pode trocar essa versão, preservando os links existentes |
| Ano original do álbum | Ano do primeiro lançamento do álbum, distinto do ano da versão escolhida | Campo obrigatório do álbum, consultável e editável; não muda automaticamente ao trocar a versão |
| Ano do lançamento específico | Ano de lançamento da versão escolhida, como uma edição deluxe ou remasterizada | Campo opcional da versão, consultável e editável; pode ficar vazio sem impedir o cadastro |
| Serviço de streaming | Serviço desejado pelo proprietário | Serviço disponível para associação de links, editável e excluível; exclusão remove seus links sem remover álbuns; nome obrigatório e único conforme seção 7.5 |
| Link de streaming | Endereço informado manualmente e serviço associado; opcional para o álbum | Destino externo acionável; múltiplas edições podem ter links na mesma entrada |
| Pesquisa no catálogo | Título do álbum e/ou artista | Resultados, ausência de resultados ou erro identificado |
| Pesquisa na biblioteca | Título ou artista | Álbuns correspondentes ou indicação de ausência de correspondências |
| Sorteio | Solicitação do proprietário | Um álbum existente ou orientação para cadastrar um álbum se a biblioteca estiver vazia |
| Acesso | Evidência de autorização, em formato ainda não escolhido | Acesso concedido ao proprietário ou negado a terceiros |

Os campos de ano original e ano do lançamento específico fazem parte dos requisitos confirmados pelo proprietário. O ano original é obrigatório e o ano do lançamento específico é opcional, conforme decisão do proprietário. As validações dos anos estão aprovadas e descritas na seção 7.1; as validações de título, artista e serviço estão aprovadas na seção 7.5. Capas, gênero, faixas, identificadores externos e outros metadados não são campos obrigatórios aprovados; serão avaliados conforme o catálogo e a necessidade real. Os limites de título, artista e serviço estão na seção 7.5; o volume de produção permanece pendente em P12.

## 4. Requisitos funcionais e critérios de aceitação

### RF01 — Buscar álbuns em catálogo externo e adicioná-los

**Comportamento confirmado:** permitir pesquisar um catálogo externo por título do álbum e/ou artista, selecionar um resultado e adicioná-lo à biblioteca, respeitando as regras de equivalência de edições. Apresentar título, artistas e anos disponíveis, distinguindo ano original e ano da edição. Permitir completar ou corrigir os campos antes de salvar. Importar no MVP apenas título, artistas, ano original e ano da edição quando disponível; capas e outros metadados continuam para avaliação posterior.

**Entrada:** termo de pesquisa e resultado escolhido. **Saída:** resultados de catálogo e, após inclusão bem-sucedida, álbum na biblioteca e no agrupamento correspondente.

**Validações e restrições:** o resultado deve representar um álbum; uma resposta do catálogo não é confirmação de persistência. Campos obrigatórios ausentes devem ser completados pelo proprietário antes da inclusão, respeitando as validações aprovadas das seções 7.1 e 7.5. Não inferir ano original a partir do ano da edição. Permitir carregar mais resultados sem perder a pesquisa atual. Dados importados permanecem editáveis; mudanças posteriores no catálogo não alteram automaticamente os dados salvos. O mapeamento técnico dos campos e limites de consulta será validado com o fornecedor em P08; uma pesquisa sem título nem artista, inclusive com campos compostos apenas por espaços, não deve consultar o catálogo e deve orientar o proprietário a informar título ou artista. A identificação de possíveis duplicatas segue a seção 7.2.

**Erros e extremos:** catálogo indisponível, resposta inválida ou incompleta, limite de consultas, nenhum resultado, nomes homônimos, resultado já adicionado e edição equivalente. Falhas não podem ser apresentadas como busca bem-sucedida sem resultados; cadastro manual permanece disponível.

- **CA01.1:** Dado um resultado válido ainda não pertencente à biblioteca, quando o proprietário o adicionar e a persistência confirmar sucesso, então o álbum poderá ser consultado no agrupamento correspondente.
- **CA01.2:** Dada uma busca sem correspondências, quando terminar, então a interface informará a ausência de resultados e manterá o cadastro manual acessível.
- **CA01.3:** Dada uma falha do catálogo, quando a busca terminar com erro, então a interface identificará a falha e manterá o cadastro manual acessível.
- **CA01.4:** Dada uma edição cuja equivalência foi confirmada pelo proprietário, quando a inclusão for concluída, então não haverá segunda entrada para esse álbum.
- **CA01.5:** Dada uma falha confirmada de salvamento, quando houver tentativa de inclusão, então não será exibida confirmação de álbum salvo.

- **CA01.6:** Dado um resultado sem ano original, quando houver tentativa de inclusão, então o proprietário deverá completar esse campo antes de salvar; o ano da edição não será usado como substituto automático.

- **CA01.7:** Dados critérios de título, artista ou ambos, quando a pesquisa no catálogo for executada, então serão apresentados os resultados correspondentes ou a indicação adequada de ausência/falha, conforme a resposta da integração validada.
- **CA01.8:** Dado um resultado de catálogo, quando apresentado, então serão mostrados título, artistas e anos disponíveis, com identificação distinta para ano original e ano da edição, sem inventar valores ausentes.
- **CA01.9:** Dado um resultado com campos obrigatórios ausentes ou valores a corrigir, quando selecionado para inclusão, então o proprietário poderá preencher ou corrigir os campos antes de salvar; a inclusão exigirá os dados obrigatórios válidos.
- **CA01.10:** Dado um álbum importado, quando o proprietário editar seus dados e salvar, então a alteração válida será persistida; uma mudança posterior no catálogo não substituirá automaticamente os dados da biblioteca.
- **CA01.11:** Dada uma pesquisa com mais resultados disponíveis, quando o proprietário solicitar mais resultados, então poderá acessá-los mantendo os critérios da pesquisa atual.
- **CA01.12:** Dado um limite de consultas ou indisponibilidade do catálogo, quando a operação falhar, então a interface informará o problema sem tratá-lo como ausência de correspondências e manterá o cadastro manual disponível.
- **CA01.13:** Dado um resultado com metadados adicionais, quando for importado no MVP, então a inclusão usará apenas título, artistas e os dois anos disponíveis, sem exigir capas ou outros metadados não aprovados.

- **CA01.14:** Dados os campos de título e artista vazios ou compostos apenas por espaços, quando uma pesquisa externa for solicitada, então nenhuma consulta será enviada ao catálogo e a interface pedirá que o proprietário informe título ou artista.

### RF02 — Cadastrar álbuns manualmente

**Comportamento confirmado:** oferecer cadastro manual, inclusive para álbuns não encontrados no catálogo, com título, artista e ano original obrigatórios; ano da versão e links opcionais. A indisponibilidade do catálogo não pode impedir esse caminho.

**Entrada:** título, artista, ano original e, opcionalmente, ano da versão e links. **Saída:** álbum persistido e consultável ou indicação dos campos inválidos/erro.

O cadastro deve disponibilizar campos separados para ano original do álbum e ano do lançamento específico. O ano original deve ser preenchido antes de concluir o cadastro. O ano do lançamento específico pode ficar vazio; não deve ser copiado automaticamente do ano original.

**Validações e restrições:** título, artista ou ano original ausente impede conclusão; texto composto apenas por espaços é inválido e os limites e o tratamento dos campos seguem a seção 7.5. O cadastro deve respeitar equivalência de edições. Não exigir metadados não aprovados.

**Erros e extremos:** campos obrigatórios ausentes, caracteres acentuados, títulos iguais de artistas diferentes, coletâneas, duplicatas e salvamento malsucedido.

- **CA02.1:** Dados título, artista e ano original válidos segundo as regras aprovadas, quando o proprietário cadastrar sem links e o salvamento tiver sucesso, então o álbum ficará disponível na biblioteca.
- **CA02.2:** Dado um cadastro sem título, sem artista ou sem ano original, quando for enviado, então a conclusão será impedida e o campo obrigatório será identificado.
- **CA02.3:** Dado um catálogo indisponível, quando o proprietário acessar o cadastro manual, então poderá preencher e salvar um álbum se os demais serviços necessários estiverem disponíveis.
- **CA02.4:** Dada uma equivalência confirmada, quando o cadastro manual for concluído, então não será criada uma segunda entrada do mesmo álbum.
- **CA02.5:** Dados anos válidos informados separadamente para o lançamento original e para a versão escolhida, quando o cadastro for salvo e consultado, então ambos serão apresentados com identificação distinta, inclusive quando seus valores forem iguais.

- **CA02.6:** Dados título, artista e ano original válidos, quando o cadastro for salvo sem ano específico, então a ausência desse campo opcional não impedirá a inclusão e ele permanecerá sem valor informado.

### RF03 — Consultar, editar e remover álbuns

**Comportamento confirmado:** permitir consultar os dados salvos, alterá-los e remover entradas da biblioteca. Manter apenas uma versão escolhida de cada álbum e permitir que o proprietário a substitua por outra versão do mesmo álbum, sem criar um segundo item.

**Entrada:** álbum selecionado, alterações, versão substituta ou solicitação de remoção. **Saída:** dados consultados, atualização persistida ou entrada removida.

Na troca da versão, preservar o ano original do álbum e todos os links existentes, incluindo endereços e associações aos serviços. O ano do lançamento específico representa a nova versão escolhida e deve poder ser atualizado independentemente do ano original. Corrigir explicitamente o ano original continua permitido como edição dos dados do álbum. A troca não exige encontrar links correspondentes à nova versão nem substitui links automaticamente. Se o ano da nova versão for desconhecido, o campo opcional pode ficar vazio. O ano da versão anterior não deve ser atribuído automaticamente à nova versão; o mapeamento dos dados do catálogo depende de P08.

**Validações e restrições:** manter campos obrigatórios após edição; alterações de identidade devem respeitar equivalência de edições. A remoção exige confirmação identificando o álbum e informando que não há opção de desfazer no MVP. Excluir o álbum remove seus links e associações com artistas, preservando os serviços e os demais álbuns. Se uma edição encontrar outro álbum equivalente, interromper o salvamento e apresentar a entrada existente, sem combinar registros automaticamente. Um álbum removido deixa de pertencer à coleção e ao conjunto elegível para sorteios posteriores com dados atualizados.

**Erros e extremos:** álbum removido em outro dispositivo, edição concorrente, falha de carregamento, edição que gere equivalência e falha/resultado incerto de gravação ou remoção. Não confirmar remoção persistente antes de conhecer o resultado.

- **CA03.1:** Dado um álbum salvo, quando consultado, então seus dados persistidos serão apresentados.
- **CA03.2:** Dada uma alteração válida salva com sucesso, quando o álbum for recarregado, então os novos dados serão apresentados.
- **CA03.3:** Dada uma edição que retire um campo obrigatório, quando enviada, então será impedida e o campo será identificado.
- **CA03.4:** Dado um álbum cuja remoção foi persistida, quando a biblioteca atualizada for consultada, então ele não aparecerá na coleção nem participará de um novo sorteio sobre essa coleção.
- **CA03.5:** Dada uma falha confirmada ao atualizar ou remover, quando o resultado for exibido, então não haverá mensagem de sucesso da operação.
- **CA03.6:** Dadas alterações concorrentes incompatíveis, quando a segunda tentativa for processada, então não haverá sobrescrita silenciosa; a primeira gravação válida será mantida e a segunda, baseada em dados desatualizados, será bloqueada com aviso, preservação dos dados digitados e apresentação dos dados atuais para revisão, conforme seção 7.3.
- **CA03.7:** Dado um álbum com uma versão escolhida, quando o proprietário trocar essa versão e a alteração for salva, então a entrada passará a representar a versão escolhida, sem criar outro item nem alterar a quantidade de álbuns da coleção.
- **CA03.8:** Dado um álbum já cadastrado, quando uma edição equivalente for reconhecida e confirmada, então não será permitido manter ambas como itens distintos; será possível manter a versão atual ou solicitar sua substituição.
- **CA03.9:** Dado um álbum com ano original, ano da versão e links salvos, quando a versão for trocada e o novo ano específico for informado e salvo, então o ano original e todos os links permanecerão intactos, o ano específico refletirá a nova versão e continuará existindo um único item.
- **CA03.10:** Dados os dois anos cadastrados, quando o proprietário corrigir explicitamente um deles e salvar, então apenas o ano editado será alterado, sem modificar automaticamente o outro.

- **CA03.11:** Dado um álbum com ano específico informado, quando o proprietário apagar apenas esse campo e salvar, então a edição será aceita, mantendo o ano original e os links.
- **CA03.12:** Dada a troca para uma versão cujo ano seja desconhecido, quando a troca for salva sem ano específico, então o campo ficará vazio, sem herdar o ano da versão anterior.

### RF04 — Organizar álbuns por artista

**Comportamento confirmado:** disponibilizar navegação por artista e agrupamento “Vários artistas”, inclusive para coletâneas. Um álbum pode aparecer sob vários artistas ou apenas sob seu artista principal, permanecendo um único item da coleção. Usar o artista principal como agrupamento padrão quando estiver identificado. Em álbuns colaborativos, permitir associar vários artistas e apresentar a mesma entrada nos respectivos agrupamentos.

**Entrada:** artista principal, artistas associados ou agrupamento associado ao álbum. **Saída:** álbuns apresentados nos agrupamentos correspondentes.

**Validações e restrições:** “Vários artistas” é uma possibilidade de agrupamento, não uma regra que obriga toda coletânea a usá-lo. Múltiplas associações são permitidas e não duplicam o álbum. Sugerir artistas já cadastrados comparando nomes sem distinguir maiúsculas ou acentos, preservando a grafia escolhida. Permitir artistas homônimos distintos, sem união automática. Ocultar da navegação agrupamentos sem álbuns, preservando os registros de artistas. Ordenar artistas por nome e álbuns por título, em ordem alfabética. Coletâneas podem usar “Vários artistas” sem cadastrar cada participante.

**Erros e extremos:** artista sem álbuns após remoção, artistas homônimos, colaboração entre artistas e alteração do artista de um álbum.

- **CA04.1:** Dado um álbum associado a um artista, quando o agrupamento desse artista for consultado, então o álbum será apresentado.
- **CA04.2:** Dada uma coletânea associada a “Vários artistas”, quando esse agrupamento for consultado, então a coletânea será apresentada.
- **CA04.3:** Dada uma mudança de agrupamento salva com sucesso, quando os agrupamentos atualizados forem consultados, então refletirão as associações vigentes, sem criar cópias do álbum.
- **CA04.4:** Dado um álbum apresentado sob dois artistas, quando for consultado por qualquer desses agrupamentos, então será acessada a mesma entrada; a contagem total da coleção incluirá esse álbum uma única vez.

- **CA04.5:** Dado um álbum com artista principal identificado, quando organizado sem outras associações escolhidas, então será apresentado sob esse artista como agrupamento padrão; em uma colaboração com vários artistas associados, a mesma entrada ficará disponível nos respectivos agrupamentos.
- **CA04.6:** Dada uma coletânea válida, quando o proprietário escolher “Vários artistas” como agrupamento e salvar, então o cadastro não exigirá informar cada participante.
- **CA04.7:** Dado um artista cadastrado, quando um nome que difira apenas por maiúsculas ou acentos for informado na associação, então o artista existente será sugerido, sem alterar automaticamente a grafia escolhida nem unir registros.
- **CA04.8:** Dados dois artistas distintos com o mesmo nome, quando forem cadastrados e associados a álbuns, então os registros continuarão distintos, sem combinação automática por coincidência de nome.
- **CA04.9:** Dado um artista cujo último álbum foi removido ou desassociado, quando a navegação for atualizada, então seu agrupamento não aparecerá, mas seu registro será preservado.
- **CA04.10:** Dados artistas e álbuns com nomes distintos sem ambiguidade de ordenação, quando a navegação for apresentada, então artistas estarão ordenados alfabeticamente por nome e álbuns por título.

### RF05 — Pesquisar na biblioteca por título ou artista

**Comportamento confirmado:** permitir encontrar álbuns da própria coleção pelo título ou pelo artista.

**Entrada:** termo de pesquisa. **Saída:** álbuns correspondentes da biblioteca ou indicação de nenhuma correspondência.

**Validações e restrições:** não inserir resultados externos na coleção por causa da pesquisa. Buscar por parte do título ou do nome de qualquer artista associado, incluindo “Vários artistas”, ignorando maiúsculas, acentos e espaços nas extremidades do termo. Exibir cada álbum uma única vez, mesmo com múltiplas correspondências. Campo vazio, inclusive após remover espaços nas extremidades, apresenta toda a coleção. Busca por erros de digitação fica fora do MVP.

**Erros e extremos:** coleção vazia, nenhum resultado, vários álbuns com o mesmo título e falha de carregamento. Falha de leitura não equivale a coleção vazia.

- **CA05.1:** Dado um álbum na coleção, quando pesquisado por seu título completo cadastrado, então ele será retornado.
- **CA05.2:** Dados álbuns de um artista na coleção, quando pesquisado pelo nome completo cadastrado desse artista, então os álbuns correspondentes serão retornados.
- **CA05.3:** Dado um termo sem correspondência segundo a política aprovada, quando a pesquisa terminar com sucesso, então a ausência de resultados será informada.
- **CA05.4:** Dado um álbum que exista apenas no catálogo externo, quando a biblioteca for pesquisada, então ele não será apresentado como parte da coleção.

- **CA05.5:** Dado um álbum com título “Kind of Blue”, quando a pesquisa for “of bl”, então o álbum será retornado por correspondência parcial, sem distinção de maiúsculas.
- **CA05.6:** Dado um álbum associado a João Gilberto, quando a pesquisa for “ joao ”, então o álbum será retornado, ignorando acento, maiúsculas e espaços nas extremidades; a grafia cadastrada permanecerá inalterada.
- **CA05.7:** Dado um álbum com vários artistas associados, quando pesquisado por parte do nome de qualquer um deles, então o álbum será retornado, mesmo que a correspondência seja com um artista diferente do principal.
- **CA05.8:** Dada uma coletânea associada a “Vários artistas”, quando pesquisado “varios artistas”, então a coletânea será retornada.
- **CA05.9:** Dado um álbum cujo título e artistas produzam várias correspondências com o mesmo termo, quando os resultados forem apresentados, então haverá apenas uma ocorrência desse álbum.
- **CA05.10:** Dada uma coleção carregada com sucesso, quando o campo de pesquisa estiver vazio ou contiver apenas espaços, então toda a coleção será apresentada; se a coleção realmente estiver vazia, seu estado vazio será informado.

### RF06 — Cadastrar, editar e excluir serviços de streaming

**Comportamento confirmado:** permitir ao proprietário cadastrar, editar e excluir os serviços que deseja utilizar. Não permitir links sem serviço existente.

**Escolha delegada para exclusão:** pedir confirmação informando o serviço e a quantidade de links associados que serão removidos. Ao confirmar, remover o serviço e todas as suas associações de links, preservando os álbuns e links de outros serviços. Ao cancelar, preservar todos os dados. Essa solução evita manter serviços inativos ou links órfãos e não exige reatribuir links a um serviço diferente.

**Entrada:** dados de identificação do serviço, alterações ou solicitação e confirmação/cancelamento de exclusão. **Saída:** serviço cadastrado ou atualizado, ou serviço e seus links removidos; álbuns preservados.

**Validações e restrições:** cadastro de serviço não implica integração com sua conta, importação de biblioteca ou contratação de assinatura. Editar um serviço deve manter os vínculos existentes com os álbuns. A exclusão e a remoção dos links devem constituir uma única operação lógica: não pode haver um resultado persistido com links órfãos. Exigir apenas o nome, de até 100 caracteres após remover espaços nas extremidades; impedir nomes repetidos ignorando maiúsculas e espaços nas extremidades, inclusive na edição.

**Erros e extremos:** serviço já cadastrado, serviço sem links, serviço já removido em outro dispositivo, falha ao salvar/excluir e inclusão concorrente de link durante exclusão. Uma falha não deve ser apresentada como exclusão bem-sucedida; a recuperação deve manter a integridade das associações, conforme P09.

- **CA06.1:** Dado um nome de serviço válido conforme a seção 7.5, quando o proprietário cadastrar um serviço e a persistência confirmar sucesso, então ele ficará disponível para associação de links.
- **CA06.2:** Dada uma falha confirmada de persistência, quando houver tentativa de cadastro do serviço, então o sistema informará a falha sem confirmar salvamento.
- **CA06.3:** Dado um serviço com links associados, quando seus dados forem editados e salvos, então os links continuarão vinculados ao mesmo serviço atualizado.
- **CA06.4:** Dado um serviço com links, quando sua exclusão for solicitada, então a confirmação identificará o serviço e a quantidade de links afetados.
- **CA06.5:** Dada a confirmação de exclusão, quando o proprietário cancelar, então o serviço e todos os links permanecerão inalterados.
- **CA06.6:** Dada a confirmação de exclusão, quando o proprietário confirmar e a operação tiver sucesso, então o serviço e seus links serão removidos; os álbuns e links de outros serviços serão preservados e nenhum link órfão permanecerá.
- **CA06.7:** Dado um serviço sem links, quando sua exclusão for confirmada e concluída, então apenas o serviço será removido.
- **CA06.8:** Dada uma falha de exclusão ou uma associação concorrente, quando o resultado persistido for verificado, então nenhum link apontará para serviço inexistente e não haverá confirmação falsa de sucesso. A recuperação segue a seção 7.3; o mecanismo que garante a integridade dos vínculos será definido no desenho técnico.

### RF07 — Associar links manualmente e abrir destinos externos

**Comportamento confirmado:** permitir associar manualmente links de streaming aos álbuns e abrir os destinos selecionados. Links de diferentes edições podem pertencer à mesma entrada.

Os links pertencem à entrada do álbum e não precisam corresponder exatamente à versão escolhida. A troca de versão mantém os links intactos; não exige buscar, validar a correspondência da edição ou cadastrar novos destinos.

**Entrada:** álbum, serviço cadastrado e endereço. **Saída:** associação persistida e tentativa de abertura do endereço externo quando solicitada.

**Validações e restrições:** validar o formato do endereço e sua segurança antes de armazenar/acionar; aceitar endereço completo iniciado por `https://`, com domínio válido, sem lista fixa de domínios por serviço, conforme seção 7.5. Associação exige álbum e serviço existentes; tentativas de associar a um serviço já excluído devem ser recusadas. A exclusão do serviço remove seus links conforme RF06. Permitir vários links por serviço no mesmo álbum, com edição e remoção individuais; impedir o mesmo endereço repetido no mesmo álbum, inclusive sob outro serviço, removendo apenas espaços nas extremidades para essa comparação. Não exigir resposta do destino para salvar. Solicitar abertura em nova aba; o dispositivo poderá encaminhar ao aplicativo externo. A aplicação não reproduz áudio nem garante a disponibilidade do destino.

**Erros e extremos:** endereço malformado ou inseguro, link indisponível, restrição regional, exigência de login/assinatura no destino e bloqueio de abertura pelo dispositivo. Detectar todos os erros internos do serviço externo não é obrigação aprovada.

- **CA07.1:** Dados álbum, serviço e link válido, quando a associação for salva com sucesso e recarregada, então o link ficará disponível no álbum e vinculado ao serviço informado.
- **CA07.2:** Dado um link válido associado, quando selecionado, então a aplicação solicitará sua abertura no destino externo.
- **CA07.3:** Dado um endereço inválido conforme a política aprovada, quando houver tentativa de associação, então a entrada será recusada com indicação do problema.
- **CA07.4:** Dado um álbum sem links, quando cadastrado ou sorteado, então a ausência de links não impedirá a operação.
- **CA07.5:** Dados links de edições equivalentes, quando associados à mesma entrada, então não será necessário criar outro álbum para representá-los.
- **CA07.6:** Dado um álbum com links de uma edição diferente da versão atualmente escolhida, quando esses links forem consultados ou selecionados após a troca de versão, então continuarão disponíveis com os mesmos endereços e serviços associados.

### RF08 — Sortear um álbum da biblioteca

**Comportamento confirmado:** sortear entre todos os álbuns da coleção, dando a cada entrada a mesma probabilidade. Repetições consecutivas são permitidas.

**Entrada:** solicitação de sorteio e conjunto de álbuns da biblioteca. **Saída:** um álbum pertencente ao conjunto ou orientação para adicionar um álbum se ele estiver vazio.

**Validações e restrições:** não filtrar por presença de link, artista ou audições anteriores. Cada entrada tem probabilidade 1/N, sendo N o número de álbuns distintos elegíveis. Associações a vários artistas não acrescentam participações; trocar a versão não cria participação adicional. Não alterar estado do álbum por ouvir ou sortear. Usar os dados persistidos carregados para o sorteio; se o escolhido tiver sido removido antes da apresentação, atualizar a coleção e sortear novamente, conforme seção 7.3.

**Erros e extremos:** biblioteca vazia, um único álbum, resultado igual ao anterior e falha ao carregar o conjunto. Uma falha de leitura não pode originar a orientação falsa de que a coleção está vazia.

- **CA08.1:** Dada uma biblioteca não vazia carregada com sucesso, quando o sorteio for solicitado, então exatamente um álbum dessa biblioteca será apresentado.
- **CA08.2:** Dada uma biblioteca vazia carregada com sucesso, quando o sorteio for solicitado, então a interface orientará a adicionar um álbum.
- **CA08.3:** Dada uma biblioteca com um único álbum, quando forem feitos sorteios sucessivos, então esse álbum será o resultado de todos eles.
- **CA08.4:** Dado um resultado igual ao anterior, quando o novo sorteio for concluído, então o resultado será aceito sem excluir ou refazer o sorteio apenas pela repetição.
- **CA08.5:** Dada uma coleção com N entradas, quando o mecanismo de seleção for verificado, então cada entrada terá probabilidade 1/N e nenhuma será excluída por falta de links. A verificação deve examinar o mecanismo e suas entradas; frequências de uma amostra finita não provam igualdade exata.
- **CA08.6:** Dada a coleção antes do sorteio, quando o resultado for apresentado, então os dados e a presença dos álbuns na coleção permanecerão iguais, salvo alterações independentes concorrentes.
- **CA08.7:** Dada uma coleção com um álbum associado a vários artistas e outros álbuns associados a um único artista, quando o conjunto do sorteio for formado, então cada álbum constará uma única vez e terá a mesma probabilidade 1/N.

### RF09 — Persistir a coleção e acessar os mesmos dados em vários dispositivos

**Comportamento confirmado:** preservar dados entre sessões e disponibilizar a mesma biblioteca nos dispositivos utilizados pelo proprietário.

**Entrada:** operações de gravação e solicitações de carregamento autorizado. **Saída:** dados persistidos recuperados, confirmação de operação bem-sucedida ou erro explícito.

**Validações e restrições:** a mudança deve estar disponível quando outro dispositivo carregar a biblioteca após a confirmação de persistência. Atualização automática em tempo real não está exigida. O comportamento de concorrência e de operações interrompidas segue a seção 7.3: bloquear gravação baseada em estado desatualizado e consultar operações de resultado incerto antes de permitir repetição segura. Os mecanismos técnicos serão definidos no desenho. Não exigir funcionamento sem rede.

**Erros e extremos:** falta de conexão, indisponibilidade de armazenamento, gravação recusada, sessão encerrada durante operação, resposta perdida após gravação e dados desatualizados em outro dispositivo.

- **CA09.1:** Dada uma alteração salva no dispositivo A, quando a biblioteca for carregada com autorização no dispositivo B após a confirmação, então a alteração estará disponível.
- **CA09.2:** Dados álbuns, serviços e associações de links salvos, quando a sessão for encerrada e os dados carregados novamente com autorização, então os dados persistidos estarão disponíveis.
- **CA09.3:** Dada uma falha confirmada de salvamento, quando o resultado for informado, então não haverá confirmação de sucesso.
- **CA09.4:** Dado um erro de carregamento, quando a tela for apresentada, então será indicada a falha sem afirmar que a biblioteca está vazia.
- **CA09.5:** Dadas alterações simultâneas incompatíveis em dois dispositivos, quando processadas, então não haverá sobrescrita silenciosa. A primeira gravação válida será preservada; a tentativa baseada no estado anterior será bloqueada, mantendo o conteúdo digitado e exibindo os dados atuais para revisão e novo salvamento.

### RF10 — Restringir acesso ao proprietário

**Comportamento confirmado:** permitir consulta e alteração apenas pelo proprietário, sem cadastro público ou compartilhamento.

**Entrada:** tentativa de acesso, consulta ou alteração. **Saída:** operação autorizada ou acesso negado sem exposição da biblioteca.

**Validações e restrições:** autorização deve proteger os dados persistidos e suas operações, inclusive acesso direto fora da interface. O proprietário aprovou entrar usando uma conta existente de um provedor de identidade, como Google, sem criar senha própria da aplicação. Google é a referência apresentada; o provedor e sua viabilidade gratuita ainda devem ser validados. Apenas a conta identificada como a do proprietário poderá acessar a biblioteca; identificar-se com outra conta do mesmo provedor não concede acesso nem cria biblioteca ou cadastro público. Não solicitar nem armazenar a senha da conta externa na aplicação. A conta do proprietário deve ser autorizada previamente, antes de seu primeiro acesso, sem cadastro público. Manter a sessão por até sete dias após a entrada, exigindo nova entrada ao término desse período. Disponibilizar “Sair” em cada dispositivo, encerrando a sessão naquele dispositivo. Recuperar acesso à conta externa pelo próprio provedor, sem senha alternativa na aplicação. Se o provedor estiver indisponível, informar a falha e permitir tentar novamente sem liberar acesso indevido. A integração deve ter sua viabilidade validada antes da implementação; o procedimento técnico de autorização prévia e os controles de sessão serão definidos no desenho.

**Erros e extremos:** ausência de autorização, evidência de acesso inválida, sessão expirada e tentativa direta de obter ou modificar registros.

- **CA10.1:** Dada uma tentativa sem autorização, quando a biblioteca ou uma operação sobre seus dados for acessada, então nenhum dado protegido será exibido e nenhuma alteração será aceita.
- **CA10.2:** Dado o proprietário com autorização válida, quando consultar ou executar uma operação válida, então a restrição de acesso permitirá a operação.
- **CA10.3:** Dada uma tentativa de leitura ou escrita direta nos recursos de dados sem autorização, quando processada, então será negada mesmo sem utilizar a interface.
- **CA10.4:** Dada uma autorização inválida ou expirada conforme a política aprovada, quando houver nova operação protegida, então ela será recusada sem expor dados.
- **CA10.5:** Dada a conta externa autorizada do proprietário, quando a entrada for concluída com sucesso pelo provedor validado, então o proprietário poderá acessar sua biblioteca sem cadastrar senha própria da aplicação.
- **CA10.6:** Dada outra conta válida no mesmo provedor, quando ela tentar entrar, então o acesso à biblioteca será negado e nenhuma nova conta da aplicação ou biblioteca será criada.
- **CA10.7:** Dada uma entrada cancelada ou malsucedida no provedor, quando o fluxo retornar à aplicação, então o acesso protegido continuará negado, sem confirmação falsa de entrada bem-sucedida.

- **CA10.8:** Dada a conta do proprietário autorizada previamente, quando ocorrer seu primeiro acesso pelo provedor validado, então a entrada será permitida sem cadastro público; uma conta sem essa autorização continuará impedida de acessar a biblioteca.
- **CA10.9:** Dada uma sessão ainda válida antes de completar sete dias desde a entrada, quando o proprietário acessar a aplicação, então poderá continuar conectado sem nova entrada, respeitando os demais controles de validade; ao completar sete dias, uma operação protegida exigirá nova entrada, sem renovação silenciosa que ultrapasse esse prazo.
- **CA10.10:** Dadas sessões válidas em dois dispositivos, quando o proprietário selecionar “Sair” em um deles, então aquela sessão deixará de autorizar operações protegidas, enquanto a sessão do outro dispositivo permanecerá sujeita à sua própria validade.
- **CA10.11:** Dada a perda de acesso à conta externa, quando o proprietário buscar recuperação, então será orientado a usar o processo do próprio provedor; a aplicação não oferecerá senha alternativa nem liberará a biblioteca sem autorização válida.
- **CA10.12:** Dado o provedor indisponível durante uma tentativa de entrada, quando a falha for detectada, então a aplicação informará a indisponibilidade e permitirá tentar novamente, sem conceder acesso protegido a essa tentativa malsucedida.

## 5. Regras de negócio

| ID | Regra confirmada | Funcionalidades afetadas |
|---|---|---|
| RN01 | A coleção contém apenas álbuns adicionados pelo proprietário | RF01–RF05, RF08–RF10 |
| RN02 | Ouvir um álbum não altera seu estado nem o remove | RF03, RF08 |
| RN03 | Edições padrão, deluxe e remasterizadas contam como o mesmo álbum; manter uma única versão escolhida, substituível pelo proprietário | RF01–RF03, RF08 |
| RN04 | Links de diferentes edições podem pertencer à mesma entrada | RF07 |
| RN05 | Inclusão de edição confirmada como equivalente não gera outra entrada | RF01–RF03 |
| RN06 | Coletâneas podem ser agrupadas em “Vários artistas” | RF02–RF05 |
| RN07 | Cada álbum tem a mesma chance no sorteio; resultados podem se repetir | RF08 |
| RN08 | Ausência de links não impede cadastro nem sorteio | RF01, RF02, RF07, RF08 |
| RN09 | O aplicativo abre destinos externos e não reproduz música | RF07 |
| RN10 | Título, artista e ano original são obrigatórios no cadastro; ano do lançamento específico é opcional | RF01–RF03 |
| RN11 | Apenas o proprietário pode consultar e alterar a biblioteca | Todos os dados protegidos |
| RN12 | Um álbum pode aparecer sob vários artistas ou apenas sob seu artista principal, mas conta como um único item, inclusive no sorteio | RF04, RF05, RF08 |
| RN13 | Serviços podem ser editados e excluídos; não pode haver links órfãos | RF06, RF07, RF09 |
| RN14 | Por escolha delegada, excluir um serviço exige confirmação do impacto e remove seus links, preservando álbuns e links de outros serviços | RF06, RF07 |
| RN15 | Manter separados o ano original do álbum e o ano de lançamento da versão específica; trocar a versão não altera automaticamente o ano original | RF01–RF03 |
| RN16 | Trocar a versão mantém os links existentes intactos; os links não precisam corresponder à versão escolhida | RF03, RF07 |

A comparação de título e artistas, ignorando maiúsculas e acentos, sugere possíveis duplicatas e exige confirmação do proprietário; não determina equivalência automaticamente. O proprietário pode indicar que são álbuns diferentes e continuar o cadastro. Equivalência confirmada oferece manter a entrada existente ou trocar sua versão, sem cadastrar outro item. A recusa de uma sugestão equivocada não autoriza duas versões reconhecidamente equivalentes. Links de outras edições continuam permitidos pelo escopo e não representam versões adicionais cadastradas. Sua preservação na troca de versão está confirmada em RN16. Outros metadados ainda não aprovados não têm política de substituição definida.

## 6. Requisitos não funcionais, segurança e desempenho

| ID | Requisito e origem | Evidência verificável / limite pendente |
|---|---|---|
| RNF01 | Interface utilizável em computador e celular — confirmado | Validar em um celular e um computador do proprietário, incluindo larguras de 360 e 1280 pixels; sem rolagem horizontal nas telas principais. Critérios na seção 7.6; referências informadas: Samsung Galaxy S24 FE com Chrome e computador com Windows/Chrome |
| RNF02 | Operações principais acessíveis por teclado e campos identificados — confirmado | Concluir entrada, cadastro, edição, remoção, pesquisa, gestão de serviços/links e sorteio sem mouse, com foco visível, campos identificados, obrigatoriedade indicada e erros associados aos campos. Não depender apenas de cores; ver seção 7.6. Não foi escolhida norma formal de acessibilidade |
| RNF03 | Persistência entre sessões e dispositivos — confirmado | CA09.1 e CA09.2, incluindo edição e remoção; não implica modo offline |
| RNF04 | Mensagens claras de falha e confirmação verdadeira — confirmado | CA01.3, CA03.5, CA09.3 e CA09.4; distinguir falha, ausência de resultados e vazio |
| RNF05 | Nenhuma sobrescrita silenciosa em alterações simultâneas — confirmado | CA03.6, CA09.5 e seção 7.3; comportamento aprovado, mecanismo pendente no desenho técnico |
| RNF06 | Consulta e alteração protegidas contra terceiros — confirmado | CA10.1–CA10.4, cobrindo dados de álbuns, artistas, serviços e links |
| RNF07 | Proteger dados e evidências de autorização durante transmissão e armazenamento — derivado de RF10 | Verificar controles do desenho escolhido; credenciais e segredos de infraestrutura não devem aparecer em arquivos públicos, interface ou mensagens de erro; solução depende de P10/P13 |
| RNF08 | Tratar metadados e endereços externos como dados não confiáveis — derivado de RF10 | Títulos/metadados com conteúdo executável devem ser exibidos como texto; endereços capazes de executar código devem ser recusados; formatos aceitos aprovados em RF07 e na seção 7.5 |
| RNF09 | Validar entradas também na fronteira que grava os dados — derivado | Uma requisição direta com campo obrigatório ausente ou sem autorização deve ser recusada, independentemente da validação visual |
| RNF10 | Não revelar dados da biblioteca nem segredos em erros acessíveis a terceiros — derivado | Provocar erro de acesso e verificar a resposta; política de registros e retenção depende de P10/P13 |
| RNF11 | Operar sem contratação de serviços pagos — confirmado | Conferir custos e limites das alternativas antes da escolha; exceder cota gratuita não autoriza cobrança nem plano pago |
| RNF12 | Respeitar condições, cobertura e limites do catálogo — dependência confirmada | Validar fornecedor e condições antes da integração; não há catálogo validado nem limites numéricos aprovados |
| RNF13 | Aprendizado em etapas pequenas, com compreensão das decisões — confirmado | Ao concluir cada etapa, o proprietário explica a decisão técnica e demonstra o comportamento entregue |
| RNF14 | Cópias de segurança diárias, retenção dos últimos sete dias e perda tolerável de até 24 horas de alterações — metas aprovadas | Ver seção 7.4; comprovar cobertura, restrição de acesso e restauração antes do uso definitivo. Viabilidade gratuita pendente em P13 |

### Desempenho e metas de uso

O escopo apresentou metas iniciais propostas. Posteriormente, o proprietário aprovou os critérios de tarefas de pesquisa e inclusão, a biblioteca piloto de 30 álbuns e o protocolo de medição abaixo. Os tempos medem a tarefa completa do usuário, incluindo sua interação; não são limites de resposta técnica do sistema. A meta de uso do sorteio continua como objetivo de avaliação do produto.

| Meta / critério | Forma de aferição | Observação / pendência |
|---|---|---|
| Biblioteca piloto de 30 álbuns, com coletâneas e edições equivalentes | Conferir composição da coleção e ausência de entradas extras para equivalências confirmadas | 30 é tamanho do piloto, não limite da coleção |
| Encontrar um álbum conhecido em até 15 segundos — aprovado | Cronometrar desde começar a pesquisa até localizar o resultado; três tentativas em cada dispositivo | Registrar individualmente tempos, falhas e condições observadas de conexão; identificar dispositivos e navegadores |
| Adicionar resultado do catálogo em até 1 minuto — aprovado | Cronometrar desde selecionar o resultado até confirmar salvamento, com campos obrigatórios disponíveis; três tentativas em cada dispositivo | Registrar indisponibilidade/limitação externa separadamente; não contar operação incompleta como sucesso |
| Mesma coleção em dois dispositivos | Executar CA09.1 nos dispositivos escolhidos | Referências: Samsung Galaxy S24 FE com Chrome e computador Windows/Chrome |
| Sorteio usado para pelo menos três audições em duas semanas | Relato do proprietário sobre uso do sorteio | Não criar histórico de audição para medir a meta |

Não foram definidos tempo máximo de resposta, volume máximo de álbuns/links, disponibilidade percentual, taxa de requisições, tempo de sincronização automática ou tolerância a interrupções. Os critérios de tarefa e o piloto estão aprovados; esses outros valores permanecem para avaliação no desenho técnico antes de assumir compromissos adicionais de desempenho ou capacidade. Não escolher cache, índices ou infraestrutura nesta especificação.

## 7. Validações, erros e casos extremos transversais

| Situação | Comportamento exigido ou limite de decisão |
|---|---|
| Título/artista/ano original ausente | Impedir cadastro/edição inválida e identificar campo; não exigir ano da versão; demais validações nas seções 7.1 e 7.5 |
| Dados acentuados, Unicode e nomes homônimos | Não presumir equivalência nem transformar dois álbuns em um automaticamente; limites de cadastro aprovados na seção 7.5; comparação para sugestões de artistas e pesquisa aprovadas em RF04/RF05 |
| Edição equivalente ou inclusão repetida | Comparar título e artistas ignorando maiúsculas e acentos e solicitar confirmação; permitir corrigir sugestão equivocada; equivalência confirmada mantém uma entrada, com opção de trocar a versão |
| Troca de versão com links existentes | Preservar endereços e associações aos serviços, sem exigir correspondência com a nova edição; manter ano original e permitir atualizar o ano específico |
| Anos iguais, diferentes ou desconhecidos | Armazenar os conceitos separadamente; ano original obrigatório e ano específico opcional; não inferir ano original a partir de reedição. Formato, intervalo e cronologia aprovados na seção 7.1 |
| Exclusão de serviço com links | Confirmar impacto e remover serviço e links associados em conjunto, preservando álbuns e links de outros serviços; nenhum vínculo órfão, inclusive sob concorrência |
| Álbum sob vários artistas | Contar uma única entrada na coleção e uma única participação no sorteio |
| Clique repetido ou reenvio após demora | A mesma solicitação de cadastro deve produzir apenas uma inclusão; consultar o resultado anterior sem criar outro item; reconciliação aprovada na seção 7.3 e mecanismo pendente no desenho técnico |
| Resposta de gravação perdida | Resultado é incerto, não uma falha comprovada; não afirmar sucesso ou orientar repetição como se nada tivesse sido salvo; consultar o resultado antes de permitir repetição segura, conforme seção 7.3 |
| Catálogo falhou ou retornou dados incompletos | Mostrar erro quando aplicável e manter cadastro manual; solicitar preenchimento/correção de campos obrigatórios antes de salvar, conforme RF01 |
| Biblioteca realmente vazia | Informar vazio após leitura bem-sucedida; no sorteio, orientar inclusão |
| Carregamento falhou | Informar falha; não apresentar a coleção como vazia |
| Um único álbum | Sempre sorteá-lo, inclusive sem links |
| Serviço ou destino externo indisponível | Biblioteca e sorteio não dependem da reprodução externa; comunicar somente falhas detectáveis pela aplicação |
| Sem conexão | Não garantir operação offline nem confirmar persistência inexistente; recuperação da tentativa segue a seção 7.3 |
| Registro alterado/removido por outro dispositivo | Não sobrescrever silenciosamente nem confirmar operação sobre estado inexistente; resolução aprovada na seção 7.3 |
| Tentativa de acesso não autorizado | Recusar leitura/escrita sem revelar dados protegidos |
| Conteúdo malicioso em campo/link | Não executar conteúdo e rejeitar endereço inseguro conforme RNF08 |
| Limite gratuito ou capacidade excedida | Informar falha sem sucesso falso; não contratar serviços automaticamente; estratégia em P12/P13 |
| Perda de dados persistidos | Metas aprovadas na seção 7.4: cópia diária, retenção de sete dias e perda tolerável de até 24 horas de alterações; validar viabilidade gratuita e demonstrar restauração antes do uso definitivo, sem presumir proteção já implementada |

Mensagens devem explicar a operação afetada e seu resultado conhecido em linguagem compreensível. Códigos internos ou detalhes de infraestrutura não substituem a mensagem ao proprietário. Texto exato, preservação de formulário e ações de repetição ainda podem ser definidos no desenho da experiência, respeitando os resultados acima.

### 7.1. Validação dos anos — aprovada

A obrigatoriedade do ano original, a opcionalidade do ano específico e as regras VA01–VA07 foram aprovadas explicitamente pelo proprietário. Aplicam-se ao cadastro manual, à inclusão pelo catálogo e à edição.

| ID | Validação aprovada | Motivo e comportamento esperado |
|---|---|---|
| VA01 | Aceitar quatro algarismos de 0 a 9, formando um ano inteiro entre 1000 e o ano atual, inclusive | Regra simples para anos completos, sem criar um corte histórico específico para álbuns; 1000 é um limite de formato aprovado, não uma afirmação sobre a história da música. Usar limite superior dinâmico, sem fixar 2026 no código |
| VA02 | Remover espaços no início/fim; rejeitar letras, sinais, decimais, datas completas e espaços entre algarismos | Evitar interpretações ambíguas; por exemplo, aceitar “ 1997 ” como 1997 e recusar “97”, “1997.5”, “19 97” e “01/01/1997” |
| VA03 | Recusar ano original vazio ou composto apenas por espaços; permitir ano específico vazio | Campo opcional vazio deve significar “não informado”, sem usar 0, ano atual ou ano original como preenchimento automático |
| VA04 | Quando informado, exigir ano específico igual ou posterior ao original | Evitar uma versão anterior ao primeiro lançamento do mesmo álbum; se houver inconsistência no catálogo, pedir conferência/correção dos valores |
| VA05 | Recusar anos futuros em ambos os campos | Regra aprovada para uma coleção de álbuns já lançados. Incluir lançamentos futuros exigirá revisão explícita deste requisito |
| VA06 | Validar os mesmos critérios na interface e na operação que persiste os dados; indicar o campo e o motivo do erro | Impedir que uma requisição direta contorne as regras; manter os valores preenchidos para correção e não confirmar salvamento de dados inválidos |
| VA07 | Validar o par de anos também ao corrigir o ano original ou trocar a versão | Se a alteração tornar o ano específico anterior ao original, pedir correção ou remoção explícita do ano opcional; não corrigir valores silenciosamente |

Se o ano original não for conhecido ou não vier do catálogo, o proprietário deverá informá-lo antes da inclusão, como consequência de sua obrigatoriedade. Não usar o ano da reedição como aproximação nem inventar um valor. O preenchimento dos anos não exige busca adicional em outra fonte externa como funcionalidade do MVP.

**Critérios de aceitação das validações aprovadas:**

- **CA-VA01:** Dado o ano atual A, quando forem informados 1000 ou A em um campo de ano, então o limite de intervalo será atendido; 999 e A+1 serão recusados.
- **CA-VA02:** Dado um valor com formato inválido conforme VA02, quando o formulário ou uma gravação direta for enviado, então a operação será recusada com indicação do campo; espaços apenas nas extremidades serão removidos.
- **CA-VA03:** Dados ano original 1997 e ano específico vazio, 1997 ou 2017, quando os demais dados forem válidos e o cadastro for salvo, então cada uma dessas combinações será aceita.
- **CA-VA04:** Dados ano original 1997 e ano específico 1996, quando houver tentativa de gravação, então a inconsistência será apontada sem salvamento nem alteração silenciosa dos valores.
- **CA-VA05:** Dados anos original 1997 e específico 2017, quando o original for alterado para 2018 sem ajuste do específico, então a gravação será impedida até correção ou remoção explícita do ano opcional.

### 7.2. Identidade dos álbuns e remoção — aprovadas

As decisões abaixo foram aprovadas pelo proprietário. Valem para inclusão manual e por catálogo, quando aplicável.

| ID | Regra aprovada |
|---|---|
| ID01 | Comparar título e artistas ignorando diferenças de maiúsculas/minúsculas e acentos para sugerir possíveis duplicatas. Essa comparação não deve alterar a grafia cadastrada nem ser tratada como prova de equivalência |
| ID02 | Solicitar confirmação ao proprietário. Se confirmar equivalência, apresentar a entrada existente e oferecer manter ou trocar a versão. Se indicar “são álbuns diferentes”, permitir continuar o cadastro |
| ID03 | Cliques repetidos ou repetição da mesma solicitação de cadastro devem resultar em uma única inclusão, inclusive após demora ou perda de resposta. Isso é diferente de cadastrar intencionalmente outro álbum distinto com dados semelhantes |
| ID04 | Antes de remover um álbum, identificar o item e informar que não haverá opção de desfazer no MVP. Cancelar preserva os dados; confirmar e concluir remove o álbum, seus links e associações com artistas, preservando os serviços, os registros de artistas e os demais álbuns. Agrupamentos vazios ficam ocultos da navegação, preservando os registros de artistas |
| ID05 | Quando uma edição encontrar outro álbum equivalente, interromper o salvamento e apresentar a entrada existente, sem juntar registros automaticamente. Uma mera semelhança deve permitir a correção da sugestão equivocada conforme ID02 |

Os detalhes técnicos da comparação com múltiplos artistas e da identificação da mesma solicitação serão definidos no desenho técnico, respeitando as regras aprovadas. Não foi aprovado usar o ano como prova de equivalência nem combinar registros automaticamente.

- **CA-ID01:** Dados um álbum existente e uma tentativa de inclusão com título e artistas iguais, exceto por acentos ou maiúsculas, quando a verificação ocorrer, então será apresentada uma possível duplicata para confirmação, sem alteração automática da grafia ou combinação de registros.
- **CA-ID02:** Dada uma possível duplicata, quando o proprietário confirmar equivalência, então a entrada existente será apresentada com as opções de manter ou trocar sua versão, sem nova entrada.
- **CA-ID03:** Dada uma sugestão equivocada, quando o proprietário indicar que são álbuns diferentes, então poderá concluir o cadastro de outro item com os campos válidos.
- **CA-ID04:** Dada uma mesma solicitação de inclusão enviada mais de uma vez, quando as tentativas forem processadas, então haverá apenas um álbum criado por essa solicitação.
- **CA03.13:** Dado um álbum com links e associações com artistas, quando sua remoção for solicitada, então a confirmação identificará o álbum e informará a ausência de opção de desfazer.
- **CA03.14:** Dada a confirmação de remoção de álbum, quando o proprietário cancelar, então o álbum, seus links e associações permanecerão inalterados.
- **CA03.15:** Dada uma remoção de álbum confirmada e concluída, quando os dados forem recarregados, então o álbum, seus links e suas associações com artistas estarão ausentes; os serviços, registros de artistas e demais álbuns estarão preservados.
- **CA03.16:** Dada uma edição que encontre outro álbum equivalente, quando houver tentativa de salvar, então a gravação será interrompida e a entrada existente será apresentada, sem alteração ou combinação automática de nenhum dos dois registros.

### 7.3. Conflitos entre dispositivos e resultado incerto — aprovados

O proprietário aprovou os comportamentos abaixo. A aprovação define a experiência e a integridade esperadas, sem escolher tecnologia, formato de controle de versão ou mecanismo de armazenamento.

| ID | Situação | Comportamento aprovado |
|---|---|---|
| CC01 | Mesmo álbum editado em dois dispositivos a partir do mesmo estado | Aceitar a primeira gravação válida. Bloquear a segunda tentativa baseada no estado anterior e avisar que os dados mudaram, sem sobrescrever a alteração já salva |
| CC02 | Edição bloqueada por conflito | Preservar o conteúdo digitado na tentativa em andamento, apresentar os dados atuais e permitir revisar e salvar novamente. Não combinar alterações automaticamente. Essa preservação não exige funcionamento offline nem recuperação do formulário após encerrar a sessão |
| CC03 | Álbum removido enquanto outro dispositivo o edita | Informar que o álbum foi removido, preservar o conteúdo da tentativa para consulta e não recriar o registro automaticamente |
| CC04 | Conexão interrompida durante salvamento ou resposta perdida | Informar que o resultado ainda não foi confirmado. Consultar a operação antes de permitir repetição segura; não afirmar falha definitiva nem sucesso sem evidência. Enquanto não for possível verificar, manter o resultado como não confirmado |
| CC05 | Sorteio durante alteração da coleção | Usar os dados persistidos carregados para aquele sorteio. Se o escolhido tiver sido removido antes da apresentação, atualizar a coleção e sortear novamente. Se a coleção atualizada estiver vazia, orientar a adicionar um álbum; se a atualização falhar, informar a falha, sem confundi-la com coleção vazia |

A repetição da mesma solicitação de cadastro continua limitada a uma inclusão, conforme ID03. Operações que excluem álbuns ou serviços continuam obrigadas a preservar a integridade dos vínculos; nenhuma resolução de conflito autoriza links órfãos. Os mecanismos e os pontos de verificação necessários para garantir esses resultados serão definidos no desenho técnico.

- **CA-CC01:** Dadas duas edições do mesmo álbum baseadas no mesmo estado, quando a primeira for salva e a segunda enviada, então a segunda será bloqueada, a primeira permanecerá salva e o dispositivo com conflito exibirá aviso, seus valores digitados e os dados atuais.
- **CA-CC02:** Dado um conflito exibido, quando o proprietário revisar os valores e salvar novamente sobre o estado atualizado, então uma alteração válida poderá ser persistida; se ocorrer nova mudança concorrente antes da gravação, o conflito será novamente informado.
- **CA-CC03:** Dado um álbum removido após o início de uma edição em outro dispositivo, quando a edição for enviada, então o sistema informará a remoção e não recriará o álbum automaticamente.
- **CA-CC04:** Dada uma gravação concluída cuja resposta se perdeu, quando o sistema consultar a operação, então reconhecerá o resultado persistido; uma repetição da mesma solicitação de cadastro não criará outro item.
- **CA-CC05:** Dada uma gravação de resultado desconhecido, quando a consulta da operação também estiver indisponível, então o sistema manterá a indicação de resultado não confirmado, sem permitir nova tentativa como se a falha estivesse comprovada.
- **CA-CC06:** Dado um álbum escolhido que tenha sido removido antes da apresentação, quando o resultado for preparado, então a coleção será atualizada e um novo sorteio será realizado sobre os álbuns disponíveis; se não restar nenhum, será apresentada a orientação de inclusão.
- **CA-CC07:** Dada uma falha ao atualizar a coleção após detectar a remoção do escolhido, quando o sorteio não puder ser concluído, então a falha será informada sem apresentar o álbum removido como disponível nem afirmar que a biblioteca está vazia.

### 7.4. Proteção e recuperação dos dados — metas aprovadas

O proprietário aprovou as metas abaixo. Elas são requisitos a verificar, não evidência de que cópias já existam ou de que um fornecedor gratuito consiga atendê-las. A recuperação dos dados da biblioteca é distinta da recuperação de acesso à conta externa.

| ID | Meta ou regra aprovada |
|---|---|
| BK01 | Proteger álbuns, anos original e específico, artistas, serviços, links e suas associações, de forma que a coleção possa ser recuperada coerentemente |
| BK02 | Produzir uma cópia de segurança diária e manter as cópias dos últimos sete dias |
| BK03 | Aceitar perda de, no máximo, 24 horas de alterações; a existência de uma rotina diária, por si só, não comprova essa meta se as cópias não forem concluídas e recuperáveis |
| BK04 | Restringir o acesso às cópias ao proprietário e aos componentes necessários à recuperação |
| BK05 | Demonstrar uma restauração e conferir os dados recuperados antes de usar a biblioteca como coleção definitiva |
| BK06 | Restaurar por procedimento técnico orientado, sem botão de recuperação na interface do MVP. Antes de executar a restauração, explicar seu impacto nos dados atuais e obter autorização explícita do proprietário |
| BK07 | Avaliar atendimento das metas com orçamento zero. Se as alternativas gratuitas não atenderem, apresentar a limitação para decisão do proprietário antes do uso definitivo; não reduzir silenciosamente as metas nem contratar serviços pagos |

Restaurar uma cópia pode substituir dados atuais e perder alterações posteriores ao ponto restaurado. Isso não oferece desfazer individual de exclusões, que continua fora do MVP. O local das cópias, o mecanismo de execução/verificação e o procedimento técnico serão definidos posteriormente. Não foi aprovado um prazo máximo para concluir a restauração.

- **CA-BK01:** Dada uma biblioteca de verificação com álbuns, ambos os campos de ano (inclusive ano específico vazio), vários artistas, serviços e links, quando uma cópia for restaurada em ambiente de verificação, então os dados e associações corresponderão ao ponto recuperado, sem duplicar álbuns nem criar links órfãos.
- **CA-BK02:** Dada a rotina de cópias em operação durante sete dias completos, quando os resultados forem conferidos, então haverá cópias diárias recuperáveis cobrindo esse período, conforme a política de retenção aprovada.
- **CA-BK03:** Dado um incidente de referência em uma simulação, quando o ponto recuperável mais recente for identificado, então a diferença temporal até o incidente não ultrapassará 24 horas. Se a meta não for atendida, a limitação será registrada, sem declarar proteção conforme.
- **CA-BK04:** Dada uma tentativa de acessar as cópias por terceiro ou componente sem permissão, quando processada, então será negada sem revelar os dados da biblioteca.
- **CA-BK05:** Dado o início do uso definitivo planejado, quando a preparação operacional for revisada, então existirá evidência de uma restauração demonstrada e da conferência dos dados; nenhuma demonstração é presumida nesta etapa de requisitos.
- **CA-BK06:** Dada uma proposta de restauração sobre a biblioteca em uso, quando o procedimento for preparado, então o proprietário receberá a identificação do ponto a recuperar e o impacto nos dados atuais; a execução dependerá de sua autorização explícita e não ocorrerá em caso de recusa.
- **CA-BK07:** Dada uma avaliação em que as opções gratuitas não atendam às metas, quando seu resultado for apresentado, então as limitações ficarão explícitas e o uso definitivo dependerá da decisão do proprietário, sem contratação paga automática ou redução silenciosa dos requisitos.

### 7.5. Campos, serviços e links — validações aprovadas

O proprietário aprovou as regras abaixo. Aplicam-se ao cadastro, à edição e aos dados de catálogo antes da persistência. As validações devem ser aplicadas na interface e na operação que grava os dados, com indicação clara do campo inválido, sem truncar valores silenciosamente.

| ID | Regra aprovada |
|---|---|
| VL01 | Título obrigatório com até 300 caracteres; nome de cada artista obrigatório com até 200; nome do serviço obrigatório com até 100. Os limites são aplicados após remover espaços nas extremidades |
| VL02 | Remover apenas espaços nas extremidades dos campos de texto; recusar campo obrigatório que fique vazio. Aceitar acentos, outros alfabetos, números e pontuação, preservando a grafia e os espaços internos. Exibir conteúdo como texto, sem executá-lo |
| VL03 | Exigir apenas nome para cadastrar serviço. Impedir nomes repetidos ignorando maiúsculas/minúsculas e espaços nas extremidades; não foi aprovada a remoção de acentos nessa comparação. A unicidade vale também ao editar |
| VL04 | Aceitar links completos iniciados por `https://`, com domínio válido. Não exigir lista fixa de domínios por serviço, permitindo endereços de compartilhamento e redirecionamento. Validade de formato não comprova disponibilidade ou conteúdo do destino |
| VL05 | Permitir vários links por serviço em um álbum. Impedir o mesmo endereço repetido no mesmo álbum, inclusive associado a serviço diferente; para comparar e salvar, remover apenas espaços nas extremidades e preservar o restante do endereço |
| VL06 | Permitir editar e remover links individualmente, preservando o álbum, seus demais links e os serviços cadastrados. A edição deve respeitar formato e unicidade por álbum |
| VL07 | Solicitar abertura em nova aba; o dispositivo poderá encaminhar ao aplicativo externo. Não exigir que o destino responda para permitir salvar um link válido |

**Critérios de aceitação:**

- **CA-VL01:** Dados título com 300 caracteres, nome de artista com 200 e nome de serviço com 100 após retirar espaços nas extremidades, quando as respectivas operações válidas forem enviadas, então os limites serão atendidos; valores com um caractere a mais serão recusados, sem truncamento silencioso.
- **CA-VL02:** Dado um título, artista ou nome de serviço vazio ou composto apenas por espaços, quando houver tentativa de cadastro ou edição, então o campo será identificado e a gravação impedida.
- **CA-VL03:** Dados nomes válidos com acentos, outros alfabetos, números ou pontuação, quando forem salvos e consultados, então a grafia e os espaços internos serão preservados, removendo apenas espaços nas extremidades e sem executar conteúdo.
- **CA06.9:** Dado um serviço chamado “Spotify”, quando houver tentativa de cadastrar outro chamado “ spotify ” ou de renomear outro serviço para esse nome, então a duplicidade será indicada e a gravação impedida.
- **CA06.10:** Dado um nome de serviço válido e ainda não cadastrado, quando o proprietário solicitar cadastro sem outros campos, então o sistema não exigirá dados adicionais para concluir a operação.
- **CA07.7:** Dados endereços completos HTTPS com domínio válido, inclusive de compartilhamento ou redirecionamento, quando associados a serviço existente, então não serão recusados apenas por o domínio não estar em uma lista fixa do serviço; endereços sem domínio, relativos ou com outro protocolo serão recusados.
- **CA07.8:** Dado um álbum com um link, quando outro endereço válido diferente for associado ao mesmo serviço, então ambos poderão permanecer na mesma entrada do álbum.
- **CA07.9:** Dado um endereço já associado ao álbum, quando o mesmo endereço, inclusive com espaços apenas nas extremidades, for incluído ou resultar de edição de outro link desse álbum, então a repetição será impedida, mesmo sob outro serviço. Diferenças no restante do endereço não serão removidas para presumir equivalência.
- **CA07.10:** Dado um link existente, quando seu endereço ou serviço associado for editado e salvo com valores válidos e sem duplicidade, então a associação será atualizada sem modificar o álbum ou seus demais links.
- **CA07.11:** Dado um álbum com links associados, quando um link for removido e a operação concluída, então apenas esse vínculo será removido, preservando o álbum, os demais links e os serviços cadastrados.
- **CA07.12:** Dado um link válido salvo, quando selecionado, então a aplicação solicitará abertura em nova aba, permitindo o encaminhamento pelo dispositivo ao aplicativo externo, sem prometer controlar esse encaminhamento.
- **CA07.13:** Dado um endereço de formato válido cujo destino esteja indisponível, quando houver tentativa de associação, então a aplicação não exigirá resposta bem-sucedida do destino para permitir salvar o link.

### 7.6. Interface e desempenho das tarefas — critérios aprovados

O proprietário aprovou a validação em um celular e um computador que utiliza, incluindo conferência da interface com larguras de 360 e 1280 pixels, sem rolagem horizontal nas telas principais. Os ambientes de referência informados pelo proprietário são Samsung Galaxy S24 FE com Chrome e computador com Windows/Chrome. Registrar as versões efetivamente utilizadas dos sistemas e navegadores ao executar a validação, sem presumir compatibilidade já comprovada. As larguras de 360 e 1280 pixels são condições de conferência da interface, não especificações declaradas das telas desses dispositivos.

As operações em andamento devem ser indicadas e envios repetidos acidentais impedidos na interface, sem substituir a garantia de inclusão única por solicitação da seção 7.2. Os fluxos de entrada, cadastro, edição, remoção, pesquisa, gestão de serviços/links e sorteio devem poder ser concluídos por teclado, com foco visível. Campos devem ter identificação, obrigatoriedade explícita e erros associados ao campo correspondente. Cor não deve ser o único meio de indicar sucesso, erro ou seleção.

A avaliação de desempenho usará a biblioteca piloto de 30 álbuns, incluindo coletâneas e edições equivalentes sem entradas duplicadas. Realizar três tentativas de cada tarefa em cada dispositivo. Registrar individualmente os tempos e as falhas; registrar indisponibilidade ou limitação externa separadamente, sem ocultá-la e sem contar operações incompletas como sucesso. Trinta é o tamanho do piloto, não o limite da coleção; a avaliação de capacidade maior será feita no desenho técnico.

- **CA-UI01:** Dadas as telas principais, quando conferidas com larguras de 360 e 1280 pixels, então seus conteúdos e controles poderão ser utilizados sem rolagem horizontal.
- **CA-UI02:** Dados os fluxos de entrada, cadastro, edição, remoção, pesquisa, serviços/links e sorteio, quando executados apenas por teclado, então será possível alcançar e acionar seus controles e concluir as operações, com indicação visível do foco.
- **CA-UI03:** Dado um formulário, quando apresentado, então cada campo terá identificação e indicação de obrigatoriedade; ao ocorrer erro de validação, o erro será associado ao campo correspondente.
- **CA-UI04:** Dado um estado de sucesso, erro ou seleção, quando apresentado, então seu significado poderá ser identificado sem depender apenas da cor.
- **CA-UI05:** Dada uma operação ainda em processamento, quando a interface for observada e seu acionamento repetido for tentado, então haverá indicação de andamento e prevenção de envios repetidos acidentais.
- **CA-PF01:** Dada a biblioteca piloto e um álbum conhecido, quando a tarefa de pesquisa for medida desde seu início até localizar o resultado, então seu tempo será comparado ao limite aprovado de 15 segundos e seu resultado individual registrado.
- **CA-PF02:** Dado um resultado de catálogo com os campos obrigatórios disponíveis, quando a inclusão for medida desde selecionar o resultado até confirmar salvamento, então seu tempo será comparado ao limite aprovado de um minuto; uma inclusão não confirmada não será registrada como sucesso.
- **CA-PF03:** Dados um celular e um computador de referência identificados, quando o protocolo de desempenho for executado, então haverá três tentativas por tarefa em cada dispositivo, com tempos, falhas, navegadores e condições de execução registrados; limitações externas serão identificadas separadamente.
- **CA-PF04:** Dada a biblioteca piloto de 30 álbuns, quando sua validação for concluída, então esse número não será convertido em restrição de cadastro; eventuais limites de produção dependerão de decisão posterior, sem presumir capacidade já demonstrada.

## 8. Contradições, ambiguidades e decisões pendentes

Não foi identificada contradição explícita que torne o escopo inviável por definição. Há tensões e lacunas que impedem tratar todos os detalhes como decididos. As perguntas seguintes não devem ser respondidas por suposição na implementação.

| ID | Lacuna, ambiguidade ou tensão | Pergunta / decisão necessária | Impacto |
|---|---|---|---|
| P01 | Resolvida para os dados aprovados: sugestão por título/artistas, confirmação e correção pelo proprietário; mesma solicitação não duplica cadastro | Nenhuma decisão de negócio restante neste bloco. Se outros metadados forem aprovados, definir seu tratamento; mecanismo de repetição segura em P09 | RF01–RF03; ver seção 7.2 |
| P02 | Resolvida: anos conforme seção 7.1; título até 300 caracteres e artista até 200, obrigatórios após remover espaços nas extremidades, com grafia e caracteres preservados | Nenhuma decisão de negócio restante neste bloco; ver seção 7.5 | Cadastro, edição e validação |
| P03 | Resolvida: confirmar remoção, sem desfazer; remover vínculos e links do álbum; bloquear edição que encontre outro equivalente, sem combinação automática | Nenhuma decisão restante neste bloco; concorrência aprovada na seção 7.3 | RF03; ver seção 7.2 |
| P04 | Resolvida: artista principal por padrão, múltiplos artistas em colaborações, coletâneas com “Vários artistas”, sugestões sem união automática, homônimos permitidos, vazios ocultos e ordem alfabética | Nenhuma decisão de negócio restante neste bloco; detalhes de comparação e ordenação serão definidos no desenho respeitando RF04 | RF04, RF05 e modelo de dados |
| P05 | Resolvida: busca parcial por título ou qualquer artista associado, incluindo “Vários artistas”; ignora maiúsculas, acentos e espaços nas extremidades; álbum único por resultado; campo vazio mostra coleção | Sem busca por erros de digitação no MVP; ver critérios de RF05 | RF05 |
| P06 | Resolvida: apenas nome obrigatório de até 100 caracteres; unicidade ignora maiúsculas e espaços nas extremidades; edição e exclusão com integridade dos links | Nenhuma decisão restante neste bloco; ver RF06 e seção 7.5 | RF06, RF07 |
| P07 | Resolvida: HTTPS com domínio válido, sem lista fixa por serviço; múltiplos links, edição/remoção individuais, endereço único por álbum e abertura em nova aba | Não exigir disponibilidade do destino para salvar; preservar endereço exceto espaços nas extremidades; ver seção 7.5 | RF07, segurança e experiência |
| P08 | Comportamento aprovado em RF01: busca por título e/ou artista, dados mínimos, anos distintos, correção antes de salvar, mais resultados sem perder pesquisa e ausência de atualização automática | Avaliar fornecedor, cobertura, termos, viabilidade gratuita, mapeamento dos dois anos e limites de consulta. Pesquisa sem título nem artista não consulta o catálogo e orienta o preenchimento, conforme aprovação do proprietário. Capas e outros metadados continuam para avaliação posterior | RF01 e dependência externa; integração não escolhida |
| P09 | Comportamento aprovado: primeira gravação válida preservada, conflito explícito com revisão, consulta de resultado incerto e atualização do sorteio se escolhido removido | Regras resolvidas na seção 7.3; mecanismos de controle de concorrência, consulta de operação e integridade dos vínculos permanecem para o desenho técnico | RF03, RF06–RF09 e integridade |
| P10 | Comportamento de acesso aprovado: conta previamente autorizada, sessão de até sete dias, saída por dispositivo e recuperação pelo provedor, sem senha alternativa | Validar provedor e viabilidade gratuita; definir mecanismo de autorização prévia e sessão no desenho técnico. Política de registros e eventuais requisitos adicionais de privacidade permanecem a definir | RF10 e segurança |
| P11 | Critérios de interface aprovados: celular/computador, larguras de 360/1280 pixels, teclado, foco, campos/erros identificados, informação além da cor e indicação de operação em andamento | Referências definidas: Samsung Galaxy S24 FE com Chrome e computador Windows/Chrome. Registrar versões na execução; nenhuma norma formal ou matriz adicional de tecnologias assistivas escolhida | Requisitos e ambientes definidos na seção 7.6; execução da validação futura |
| P12 | Critérios de tarefa aprovados: piloto de 30 álbuns, pesquisa até 15 segundos, inclusão até um minuto e três tentativas por tarefa em cada dispositivo, com registro de tempos/falhas | Usar os ambientes definidos em P11 e registrar condições de conexão; avaliar capacidade maior e eventuais limites técnicos no desenho. Trinta álbuns não é limite da coleção | Seção 7.6 e tabela de desempenho; sem fornecedor ou capacidade de produção validados |
| P13 | Metas de proteção aprovadas: cópia diária, retenção de sete dias, perda tolerável de até 24 horas, acesso restrito e restauração técnica demonstrada e autorizada | Quais soluções gratuitas atendem às metas e aos limites de armazenamento compartilhado? Definir execução, armazenamento, verificação das cópias e procedimento de restauração. Se inviável gratuitamente, apresentar limitações e obter decisão antes do uso definitivo | Viabilidade técnica e operacional pendente; ver seção 7.4 |

**Tensões a resolver:** edições equivalentes exigem identidade além de simples igualdade de título; orçamento zero não garante disponibilidade e recuperação; as metas de recuperação estão aprovadas, mas sua viabilidade e execução ainda não foram validadas; acesso em vários dispositivos não define atualização automática. A possibilidade de links externos quebrados não contradiz RF07: a aplicação controla a tentativa de abertura, enquanto o serviço externo controla seu conteúdo e acesso.

O proprietário respondeu às perguntas sobre P01, P04 e P06: confirmou uma única versão substituível por álbum, permitiu apresentação sob um ou vários artistas com contagem única e aprovou edição/exclusão de serviços sem links órfãos. Delegou a escolha do tratamento dos links na exclusão: esta revisão define confirmação do impacto e remoção conjunta dos links do serviço. As pendências residuais constam na tabela. Essas respostas complementam o escopo original, que não foi alterado, e não equivalem à aprovação integral desta especificação.

Em esclarecimento posterior, o proprietário confirmou a existência de dois campos — ano original do álbum e ano do lançamento específico — e determinou que os links permaneçam intactos na troca de versão, sem exigir correspondência exata com a edição nos serviços de streaming. Essa decisão resolve a preservação dos links em P01. Em seguida, o proprietário definiu ano original obrigatório e ano específico opcional e solicitou uma sugestão de validações. O proprietário aprovou explicitamente as validações VA01–VA07 da seção 7.1 e seus critérios de aceitação. A pendência sobre essas validações está encerrada; as questões de título/artista foram posteriormente resolvidas na seção 7.5 e P08 mantém o mapeamento no catálogo.

O proprietário também aprovou o bloco de identidade e remoção da seção 7.2: sugestão de duplicatas com confirmação, correção de sugestões equivocadas, inclusão única por solicitação, confirmação de exclusão sem desfazer e sem combinação automática em edições. P01 e P03 estão resolvidas para os dados atualmente aprovados.

O proprietário aprovou também o bloco de conflitos entre dispositivos e resultados incertos da seção 7.3. As decisões de comportamento de P09 estão resolvidas; os mecanismos técnicos serão avaliados no desenho, sem autorização para implementar nesta etapa.

O proprietário aprovou entrar com uma conta existente, como Google, sem criar uma senha para a aplicação. A biblioteca permanece restrita ao proprietário. Em seguida, aprovou a autorização prévia de sua conta, sessão de até sete dias, saída por dispositivo, recuperação pelo próprio provedor e aviso com possibilidade de nova tentativa se o provedor estiver indisponível. As decisões de comportamento de acesso de P10 estão resolvidas; integração, autorização prévia e controles de sessão permanecem para avaliação técnica. A recuperação de acesso é distinta da recuperação dos dados da coleção em P13.

O proprietário aprovou as metas de cópia e recuperação da seção 7.4: cópia diária com retenção de sete dias, perda tolerável de até 24 horas, acesso restrito, demonstração antes do uso definitivo e restauração técnica com autorização explícita. A viabilidade gratuita e os mecanismos operacionais permanecem pendentes em P13; não foi autorizada implementação nem restauração nesta etapa.

O proprietário aprovou as regras de organização e pesquisa incorporadas a RF04/RF05 e seus critérios: artista principal por padrão, múltiplas associações para colaborações, coletâneas simplificadas, sugestões com grafia preservada, homônimos distintos, agrupamentos vazios ocultos, ordem alfabética e busca parcial sem distinguir acentos/maiúsculas, com contagem única por álbum. P04 e P05 estão resolvidas.

O proprietário aprovou o bloco de validações da seção 7.5, encerrando P02, P06 e P07: limites e tratamento dos campos, nome único de serviço e regras de formato, multiplicidade, manutenção e abertura dos links. As validações ainda não foram implementadas.

O proprietário aprovou os critérios de interface e desempenho da seção 7.6 e o protocolo das tarefas descrito na tabela de desempenho. Posteriormente, o proprietário identificou Samsung Galaxy S24 FE com Chrome e computador com Windows/Chrome como ambientes de referência; as versões serão registradas na execução. Essa identificação não comprova tempos, compatibilidade ou capacidade. P11 está definida quanto aos requisitos e ambientes, com execução futura; P12 mantém a avaliação técnica de capacidade e eventuais limites adicionais.

O proprietário aprovou o comportamento do catálogo detalhado em RF01: pesquisa por título e/ou artista, apresentação dos dados mínimos e anos distintos, correção de campos antes de salvar, manutenção editável dos dados, ausência de atualização automática e carregamento de mais resultados sem perder a pesquisa. P08 mantém a avaliação técnica do fornecedor e as lacunas residuais explícitas; nenhum catálogo foi escolhido ou consultado nesta revisão.

O proprietário aprovou também o bloqueio de pesquisa externa totalmente vazia: orientar o preenchimento de título ou artista, sem consultar o catálogo, inclusive quando houver apenas espaços.

## 9. Aprovação e verificação futura

O proprietário aprovou explicitamente esta especificação como base para a próxima etapa de avaliação técnica e arquitetura, mantendo explícitas as pendências técnicas da seção 8. Essa aprovação encerra a etapa de especificação de requisitos; não autoriza implementação, contratação de serviços ou deploy.

As pendências restantes continuam explícitas e bloqueiam os comportamentos que dependem delas; a aprovação não escolhe implicitamente tecnologias, fornecedores ou alternativas técnicas. Se a avaliação identificar incompatibilidade com requisitos ou orçamento, apresentar a limitação ao proprietário para decisão, sem alterar silenciosamente as regras aprovadas.

Para aceitar uma funcionalidade implementada no futuro, será necessário demonstrar seus critérios CA, validar os RN/RNF aplicáveis e registrar decisões pendentes resolvidas. A verificação de acesso deve cobrir a interface e o acesso direto aos dados; a de persistência deve incluir duas sessões e dois dispositivos; a de concorrência deve usar alterações incompatíveis sobre o mesmo estado.

**Evidência desta etapa:** o escopo foi lido e os requisitos foram especificados. Não houve implementação, execução de testes de aplicação, validação de fornecedor, implantação ou comprovação das metas de desempenho.

**Revisão ativa sugerida:** explique com suas palavras por que “cada álbum tem a mesma chance” é regra de negócio, enquanto “todos os campos identificados e fluxos acessíveis por teclado” é requisito de qualidade. Essa revisão não é uma funcionalidade do produto.
