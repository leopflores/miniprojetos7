#Importação das bibliotecas
import pandas as pd
import numpy as np
import matplotlib as plt
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
print(f'Contagem de valores não nulos por coluna: \n{df.isnull().sum()} \n\n')
print(f'Contagem de valores não pertencentes ao Dtype por coluna: \n{df.isna().sum()} \n\n')

#Verificamos que não há valores nulos nem não pertencetes ao dtype de cada coluna. Agora vamos checar por valores repetidos
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
print(f'Estatísticas de número de filhos de clientes não ponderado:\n{cliente_filtrado['CL_FHL'].describe()}')

#Apesar dessa diferente interpretação, os resultados coincidentemente foram bem similares.A contagem é de registros foi de 733447 para 1000, o que indica que possuímos 1000 clientes distintos em nossa base
#Uma média de 1,13 filho por cliente, com desvio padrão significativo, e verifica-se que a maior parte de nossos clientes não possuem filhos


