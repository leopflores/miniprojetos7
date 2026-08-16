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
#Podemos verificar que a coluna de data está em formato de str, tentaremos transoformar a coluna de data para datetime, observando a fomatação e lidando com possíveis erros:
df['DATA'] = pd.to_datetime(
    df['DATA'],
    format='%d/%m/%Y')

display(df.dtypes,"\n\n")