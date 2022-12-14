#!/usr/bin/env python
# coding: utf-8

#BIBLIOTECAS
from github import Github
from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import lxml
import numpy as np
import util as util
from util import *
from upload import *

def obtem_ano_anterior(): 
    data_atual = datetime.now()
    ano_anterior = data_atual.year-1
    mes_atual = data_atual.month
    ano_atual = data_atual.year

    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.24364/dados?formato=json&dataInicial=01/01/{0}&dataFinal=01/{1}/{2}'
    url = url.format(ano_anterior, mes_atual, ano_atual)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data_ibc = json.loads(soup.text)
    ano_anterior = int(data_ibc[-1]['data'][6:10]) - 1

    return str(ano_anterior)

#################################################
#Acesso a API do Governo

data_atual = datetime.now()
ano_anterior = str(int(obtem_ano_anterior()) - 1)
mes_atual = data_atual.month
ano_atual = data_atual.year

url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.24364/dados?formato=json&dataInicial=01/01/{0}&dataFinal=01/{1}/{2}'
url = url.format(ano_anterior, mes_atual, ano_atual)
print(url)
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
data_ibc = json.loads(soup.text)
df_ibc = pd.DataFrame(data_ibc)
print('- Dados extraídos')
#################################################
#O trecho a seguir é responsável por calcular a variação mensal. 

df_ibc["valor"] = pd.to_numeric(df_ibc["valor"])

shifted = df_ibc['valor'].shift(1) #realiza o deslocamento de linhas (desloca uma linha)
df_ibc['variacao_mensal'] = ((df_ibc['valor'] - shifted) / shifted)*100

df_ibc['data'] =  pd.to_datetime(df_ibc['data'], format="%d/%m/%Y")
df_ibc['ano'] = df_ibc['data'].apply(lambda x: str(x)[:4])
df_ibc['mes'] = df_ibc['data'].apply(lambda x: str(x)[5:7])
df_ibc = df_ibc[['data', 'variacao_mensal']] 

df_ibc['data'] = df_ibc['data'].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
df_ibc = df_ibc[-24:]

#####serie
serie_ibc = []
for i, row in df_ibc.iterrows():
  if row[0][:4] >= '2020':
    serie_ibc.append({'x': row[0], 'y': round(float(row[1]), 2)})
#####

meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

print('Série criada')

periodos = list(df_ibc['data'])
valores = list(df_ibc['variacao_mensal'])
ano = str(periodos[0])[:4]
mes = str(periodos[0])[5:7]

data_ibc = json.loads(soup.text)
df_ibc = pd.DataFrame(data_ibc)
df_ibc['data'] =  pd.to_datetime(df_ibc['data'], format="%d/%m/%Y")
df_ibc['ano'] = df_ibc['data'].apply(lambda x: str(x)[:4])
df_ibc['mes'] = df_ibc['data'].apply(lambda x: str(x)[5:7])
del df_ibc['data']
test = df_ibc.tail(1)
mes_atualizacao_db = ((test['mes']).astype(int)).tolist()
df_ibc = df_ibc.groupby("ano").head(mes_atualizacao_db)

numero_mes_referencia = int(mes_atualizacao_db[0])
mes_referencia = meses_ano[numero_mes_referencia-1]

ano_ref = np.unique(df_ibc['ano'])[-1]

if mes_referencia == 'Jan':
    referencia = mes_referencia + '/' + ano_ref
else:
    referencia = 'Jan-'+mes_referencia + '/' + ano_ref 

df_ibc['valor'] = df_ibc['valor'].astype(float)
df_ibc = df_ibc.groupby(['ano']).mean()
#acumulado por ano
indice_ano_atual = (df_ibc['valor'][2]/df_ibc['valor'][1] -1 )*100 
indice_ano_atual = round(indice_ano_atual,2)

#variacao = ((soma_periodo_anterior/ soma_periodo_atual) -1) /100
# indice_ano_anterior = (df_ibc['valor'][1]/df_ibc['valor'][0] -1 )*100 
# indice_ano_anterior = round(indice_ano_anterior,2)

# valor_periodo_atual = serie_ibc[-2:][1]['y']
# valor_periodo_anterior = serie_ibc[-2:][0]['y']

if indice_ano_atual > 0:
    direcao = 'up'
    cor_valor = "green"
elif indice_ano_atual < 0:
    direcao = 'down'
    indice_ano_atual = str(indice_ano_atual)
    indice_ano_atual = indice_ano_atual[1:]
    cor_valor = "red"
else:
    direcao = 'left'

print('- Valor do cartão armazenado')
#################################################
#Criação do JSON
ibc_json = {
    'nome': 'Índice de Atividade Econômica',
    'descricao': 'Variação percentual em relação ao mesmo período do ano anterior',
    'fonte': 'BACEN',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(indice_ano_atual)+'%',
            'direcao': direcao,
            'cor_valor': cor_valor,
            'cor_seta': 'orange',
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': referencia,
            'y_label': {
                    'prefixo_sufixo': 'sufixo',
                    'label': '%',
            },
            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': serie_ibc,
        }
    ]
}

path_save_json = util.config['path_save_json']['path']

with open(path_save_json+'ibc.json', 'w', encoding='utf-8') as f:
    json.dump(ibc_json, f, ensure_ascii=False, indent=4)

print(' JSON armazenado')

######################################################
#Upload para o github
upload_files_to_github('ibc')
print('- JSON enviado para o GitHub')