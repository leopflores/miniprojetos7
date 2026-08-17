#Importação das bibliotecas
import pandas as pd
import numpy as np
from IPython.display import display

#Lietura do CSV utilizando pandas
df = pd.read_csv("dados/Base Varejo.csv")

#O CSV utiliza como separador ponto e vírgula e não vírgula, portanto teremos que definir isso na função de leitura

df = pd.read_csv("dados/Base Varejo.csv",sep=";")


#Vamos Analisar o conteúdo da nossa base:

display(df.shape,'\n\n')
#Possuímos 830000 registros distribuídos em 14 colunas

display(df.columns,"\n\n")
#A base contém comlunas de:
# Data, 
# CO_ID (ID da Compra),
# CL_ID (ID do Cliente),
# CL_GENERO (Genero do Cliente), 
# CL_EC ( Estado civil do cliente:
# 1: Casado ou união estával;
# 2: Divorciado;
# 3: Separado;
# 4. Solteiro;
# 5: Viúvo),
# CL_FHL (Número de filhos do cliente),
# CL_SEG (Segmentação econômica do cliente (classe A, B ou C)),
# PR_ID (ID do Porduto),
# PR_CAT (Catetgoria do Produto),
# PR_NOME (Nome do Produto) e Quatro colunas Não nomeadas

#Vamos verificar o tipo de dados existentes nessas colunas:
display(df.dtypes,"\n\n")
#Podemos verificar que a coluna de data está em formato de str, tentaremos transoformar a coluna de data para datetime, observando a fomatação:
df['DATA'] = pd.to_datetime(
    df['DATA'],
    format='%d/%m/%Y')

#Verificando se funcionou:
display(df.dtypes,"\n\n")
#A coluna DATA está com o formato correto agora

#Vamos observar nossas colunas sem nomenclantura e verificar se podemos excluí-las:

print(f'Checar se todos os valores são nulos nas colunas \nUnamed:10 - {df['Unnamed: 10'].isnull().all()}\nUnamed:11 - {df['Unnamed: 11'].isnull().all()}\nUnamed:12 - {df['Unnamed: 12'].isnull().all()}\nUnamed:13 - {df['Unnamed: 13'].isnull().all()}')

#De fato todos os valores são nulos, então iremos removê-las
df.drop(columns=['Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13'],inplace=True)
print('\n\n',df.columns,'\n\n')

#Certo, agora possuímos apenas as colunas que nos interessam. Observando o tipo de cada uma agora, tentaremos verificar se há erros e tratá-los:
print(f'Contagem de valores nulos por coluna: \n{df.isnull().sum()} \n\n')
print(f'Contagem de valores não pertencentes ao Dtype por coluna: \n{df.isna().sum()} \n\n')

#O valor vindo como #N/D de arquivos csv ou excel pode não ser interpretado como nulo pelo pandas, por isso, vale realizar a transformação destes para Nan ou nulo:
df = df.replace('#N/D', np.nan)
print(f'Contagem de valores nulos por coluna com substituição do N/D: \n{df.isnull().sum()} \n\n')

#Agora sim esses valores apareceram como NAN nas categorias de produto, vamos avaliar eles
display(df[df['PR_CAT'].isna()])
#Vamos verificar se há outros produtos pertencentes ao ID 107
display(df[df['PR_ID']==107]
        .groupby('PR_NOME',dropna=False)
        .size()
        )
#Não, somente o NaN, então podemos removê-los:
df.dropna(subset=['PR_CAT'], inplace=True)
print(f'Removidos {df['PR_CAT'].isna().sum()} registros NaN')

#Removemos os valores NAN. Agora vamos checar por valores repetidos
print(f'Quantidade de linhas idênticas (duplicadas): {df.duplicated().sum()}\n')
display(df[df.duplicated()])
#Obtemos 96553 linhas repetidas. Ao que me parece, esses registros repetidos são erros, visto que não há coluna de quantidade de produtos, portanto a informação que temos é que o cliente CL_ID, na compra CO_ID, realizada na data DATA, obteve determinado produto e essa informação repetida não nos é valiosa.
# Dito isso, iremos remover as duplicatas mantendo o primeiro valor
df.drop_duplicates(keep='first',inplace=True)
print(df.shape)
print(f'Removidas {830000 - df.shape[0]} linhas do Dataframe')

#Com nossas duplicatas removidas, consideraremos a base limpa e partiremos para nossa análise:
#1. Analisar estatísticas da coluna CL_FHL:
print(f'\nEstatísticas da coluna de número de filhos dos clientes: \n{df['CL_FHL'].describe()}\n\n')
#Essa análise demonstra os resuiltados estatísticos dos filhos por cliente ponderando-os sobre o número de registros na tabela. Isto é, clientes com mais registros irão ter mais peso nessas estatísticas.
#Se, por outro lado, quisermos analisar a distribuição de número de filhos dos clientes desconsiderando o peso do número de registros, devemos capturar todos os valores únicos de CL_ID e daí então rodar o método describe na coluna de número de filhos:

