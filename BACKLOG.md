# Music Library — Backlog priorizado

**Data:** 22/10/2026.  
**Status:** B01 concluída em 22/10/2026, com decisões registradas e revisão ativa realizada. Preparação técnica inicial já presente, sem aceite automático dos critérios de B06/B07.

**Fontes:** [PROJECT_SCOPE.md](PROJECT_SCOPE.md), [REQUIREMENTS.md](REQUIREMENTS.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

## 1. Premissas e limites

- Os requisitos detalhados e os esclarecimentos aprovados prevalecem sobre simplificações do escopo.
- Ano original é obrigatório; ano da versão é opcional. Trocar a versão preserva os links.
- Backups e restauração técnica são condições anteriores ao uso definitivo. Exportação e recuperação pela interface continuam fora do MVP.
- A estrutura geral com monólito Django, páginas renderizadas no servidor e PostgreSQL compartilhado foi aprovada na revisão da B01, assim como revisão global, repetição segura por UUID, geração após restauração, identidade prévia e validação da infraestrutura gratuita. As decisões estão registradas na seção 13 de `ARCHITECTURE.md`. Google, MusicBrainz, fornecedores de infraestrutura e detalhes técnicos não avaliados continuam propostos.
- O projeto já possui repositório Git e estrutura inicial Django. A revisão da B01 ocorre na branch `docs/b01-revisao-arquitetura`.
- Aprovar este backlog não autoriza implementação, instalação, operações Git, configuração externa, migração ou deploy.
- O proprietário escreverá testes e implementação com mentoria, uma tarefa por vez.

**MVP:** cadastro manual e por catálogo; consulta, edição e exclusão; artistas e pesquisa; serviços e links; sorteio; persistência compartilhada; acesso exclusivo; tratamento de conflitos e resultados incertos; proteção operacional demonstrada.

## 2. Como usar

**Prioridades:**

- **P0:** decisão ou fundamento necessário para evitar trabalho inviável, exposição ou perda de dados.
- **P1:** comportamento essencial do MVP.
- **P2:** comprovação integrada e preparação para uso definitivo.
- **P3:** avaliação de uso ou melhoria posterior.

Prioridade não substitui dependência: uma tarefa só começa quando suas dependências estiverem satisfeitas. B01 está **concluída**, com decisões aprovadas e registradas e revisão ativa realizada. Há arquivos de preparação relacionados a B06/B07, cujos critérios e dependências ainda precisam ser conferidos antes de registrar conclusão. Os demais itens permanecem **a fazer**; decisões e provas podem terminar com uma limitação documentada, que deverá ser resolvida antes de liberar seus dependentes.

CA significa critério de aceitação. As referências abaixo apontam para os identificadores de `REQUIREMENTS.md`.

Nas tarefas de implementação, usar TDD quando adequado: escrever um teste que falha, implementar o mínimo e melhorar a organização mantendo o comportamento.

## 3. Decisões e provas de viabilidade

Estas tarefas produzem decisões ou evidências, sem entregar funcionalidades do produto.

| ID / prioridade | Objetivo | Dependências | Critérios de aceitação | Verificação prevista | Risco principal |
|---|---|---|---|---|---|
| B01 · P0 · concluída em 22/10/2026 | Revisar e decidir sobre a arquitetura proposta | — | Registrar aprovação, ajustes ou rejeição; explicitar revisão global, identidade prévia, geração de operações e limitações gratuitas | Decisões registradas na seção 13 de ARCHITECTURE.md; revisão ativa sobre UUID realizada com o proprietário | Tratar proposta como escolha aprovada |
| B02 · P0 | Avaliar orçamento e infraestrutura candidata | B01 | Registrar cotas, suspensão, persistência, TLS, permissões de banco, ordenação em português e comportamento ao exceder limites; nenhuma cobrança automática aceita | Revisão documental e, quando autorizado, configuração real | Orçamento zero inviável para as metas |
| B03 · P0 | Validar catálogo com 30 álbuns representativos | B01 | Registrar cobertura, licença, título/artistas, dois anos, coletâneas, colaborações, homônimos, edições e paginação; decidir se o candidato atende P08 | Consultas controladas autorizadas e comparação manual | Cobertura insuficiente ou anos interpretados incorretamente |
| B04 · P0 | Definir autorização prévia da identidade | B01 | Aprovar obtenção verificada de emissor/identificador da conta, vínculo do proprietário, configuração gratuita e política de registros; não usar primeiro login como autorização | Revisão do procedimento e prova autorizada do provedor | Vincular terceiro ou manter entrada alternativa |
| B05 · P0 | Avaliar recuperação gratuita antes de investir no piloto remoto | B02 | Identificar execução, armazenamento, criptografia, recuperação da chave, cotas, retenção e supervisão; registrar como serão avaliadas as 24 horas; alternativa inviável exige decisão | Conferência de capacidade/custos e simulação do procedimento | Confundir agendamento com proteção recuperável |

B03 bloqueia a integração real do catálogo. B04 bloqueia o login real. B05 não comprova recuperação: sua execução e demonstração aparecem em B33–B36.

## 4. Fundação e primeira inclusão manual

Os itens técnicos abaixo existem para habilitar a primeira fatia completa: entrar, cadastrar e consultar um álbum.

| ID / prioridade | Objetivo | Dependências | Critérios de aceitação | Testes previstos | Risco principal |
|---|---|---|---|---|---|
| B06 · P0 | Preparar Git e branch de trabalho | B01 | Após autorização específica, ter repositório, exclusão de segredos do versionamento e branch de trabalho; nenhum commit direto em main/master | Conferir branch, estado e arquivos ignorados | Versionar credenciais |
| B07 · P0 | Preparar aplicação e banco local de testes | B02, B06 | Após autorização, fixar dependências compatíveis; executar aplicação mínima e teste com PostgreSQL descartável; configuração sem segredos no código | Inicialização e conexão com banco | Ambiente local esconder diferenças do banco remoto |
| B08 · P1 | Validar os dois anos | B07 | Cumprir VA01–VA07: quatro dígitos ASCII, intervalo dinâmico, original obrigatório, versão opcional e cronologia; usar America/Fortaleza | CA-VA01–05; relógio controlado, virada do ano e formatos inválidos | Ano fixo ou preenchimento automático indevido |
| B09 · P1 | Validar textos e construir chaves de comparação | B07 | Limites 300/200/100, espaços externos removidos e grafia preservada; busca ignora acentos/caixa; chave de serviço preserva acentos | CA-VL01–03; Unicode, limites exatos e espaços internos | Usar uma normalização inadequada para todas as regras |
| B10 · P0 | Persistir álbum e artistas com integridade | B08, B09 | Migração mínima; álbum com ao menos um artista, no máximo um principal, homônimos distintos e anos separados; gravação inválida recusada no comando | Banco vazio, restrições e rollback de associação inválida | Álbum incompleto persistido |
| B11 · P0 | Permitir entrada somente do proprietário | B04, B07 | Identidade previamente autorizada entra; terceiros não criam conta nem biblioteca; falha/cancelamento mantém acesso negado; sem senha/cadastro/admin alternativo | CA10.1–08, CA10.11–12; rotas diretas e provedor simulado | Proteção apenas na interface |
| B12 · P0 | Limitar sessão e sair por dispositivo | B11 | Expiração absoluta em sete dias; atividade não prorroga prazo; saída invalida apenas a sessão atual | CA10.4, CA10.9–10; relógio controlado e duas sessões | Sessão renovada indefinidamente |
| B13 · P0 | Estabelecer gravação transacional com revisão e recibo | B10, B11 | Mudança e recibo são atômicos; UUID repetido com mesmos dados recupera resultado; conteúdo diferente, revisão antiga ou geração antiga são recusados | Rollback, repetição paralela e disputa real em duas conexões | Efeito duplicado ou sucesso registrado sem mudança |
| B14 · P1 | Cadastrar manualmente e consultar um álbum | B12, B13 | Formulário e comando validam os mesmos campos; salvar sem links/ano específico funciona; detalhe mostra dados persistidos; erros não confirmam sucesso | CA02.1–03, CA02.5–06, CA03.1; requisições diretas e banco indisponível | Formulário contornar validação ou depender do catálogo |

## 5. Coleção, manutenção e sorteio

Cada tarefa deve entregar comportamento observável pela interface, usando os controles anteriores.

| ID / prioridade | Objetivo | Dependências | Critérios de aceitação | Testes previstos | Risco principal |
|---|---|---|---|---|---|
| B15 · P0 | Consultar resultado de gravação incerta | B14 | Consulta autenticada recupera recibo; ausência de recibo mantém incerteza; repetição técnica usa mesmo UUID/dados; resultado histórico não confunde estado atual | CA-ID04, CA-CC04–05; resposta perdida depois do commit e requisição atrasada | Timeout interpretado como falha comprovada |
| B16 · P1 | Apresentar andamento e reconciliação na interface | B15 | Indicar processamento, evitar cliques repetidos e consultar resultado; se consulta falhar, manter incerteza; recarga preserva apenas UUID; oferecer caminho sem JavaScript | CA-UI05, CA-CC04–05; perda de resposta e consulta indisponível no navegador | Novo UUID criar segundo efeito |
| B17 · P1 | Revisar possíveis duplicatas na inclusão | B14 | Sugerir por título/artistas sem provar equivalência; permitir corrigir falso positivo; equivalência confirmada mantém entrada existente e oferece troca de versão; revalidar ao gravar | CA-ID01–03, CA02.4; colaborações, anos diferentes e nomes semelhantes | Unir álbuns distintos ou aceitar equivalência como novo item |
| B18 · P1 | Associar artistas e navegar por agrupamentos | B17 | Principal quando identificado, múltiplos artistas, “Vários artistas”, sugestões sem união automática, homônimos distintos e vazios ocultos; contagem única; ordem alfabética | CA04.1–10; IDs distintos e ordenação no PostgreSQL | Multiplicar a contagem por associação |
| B19 · P1 | Pesquisar a coleção com paginação | B18 | Buscar parte do título ou de qualquer artista, ignorando caixa/acentos/espaços externos; resultado único; vazio mostra coleção navegável; falha difere de nenhum resultado | CA05.1–10, CA09.4; múltiplas páginas e correspondências simultâneas | Pesquisar somente a página atual |
| B20 · P1 | Editar dados do álbum e revisar conflitos | B17, B18 | Corrigir campos/associações sem alterar outros dados; preservar tentativa em conflito e mostrar estado atual; removido não é recriado; equivalência confirmada com outro item bloqueia edição | CA03.2–06, CA03.10–11, CA03.16, CA-CC01–03 | Sobrescrita ou combinação automática |
| B21 · P1 | Cadastrar e renomear serviços | B09, B13, B16 | Exigir apenas nome; impedir duplicidade ignorando caixa/espaços externos e preservando acentos; renomear mantém identidade do serviço | CA06.1–03, CA06.9–10; corrida de nomes equivalentes e falha de gravação | Unicidade garantida apenas pelo formulário |
| B22 · P1 | Associar links seguros e abrir destinos | B14, B21 | HTTPS absoluto com domínio válido; sem credenciais/controles; vários links por serviço; endereço único por álbum após retirar espaços externos; abertura segura em nova aba; sem consultar destino | CA07.1–05, CA07.7–09, CA07.12–13; URLs inseguras e destino indisponível | Executar conteúdo ou alterar endereço válido |
| B23 · P1 | Editar e remover links individualmente | B22 | Alterar endereço/serviço respeitando validade e unicidade; remover somente o vínculo escolhido; preservar álbum, serviços e outros links | CA07.10–11; duplicação por edição e serviço removido | Remover ou alterar vínculos além do escolhido |
| B24 · P1 | Trocar versão preservando álbum e links | B17, B20, B22 | Mesmo ID e quantidade; original intacto; ano específico atualizado ou vazio, sem herdar o anterior; links/endereço/serviço preservados | CA03.7–09, CA03.12, CA07.6; comparar estado antes/depois | Tratar versão como outro álbum |
| B25 · P1 | Excluir álbum com confirmação | B20, B22 | Identificar álbum e ausência de desfazer; cancelar preserva tudo; concluir remove álbum, links e associações, mantendo artistas/serviços/outros álbuns | CA03.4–05, CA03.13–15; rollback e cascatas reais no banco | Exclusão parcial ou de entidades compartilhadas |
| B26 · P1 | Excluir serviço com impacto atualizado | B21, B22 | Mostrar nome e quantidade de links; cancelar preserva dados; confirmar remove serviço/links atomicamente; novo link após confirmação exige revisão | CA06.4–08; duas conexões, ambas as ordens da corrida e cascatas reais | Confirmação desatualizada ou links órfãos |
| B27 · P1 | Sortear uniformemente sobre a coleção inteira | B19, B25 | IDs únicos, chance 1/N, sem filtro por busca/página/artista/link; aceitar repetição; não gravar histórico; removido antes da preparação provoca atualização e novo sorteio | CA08.1–07, CA-CC06–07; fonte aleatória controlada, vazio, um item e remoção concorrente | Favorecer álbuns com vários artistas ou confundir falha com vazio |

B17 oferece a opção de troca; a substituição completa só fica aceita após B24.

## 6. Catálogo externo

| ID / prioridade | Objetivo | Dependências | Critérios de aceitação | Testes previstos | Risco principal |
|---|---|---|---|---|---|
| B28 · P0 | Consultar catálogo com limites compartilhados | B03, B07, B11 | Adaptador de host fixo, timeout, limite de resposta e identificação do cliente; controle de tráfego entre processos; falhas classificadas; nenhuma transação de negócio durante rede | Respostas simuladas: timeout, 503, JSON inválido e duas consultas concorrentes | Ultrapassar limites ou bloquear gravações |
| B29 · P1 | Pesquisar e navegar resultados externos | B28 | Título, artista ou ambos; pesquisa vazia não consulta; exibir anos distintos sem inventá-los; paginação preserva critérios; manual acessível em vazio/falha | CA01.2–03, CA01.7–08, CA01.11–12, CA01.14 | Falha externa apresentada como nenhum resultado |
| B30 · P1 | Revisar e importar resultado selecionado | B16, B17, B18, B24, B29 | Completar/corrigir campos, distinguir grupo/lançamento, não inferir original pela edição; salvar pelo comando existente; importar apenas dados aprovados e nunca atualizar automaticamente | CA01.1, CA01.4–06, CA01.9–10, CA01.13; dados incompletos, equivalência e resposta perdida | Metadados externos contornarem regras locais |

## 7. Operação e aceitação

As verificações desta fase complementam os testes de cada tarefa.

| ID / prioridade | Objetivo | Dependências | Critérios de aceitação | Verificação prevista | Risco principal |
|---|---|---|---|---|---|
| B31 · P0 | Conferir segurança em todos os fluxos | B12, B15, B23–B30 | Proteger páginas, comandos, catálogo e operações; CSRF, saída como texto, consultas parametrizadas, cache privado e erros sem segredos; credenciais com permissões mínimas | CA10.1–12 e RNF06–10; acesso direto, terceiro, cookie revogado e entradas maliciosas | Rota esquecida expor a biblioteca |
| B32 · P1 | Automatizar verificações e rastrear aceitação | B14 | Preparar verificações de unidade/banco, migrações e configuração; poucos fluxos críticos no navegador; mapear cada CA para teste/evidência e registrar pendências | Execução autorizada da automação; revisão da cobertura conforme novas tarefas terminarem | Declarar aceite apenas porque a automação passou |
| B33 · P0 | Produzir cópia consistente e criptografada em teste | B05, B26 | Incluir dados, relações, estado/recibos e versão do esquema; manifesto sem segredos; sessões/tokens excluídos ou invalidados antes de exposição; chave privada fora da aplicação | Gerar, baixar e verificar cópia com biblioteca de teste e conta sem permissão | Arquivo íntegro, mas incompleto ou inacessível |
| B34 · P0 | Demonstrar restauração em banco isolado | B33 | Com autorização específica, recuperar dados/URLs/anos/homônimos; conferir ausência de órfãos; invalidar sessões e trocar geração operacional; formularios antigos recusados; documentar retorno | CA-BK01, CA-BK04–06; comparar ponto recuperado e tentar operação antiga | Reativar sessões ou repetir operações perdidas no backup |
| B35 · P2 | Preparar e publicar piloto restrito | B02, B04, B31, B32, B34 | Preparar configuração HTTPS, banco persistente, permissões, segredos e plano de retorno; publicação e migração só com autorização específica; validar login real | Verificação de saúde, persistência após reinício e acesso negado a terceiro | Estado remoto divergir do ambiente testado |
| B36 · P0 | Demonstrar sete dias de proteção e falha do agendador | B35 | Cópias recuperáveis cobrindo sete dias; medir idade pelo ponto recuperado; demonstrar incidente com perda ≤24 h; validar supervisão e cotas; registrar falhas sem reduzir metas | CA-BK02–04, CA-BK07; atrasos/falhas induzidos e recuperação autorizada | Confiar somente em horários agendados |
| B37 · P2 | Validar interface e persistência nos dois dispositivos | B30, B35 | Galaxy S24 FE/Chrome e Windows/Chrome com versões registradas; 360/1280 px sem rolagem horizontal; teclado, foco, rótulos, erros e estados além da cor; coleção persiste entre sessões/dispositivos | CA-UI01–05, CA09.1–05; inclusão, edição, exclusão, conflito, serviços/links e sorteio | Emulação esconder problema do dispositivo real |
| B38 · P2 | Medir tarefas e avaliar crescimento | B27, B30, B35, B37 | Piloto de 30 álbuns; três tentativas por tarefa/dispositivo; pesquisa ≤15 s e inclusão ≤1 min; registrar cada tempo/falha, rede e aplicação fria/aquecida; avaliar 1.000/10.000 sintéticos sem prometer capacidade | CA-PF01–04; consultas, memória, bloqueios, backup e cotas | Média ocultar falhas ou piloto virar limite de cadastro |
| B39 · P0 | Revisar prontidão para uso definitivo | B31–B38 | Cada CA com evidência; P08/P09/P10/P12/P13 resolvidas ou com decisão explícita; recuperação demonstrada e limitações apresentadas; decisão do proprietário registrada | Auditoria da matriz de aceitação e pendências | Declarar MVP pronto com bloqueador operacional aberto |
| B40 · P3 | Avaliar utilidade do sorteio no uso cotidiano | B39 | Proprietário relata pelo menos três audições escolhidas por sorteio em duas semanas; registrar aprendizado sem criar histórico no produto | Relato do proprietário | Introduzir funcionalidade apenas para medir uso |

B32 começa com a primeira fatia e recebe os testes das seguintes; sua conclusão em B39 exige a matriz completa. B38 deve ser dividida em duas sessões de trabalho: tarefas do usuário e capacidade técnica.

## 8. Ordem recomendada e marcos

A numeração fornece a ordem padrão. As dependências permitem antecipar algumas avaliações sem iniciar funcionalidades bloqueadas.

| Marco | Ordem recomendada | Evidência para encerrar |
|---|---|---|
| M0 — Viabilidade decidida | B01 → B02 → B03 → B04 → B05 | Decisões registradas; limitações encaminhadas |
| M1 — Primeira fatia local | B06 → B07 → B08 → B09 → B10 → B11 → B12 → B13 → B14 | Proprietário entra, cadastra e consulta álbum válido |
| M2 — Coleção utilizável | B15 → B16 → B17 → B18 → B19 → B20 | Repetição segura, revisão de duplicatas, artistas, busca e edição |
| M3 — Manutenção e sorteio | B21 → B22 → B23 → B24 → B25 → B26 → B27 | Links, versões e exclusões preservam integridade; sorteio uniforme |
| M4 — Catálogo integrado | B28 → B29 → B30 | Importação revisável reutiliza regras do cadastro manual |
| M5 — Piloto protegido | B31/B32 concluídos → B33 → B34 → B35 | Segurança conferida e restauração isolada demonstrada |
| M6 — Uso definitivo avaliado | B36 → B37 → B38 → B39 | Recuperação, dispositivos, desempenho e critérios evidenciados |
| M7 — Utilidade observada | B40 | Relato de uso e aprendizado |

B03–B05 antecipam riscos caros de descobrir tarde. B32 acompanha a implementação desde B14. O período de sete dias de B36 pode coincidir com B37/B38, respeitando suas dependências.

Nenhum marco intermediário reduz o escopo aprovado do MVP. Ter cadastro manual funcionando não encerra RF01, RF07 ou os requisitos operacionais.

## 9. Condição comum para concluir uma tarefa

1. Demonstrar os critérios de aceitação e registrar o que foi efetivamente verificado.
2. Executar os testes relevantes e informar falhas ou limitações.
3. Conferir que a tarefa não alterou regras ou arquivos fora do escopo autorizado.
4. Atualizar a rastreabilidade dos CA quando houver implementação.
5. O proprietário explicar a decisão principal com suas palavras.
6. Aguardar sua escolha antes da próxima tarefa.

Não há estimativas em horas: o ritmo inclui aprendizado, configuração e decisões ainda pendentes. Se uma tarefa exigir vários comportamentos independentes, dividi-la antes de implementar.

## 10. Melhorias posteriores e fora do escopo

**Candidatas posteriores, sem aprovação:** exportação/recuperação pela interface, capas e outros metadados; otimização de consultas quando houver medição; revisão por entidade se conflitos independentes forem frequentes; política de descarte de recibos que impeça reexecução antiga.

**Fora do MVP:** sincronização com streaming, descoberta automática de links, reprodução, histórico de audição, recomendações externas, etiquetas, múltiplas coleções, compartilhamento, cadastro público, busca por erros de digitação e funcionamento offline.

Esses itens precisam de análise e aprovação próprias antes de entrar na implementação.

## 11. Próxima ação

**B01 concluída.** A estrutura geral e as cinco decisões foram aprovadas e registradas na seção 13 de `ARCHITECTURE.md`. Na revisão ativa, o proprietário identificou a unicidade do UUID; a mentoria complementou que o servidor precisa reconhecer a operação e devolver seu resultado sem repetir o efeito. O proprietário autorizou o fechamento. As validações técnicas futuras continuam pendentes.

**Próxima tarefa prevista: B02 — avaliar orçamento e infraestrutura candidata**, aguardando decisão do proprietário para iniciar.

Após aprovar as decisões e preparar o ambiente, a primeira microtarefa de código sugerida é um teste de B08: aceitar o ano atual e recusar o seguinte. O proprietário escreve o teste.

**Revisão ativa:** qual a diferença entre impedir duas execuções da mesma solicitação e decidir se duas edições representam o mesmo álbum?

**Evidência da revisão atual:** repositório Git, branch de trabalho e arquivos de preparação inicial conferidos; aprovações explícitas do proprietário registradas com autorização. A presença de configuração de banco, teste e CI não comprova sua execução bem-sucedida. Nenhum teste de aplicação, instalação, integração externa ou deploy foi executado nesta revisão documental.
