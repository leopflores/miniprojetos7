# Mini-Projeto Avaliativo
### Módulo 1 · Semana 07 · Turma Analise_de_Dados

Análise Exploratória de Dados (AED) aplicada à base **Varejo**, contendo registros de compras (datas, clientes, produtos, categorias e valores), com o objetivo de identificar problemas de qualidade, tratá-los e extrair estatísticas e padrões de agrupamento relevantes para o negócio.

## Como executar

1. Coloque o arquivo `Base Varejo.csv` na pasta `dados/`.
2. Instale as dependências: `pip install pandas numpy`.
3. Rode no VS Code `python main.py`.

## Pipeline realizado

1. **Carga e inspeção** — leitura do CSV (separador `;`), verificação de shape (830.000 registros × 14 colunas), nomes e tipos de coluna.
2. **Identificação de problemas** — quatro colunas `Unnamed` 100% vazias, valores `#N/D` não reconhecidos como nulos pelo pandas (mascarando 3.650 nulos em `PR_CAT`/`PR_NOME`) e 96.553 linhas totalmente duplicadas.
3. **Limpeza**
   - Remoção das colunas `Unnamed: 10–13` (100% nulas).
   - Conversão de `#N/D` para `NaN` e remoção das linhas sem categoria de produto (`PR_CAT`), já que pertenciam todas a um único produto sem nome cadastrado.
   - Conversão de `DATA` de texto para `datetime` (`%d/%m/%Y`).
   - Remoção de duplicatas exatas, mantendo a primeira ocorrência — justificado pela ausência de coluna de quantidade, o que torna uma linha repetida uma informação redundante, não uma nova compra do mesmo item.
4. **Estatística descritiva** — `CL_FHL` (número de filhos do cliente), calculada tanto por registro quanto por cliente único (`CL_ID` deduplicado), para evitar viés de clientes com mais compras.
5. **Agrupamentos** — contagens e percentuais por gênero, categoria de produto e segmento econômico, além de tabelas cruzadas (`pivot_table`) gênero × categoria, segmento × categoria e gênero × segmento.

## Reflexão teórica — ETL e qualidade de dados

O processo seguiu as três etapas clássicas de ETL: **Extração** (leitura do CSV bruto), **Transformação** (padronização de tipos, tratamento de nulos "camuflados" e remoção de duplicatas) e **Carga** (dataframe limpo pronto para análise/dashboard). O ponto mais relevante do exercício foi perceber que qualidade de dados não é só "contar nulos": o valor `#N/D` só foi identificado como ausente porque o `pandas` não reconhece esse marcador automaticamente — sem essa etapa, 3.650 registros sem categoria teriam sido tratados como dados válidos. Da mesma forma, duplicatas exatas só fazem sentido como erro de lançamento porque o esquema da tabela não tem coluna de quantidade. Em outra modelagem de dados, a mesma linha repetida poderia ser legítima. Isso reforça que decisões de limpeza dependem do contexto de negócio, não apenas de regras genéricas.

## Principais insights

- A base final ficou com aproximadamente 730 mil registros de compra, referentes a 1.000 clientes únicos, após remover linhas sem categoria de produto e duplicatas exatas.
- **Alimentos domina o mix de vendas**: cerca de 52% de todos os itens comprados pertencem à categoria ALIMENTOS, seguida por HIGIENE (~19%) e LIMPEZA (~18%). ACESSORIOS é a menos relevante (~1,8%).
- **Perfil familiar dos clientes**: a maioria não tem filhos (moda = 0), com média de ~1,1 filho por cliente e alta dispersão (desvio padrão > 1,4), indicando um público heterogêneo.
- **Leve maioria feminina**: ~52% dos registros vêm de clientes do gênero F contra ~48% de M, mas a diferença não é grande o suficiente para indicar um público fortemente segmentado por gênero.
- **Classe econômica concentrada em B**: ~64% dos registros pertencem ao segmento B, ~28% ao C e apenas ~8% ao A.
- **Categoria de produto não varia por classe social nem por gênero**: as tabelas cruzadas mostram percentuais de categoria praticamente idênticos entre segmentos A/B/C e entre F/M — ou seja, classe econômica e gênero não parecem influenciar o que é comprado. A única tendência levemente perceptível é uma proporção maior de mulheres na classe C frente aos homens.

## Limitações e problemas remanescentes

- **Sem análise temporal**: a base cobre compras de fevereiro/2019 a agosto/2022, mas o script não explora variação de vendas ao longo do tempo (por mês/ano).
- **Coluna `CL_EC` (estado civil) não explorada**: nenhum agrupamento usa essa dimensão. Poderia revelar padrões de consumo por estado civil que não foram testados.
- **Sem verificação explícita de valores fora do esperado**: não há checagem programática de datas fora do intervalo do negócio. A base aparenta estar limpa nesse aspecto, mas isso não foi validado com código.