clientes = df[['CL_ID','CL_FHL']]
cliente_filtrado = clientes.drop_duplicates(subset='CL_ID')
print(f'Estatísticas de número de filhos de clientes não ponderado:\n{cliente_filtrado['CL_FHL'].describe()}\n\n')

#Apesar dessa diferente interpretação, os resultados coincidentemente foram bem similares.A contagem é de registros foi de 733447 para 1000, o que indica que possuímos 1000 clientes distintos em nossa base
#Uma média de 1,13 filho por cliente, com desvio padrão significativo, e verifica-se que a maior parte de nossos clientes não possuem filhos


#2. Padrões de agrupamento
#Para análise de padrões de agrupamento, vamos analisar quantidade de registros por gênero, por categoria de produtos e por classe econômica
#2.1Primeiramente analisaremos os agrupamentos e dados individuais:
#Gênero:
print(df.groupby(['CL_GENERO']).size())
porcentagem_m = ((df['CL_GENERO']=='M').sum()/len(df)) * 100
porcentagem_f = ((df['CL_GENERO']=='F').sum()/len(df)) * 100
print(f'\nPorcentagem de registros Masculino: {porcentagem_m:.2f}%')
print(f'Porcentagem de registros Feminino: {porcentagem_f:.2f}%\n\n')
#Portanto a maioria de nossos clientes são do Gênero Feminino

#Categoria de Produtos:
print(df.groupby(['PR_CAT']).size())
porcentagem_ac = ((df['PR_CAT']=='ACESSORIOS').sum()/len(df)) * 100
porcentagem_al = ((df['PR_CAT']=='ALIMENTOS').sum()/len(df)) * 100
porcentagem_be = ((df['PR_CAT']=='BEBIDAS').sum()/len(df)) * 100
porcentagem_hi = ((df['PR_CAT']=='HIGIENE').sum()/len(df)) * 100
porcentagem_li = ((df['PR_CAT']=='LIMPEZA').sum()/len(df)) * 100
porcentagem_pe = ((df['PR_CAT']=='PET').sum()/len(df)) * 100
print(f'\nPorcentagem de registros ACESSORIOS: {porcentagem_ac:.2f}%')
print(f'Porcentagem de registros ALIMENTOS: {porcentagem_al:.2f}%')
print(f'Porcentagem de registros BEBIDAS: {porcentagem_be:.2f}%')
print(f'Porcentagem de registros HIGIENE: {porcentagem_hi:.2f}%')
print(f'Porcentagem de registros LIMPEZA: {porcentagem_li:.2f}%')
print(f'Porcentagem de registros PET: {porcentagem_pe:.2f}%\n\n')
#Verificamos que mais da metade dos registros advém da compra de alimentos (52,38%) e que apenas 1,75% deles advém de acessorios

#Classe Econômica:
print(df.groupby(['CL_SEG']).size())
porcentagem_a = ((df['CL_SEG']=='A').sum()/len(df)) * 100
porcentagem_b = ((df['CL_SEG']=='B').sum()/len(df)) * 100
porcentagem_c = ((df['CL_SEG']=='C').sum()/len(df)) * 100
print(f'Porcentagem de registros Classe A: {porcentagem_a:.2f}%')
print(f'Porcentagem de registros Classe B: {porcentagem_b:.2f}%')
print(f'Porcentagem de registros Classe C: {porcentagem_c:.2f}%\n')
#Verificamos que a maior parte de nossos clientes pertencem a classe B

#2.2.Verificaremos agora a relação entre essas categorias utilizando o pivot_tables:
#Vamos verificar se há relação entre classe econÇomica de cliente e categoria de produto

#Número de registros contados e distribuídos pela relação segmento de classe econômica do cliente e categoria de produto
tabela_seg_cat = df.pivot_table(
    index='CL_SEG',
    columns='PR_CAT',
    aggfunc='size'
    )

#Calculo do percentual de cada categoria pela linha de classe econômica:
tabela_percentual = tabela_seg_cat.div(tabela_seg_cat.sum(axis=1), axis=0) * 100
display(tabela_percentual,'\n')
#Verifca-se que não há tendência de categorias de produto em função da classe econômica

#Agora, verificaremos se há relação entre gênero e categorias de produto, utilizando o mesmo método:
tabela_gen_cat = df.pivot_table(
    index='CL_GENERO',
    columns='PR_CAT',
    aggfunc='size'
    )
tabela_percentual = tabela_gen_cat.div(tabela_gen_cat.sum(axis=1), axis=0) * 100
display(tabela_percentual,'\n')
#Também não apoarenta haver tendências

#Finalmente, verificaremos se há relação entre genero e classe econômica:
tabela_gen_seg = df.pivot_table(
    index='CL_GENERO',
    columns='CL_SEG',
    aggfunc='size'
    )
tabela_percentual = tabela_gen_seg.div(tabela_gen_seg.sum(axis=1), axis=0) * 100
display(tabela_percentual)
#Aqui, uma leve tendência parece indicar que há mais pessoas do gênero feminino pertencentes a classe C do que pessoas do gênero masculino. Entretanto a percentagem de pessoas pertencentes à classe A é bastante similar

