# BL-02 — Contrato do arquivo de cópia

**Estado:** BL-02 concluída por revisão documental em 12/11/2026. A exportação e a restauração ainda não foram implementadas.

Referências: [BL-02 no backlog](BACKLOG.md#bl-02--definir-o-contrato-do-arquivo-de-cópia), [requisitos](REQUIREMENTS.md) e [solução escolhida na BL-01](SOLUTION.md).

## 1. Estrutura e identificação

A cópia usa JSON e contém um objeto externo com os seguintes campos:

| Campo | Tipo | Valor ou significado |
| --- | --- | --- |
| `formato` | Texto | Valor fixo `music-library`, que identifica o formato próprio da biblioteca. |
| `versao` | Número inteiro | Valor `1`, que identifica a primeira versão das regras do formato. |
| `albuns` | Lista | Contém os objetos que representam os álbuns da coleção. Pode estar vazia. |

`formato` e `versao` são metadados: informações sobre o arquivo. Todas as cópias desta versão usam os mesmos valores nesses campos, independentemente dos álbuns que contêm. A versão identifica as regras do formato e só muda quando essas regras mudarem.

Cada objeto da lista `albuns` representa um álbum com os três dados aprovados no MVP:

| Campo | Conteúdo |
| --- | --- |
| `titulo` | Texto com o título do álbum. |
| `artista` | Texto com o artista do álbum. |
| `situacao` | Texto com uma das situações: `quero ouvir` ou `já ouvi`. |

Todos os campos das duas tabelas são obrigatórios. O objeto externo aceita somente `formato`, `versao` e `albuns`; cada objeto de álbum aceita somente `titulo`, `artista` e `situacao`. Campos extras, como `genero`, causam a rejeição do arquivo inteiro, mesmo quando os campos conhecidos são válidos.

Os tipos devem corresponder ao contrato, sem conversão automática: não aceitar campos ausentes, `null`, números no lugar de textos, um objeto no lugar da lista `albuns` ou itens dessa lista que não sejam objetos. `versao` deve ser o número inteiro `1`, não o texto `"1"`, um booleano ou um número decimal. A raiz do JSON deve ser um objeto, não uma lista.

## 2. Exemplo com dois álbuns

O exemplo elaborado na mentoria representa as duas situações de escuta:

```json
{
    "formato": "music-library",
    "versao": 1,
    "albuns": [
        {
            "titulo": "2112",
            "artista": "Rush",
            "situacao": "já ouvi"
        },
        {
            "titulo": "Transcendence",
            "artista": "Crimson Glory",
            "situacao": "quero ouvir"
        }
    ]
}
```

## 3. Coleção vazia

Uma cópia vazia mantém a identificação e a versão. O campo `albuns` contém uma lista vazia:

```json
{
    "formato": "music-library",
    "versao": 1,
    "albuns": []
}
```

O arquivo continua tendo um objeto externo; a lista vazia aparece como valor de `albuns`.

## 4. Política de compatibilidade

Esta versão da aplicação reconhecerá apenas o formato `music-library` na versão inteira `1`. A extensão `.json` e a sintaxe JSON válida, sozinhas, não identificam uma cópia própria compatível.

Se a identificação ou a versão estiver ausente ou for incompatível, a restauração deverá rejeitar o arquivo inteiro, informar o motivo em português e preservar integralmente a coleção atual. Por exemplo, um arquivo com `versao` igual a `2` deverá ser rejeitado, pois suas regras ainda não são conhecidas pela aplicação.

Nenhum registro de um arquivo incompatível poderá ser aproveitado para restauração parcial. Reconhecer o formato e a versão é apenas uma etapa: todos os registros ainda precisarão ser validados antes de permitir a substituição da coleção, conforme RN-12 e CA-30.

Este exemplo tem sintaxe JSON válida, mas é incompatível por declarar a versão `2`:

```json
{
    "formato": "music-library",
    "versao": 2,
    "albuns": []
}
```

O arquivo deve ser rejeitado sem substituir a coleção atual, informando em português que a versão não é suportada. Não há conversão de versões nem importação de formatos externos nesta entrega.

## 5. Validação dos campos e preservação da grafia

Antes de permitir a substituição, validar todos os registros segundo estas regras:

| Campo | Validação |
| --- | --- |
| `titulo` | Texto obrigatório. Retirar espaços no início e no fim; depois, exigir pelo menos um caractere visível e no máximo 200 caracteres. |
| `artista` | Texto obrigatório, com a mesma regra de remoção de espaços nas pontas, presença de caractere visível e limite de 200 caracteres. |
| `situacao` | Texto com exatamente um dos valores `quero ouvir` ou `já ouvi`. Não normalizar nem corrigir esse valor. |

**Decisão confirmada na mentoria:** para título e artista, verificar o limite depois de retirar os espaços nas pontas. Assim, 200 caracteres válidos cercados por espaços são aceitos; 201 caracteres restantes são rejeitados. Não truncar o texto nem reduzir espaços internos para fazê-lo caber no limite. Um campo vazio ou só com espaços é inválido.

Preservar maiúsculas, minúsculas, acentos e espaços internos de título e artista para gravação, exportação e exibição. A única alteração nesses valores é a retirada de espaços nas pontas. A normalização da seção seguinte serve somente para comparação. Por exemplo, ` Álbum  Exemplo ` deve ser restaurado como `Álbum  Exemplo`, mantendo o acento, a caixa e os dois espaços internos.

Situações como `Já ouvi`, `ja ouvi`, `quero ouvir `, texto vazio ou qualquer outro valor são inválidas. Não usar uma situação padrão para substituir uma entrada ausente ou inválida.

Qualquer erro de estrutura, tipo, campo ou valor rejeita o arquivo inteiro, mesmo que os demais álbuns sejam válidos. A mensagem deve informar o motivo em português, identificando o registro e o campo quando aplicável; erros de comprimento devem informar o limite de 200 caracteres. Não descartar registros inválidos nem restaurar somente a parte válida.

Não há um limite máximo de 10.000 álbuns no contrato. Esse é o volume aprovado para verificar a capacidade da aplicação, não uma regra de rejeição do registro seguinte. Não se acrescenta uma promessa de capacidade já medida.

## 6. Duplicatas dentro da cópia

A cópia não pode conter dois álbuns com o mesmo par de título e artista após a comparação aprovada na seção 3 dos requisitos e em RN-07:

- Ignorar diferenças entre maiúsculas e minúsculas e entre letras com e sem acentos.
- Desconsiderar espaços nas pontas e tratar sequências de espaços internos como um único espaço na comparação.
- Comparar título e artista em conjunto, independentemente da situação de escuta.

O mesmo título com artistas diferentes é permitido. Um nome de artista composto continua sendo um único texto; não separar participantes nem acrescentar campos de identificação ou edição do álbum.

Verificar duplicatas apenas entre os registros da cópia. Um álbum equivalente na coleção atual não invalida o arquivo, pois a restauração substitui essa coleção integralmente. Ao encontrar uma duplicata interna, rejeitar o arquivo inteiro e explicar o motivo; não escolher um dos registros, eliminar duplicatas automaticamente ou mesclar situações.

## 7. Exportação e substituição da coleção

### 7.1. Exportação completa

Exportar todos os registros salvos com seus títulos, artistas e situações, inclusive os ocultos por artista, busca ou filtro de situação. Usar a grafia salva, sem aplicar a normalização de comparação aos valores exportados. Uma coleção vazia gera a cópia válida da seção 3.

A exportação não altera a coleção. Confirmar sua geração somente depois de ler a coleção integralmente e gerar o arquivo completo. Se a leitura ou a geração falhar, informar que a cópia não foi concluída, sem confirmar sucesso nem apresentar uma cópia parcial como completa. A geração do arquivo não comprova que o usuário o guardou.

### 7.2. Restauração confirmada

1. Ler e validar o arquivo inteiro: sintaxe JSON, estrutura, identificação, versão, campos, tipos, limites, situações e duplicatas internas. Arquivo ilegível, incompatível ou inválido não altera a coleção atual.
2. Após a validação, informar que a restauração substituirá toda a coleção atual, sem mesclar, e exigir confirmação explícita antes de gravar. Permitir cancelar preservando os registros anteriores, sem confirmar restauração.
3. Exigir a mesma confirmação para uma cópia vazia, avisando que a substituição deixará a biblioteca sem álbuns.
4. Após a confirmação, substituir todos os registros em uma única transação, conforme a estratégia da seção 3 de [SOLUTION.md](SOLUTION.md#3-gravação-integral-e-restauração). Uma transação confirma todas as alterações ou desfaz a operação inteira; a remoção dos dados anteriores não pode ser confirmada separadamente da inserção dos novos.
5. Confirmar a restauração somente após concluir a gravação integral. A coleção deve conter exatamente os álbuns da cópia, com a grafia de exibição definida neste contrato, inclusive ao encerrar e reabrir a aplicação.

Se ocorrer falha durante a substituição ou na confirmação da transação, informar que a restauração não foi salva, não confirmar sucesso e preservar integralmente a coleção anteriormente confirmada, inclusive após reabrir. Não deixar mistura de coleções, substituição parcial ou uma biblioteca vazia causada pela falha.

## 8. Exemplos de arquivos inválidos

Os exemplos abaixo têm sintaxe JSON válida e identificação compatível, mas violam as regras dos registros. Ambos devem ser rejeitados integralmente, preservando a coleção atual.

### 8.1. Título obrigatório vazio

```json
{
    "formato": "music-library",
    "versao": 1,
    "albuns": [
        {
            "titulo": "",
            "artista": "Rush",
            "situacao": "já ouvi"
        }
    ]
}
```

O campo existe e é texto, mas está vazio. Informar que o título do primeiro álbum precisa ser preenchido; não criar um registro parcial. Um título só com espaços também é inválido após retirar os espaços nas pontas.

### 8.2. Duplicata após a normalização

```json
{
    "formato": "music-library",
    "versao": 1,
    "albuns": [
        {
            "titulo": "Álbum  Exemplo",
            "artista": "Artista A",
            "situacao": "quero ouvir"
        },
        {
            "titulo": " album exemplo ",
            "artista": "ARTISTA A",
            "situacao": "já ouvi"
        }
    ]
}
```

Os pares de título e artista são equivalentes na comparação. A diferença de situação não torna os álbuns distintos. Informar a duplicidade e rejeitar a cópia inteira, sem aproveitar apenas um dos registros.

## 9. Revisão documental da BL-02

Na revisão de 12/11/2026, os cinco exemplos foram lidos com `json.loads` do Python 3.12.3, confirmando sua sintaxe JSON. Também foram conferidos os arquivos das referências locais e, por leitura, a validade ou o motivo de rejeição de cada exemplo, as regras de campos e a correspondência com os seguintes cenários dos requisitos:

| Referência | Regra contemplada no contrato |
| --- | --- |
| CA-26 — Exportação completa | Seções 1, 2 e 7.1: todos os dados salvos, inclusive registros ocultos por filtros, sem alterar a coleção. |
| CA-27 — Falha de exportação | Seção 7.1: falha de leitura ou geração não confirma sucesso nem apresenta uma cópia parcial como completa. |
| CA-28 — Restauração válida | Seção 7.2: validar, confirmar, substituir integralmente, confirmar após salvar e recuperar os mesmos dados ao reabrir. |
| CA-29 — Cancelamento | Seção 7.2: cancelar preserva a coleção anterior sem gravar ou confirmar restauração. |
| CA-30 — Arquivo inválido | Seções 1, 4, 5, 6 e 8: rejeição integral por incompatibilidade, campos, tipos, limites, situações ou duplicatas, preservando os dados anteriores. |
| CA-31 — Falha de restauração | Seção 7.2: desfazer toda a substituição em falha, inclusive ao confirmar a transação; preservar os dados após reabertura. |
| Cópia vazia — seção 8 dos requisitos | Seções 3 e 7: exportar a lista vazia e exigir confirmação explícita antes de substituir a coleção por ela. |

Na revisão documental, foram conferidas as regras para campos ausentes ou extras em ambos os níveis, `null`, tipos incorretos e situações não permitidas. Também foram conferidos os resultados especificados abaixo para título e artista; esta tabela não representa testes executados de um validador:

| Entrada, com os demais campos válidos | Resultado previsto |
| --- | --- |
| Texto vazio ou só com espaços | Rejeitar a cópia inteira. |
| Texto válido com 200 caracteres após retirar espaços nas pontas | Aceitar, preservando os espaços internos e a grafia. |
| Texto válido com 200 caracteres cercados por espaços nas pontas | Aceitar após retirar os espaços nas pontas. |
| Texto com 201 caracteres após retirar espaços nas pontas | Rejeitar sem truncar, identificando o campo e o limite. |
| Mesmo título e artista equivalentes, com situações diferentes | Rejeitar por duplicata interna. |
| Mesmo título com artistas diferentes | Aceitar os dois registros. |

**Resultado da revisão:** os critérios documentais da BL-02 estão contemplados, com exemplos de cópia válida, vazia, incompatível e inválida, regras de validação integral e correspondência com CA-26 a CA-31 e o caso de cópia vazia. As decisões de contar caracteres após retirar espaços nas pontas e rejeitar campos extras foram confirmadas pelo usuário. Este registro define o contrato; exportação, validação e restauração ainda não foram implementadas nem verificadas em execução. A preservação dos dados em falhas, a capacidade e a compatibilidade com os navegadores permanecem nas tarefas correspondentes do backlog.
