
from mmap import ACCESS_COPY
from re import ASCII
from telnetlib import NEW_ENVIRON
from pandas._libs.tslibs import timestamps
from pandas.io import api
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import numpy as np
from datetime import datetime
import util as util
from util import *
from upload import *
from github import Github
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bd
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import time

# driver.quit()
driver = webdriver.Chrome(executable_path="G:/IEL/OBSERVATORIO/ETL/panorama economico/chromedriver_win32/chromedriver.exe")
driver.get("https://extra-ibre.fgv.br/ibre/sitefgvdados/default.aspx?Convidado=S")
time.sleep(25)
driver.find_element_by_id('dlsCatalogoFixo_imbOpNivelUm_2').click()
time.sleep(10)
driver.find_element_by_id('dlsCatalogoFixo_imbOpNivelDois_3').click()
time.sleep(10)
driver.find_element_by_id('dlsMovelCorrente_imbIncluiItem_2').click()
time.sleep(10)
driver.find_element_by_id('butCatalogoMovelFecha').click()
time.sleep(10)
driver.find_element_by_id('cphConsulta_rbtSerieHistorica').click()
time.sleep(10)
driver.find_element_by_id('cphConsulta_butVisualizarResultado').click()
time.sleep(10)
driver.get("https://extra-ibre.fgv.br/IBRE/sitefgvdados/VisualizaConsultaFrame.aspx")

time.sleep(10)
html = driver.page_source
driver.quit()

soup = b
(html, "html.parser") 
table = soup.find_all('table')
df = pd.read_html(str(table[0]))[1]
df.columns = ['ano', 'valor']
df = df.iloc[-100:]
df.reset_index(drop=True, inplace=True)
df['valor'] = pd.to_numeric(df['valor'])
df['valor'] = df['valor']/100
indice_inicio_serie = df.ano[df.ano == '01/2020'].index.tolist()[0]
indice_inicio_serie = len(df)-indice_inicio_serie
df = df.iloc[-indice_inicio_serie:]


json_igpm = []


for index, row in df.iterrows():
    print(row['ano'])
    mes = pd.to_datetime(row['ano'], format='%m/%Y', errors='coerce')
    mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")
    #mensal = str(row['mensal']).replace(".", ",")
    valor = float(row['valor'])
    json_igpm.append({'x': mes, 'y': valor})


newlist = sorted(json_igpm, key=lambda k: k['x']) 
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

referencia = newlist[-1:][0]['x']
ano = referencia[:4]
mes = int(referencia[5:7])
referencia = meses_ano[mes - 1] + '/' + ano

valor_cartao = newlist[-1:][0]['y']
print('- Valor do cartão armazenado')                                                                               
valor_periodo_atual = float(newlist[-2:][1]['y'])                                                                               
                                                                               
if valor_periodo_atual > 0:                                                                               
  direcao = 'up'                                                                               
  cor_valor = 'green'                                                                              
elif valor_periodo_atual < 0:                                                                         
  direcao = 'down'                                                                               
  cor_valor = 'red'                                                                                
  valor_cartao = str(valor_cartao)[1:]                                                                               
                                                                              
else:                                                                               
  direcao = 'right'
  cor_valor = 'gray'

json_igpm = {
    'nome': 'Índice Geral de Preços Mercado (IGP-M)',
    'descricao': 'Variação mensal',
    'fonte': 'FGV',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(valor_cartao)+'%', 
            'direcao': direcao,
            'cor_valor': cor_valor,
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': referencia,
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%'
            },

            'serie_labels': {
                'x': 'Data',
                'y': 'Variação',
            },

            'serie': newlist,
        },       
    ]
}


path_save_json = util.config['path_save_json']['path']
name_json = 'igpm'

with open(path_save_json + name_json +'.json', 'w', encoding='utf-8') as f:
    json.dump(json_igpm, f, ensure_ascii=False, indent=4)
print('- JSON armazenado')

###################################################
#Upload
upload_files_to_github(name_json)
print('- JSON enviado para o GitHub') 

 
#def retorn_num_mes(mes_nome):
   #if mes_nome == 'Janeiro':
    # return '01'
   #if mes_nome == 'Fevereiro':
    # return '02'
   #if mes_nome == 'Março':
    # return '03'
   #if mes_nome == 'Abril':
    # return '04'
   #if mes_nome == 'Maio':
    # return '05'
   #if mes_nome == 'Junho':
    # return '06'
   #if mes_nome == 'Julho':
    # return '07'
   #if mes_nome == 'Agosto':
    # return '08'
   #if mes_nome == 'Setembro':
    # return '09'
   #if mes_nome == 'Outubro':
    # return '10'
   #if mes_nome == 'Novembro':
    # return '11'
   #if mes_nome == 'Dezembro':
     #return '12'

# url = FONTE_IGPM
# data = requests.get(url)
# soup = bs(data.content, "html.parser")

# qtd_tables = 2
# json_igpm = []
# referencia = [None] * qtd_tables
# ano = [None] * qtd_tables

# print('- Dados extraídos')
# for table_num in range(qtd_tables):
#   table = soup.find_all('table')
#   df = pd.read_html(str(table), decimal=',', thousands='.')[table_num]
#   ano[table_num] = df.columns[0][0]
#   print(ano[table_num])
#   df.columns = df.columns.droplevel(0)
#   # df1['ano']= ano
#   df.drop(["Acumulado nos últimos 12 meses %"], axis=1, inplace=True)
#   df.dropna(inplace=True)
#   df.rename(columns={'MÊS': 'mes', 'Mensal %': 'mensal'}, inplace=True)
#   # print(df)
#   data = []

  
#   for index, row in df.T.iteritems():
#     mes = (ano[table_num] + retorn_num_mes(row['mes']))
#     mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
#     mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")
#     mensal = str(row['mensal']).replace(".", ",")
#     valor = float(mensal.replace(",","."))
      
#     json_igpm.append({'x': mes, 'y': valor})

# print('- Série criada')
# import time 
# print(json_igpm)
# time.sleep(20)


# ##################referencia
# newlist = sorted(json_igpm, key=lambda k: k['x']) 
# meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# referencia = newlist[-1:][0]['x']
# ano = referencia[:4]
# mes = int(referencia[5:7])
# referencia = meses_ano[mes - 1] + '/' + ano



# # valor_periodo_anterior = float(newlist[-2:][0]['y'])
# #>>>>> VERIFICAR valor_periodo_atual = float(newlist[-2:][1]['y'])

# ######valor cartao 
# valor_cartao =newlist[-1:][0]['y']
# print('- Valor do cartão armazenado')
# valor_periodo_atual = float(newlist[-2:][1]['y'])

# if valor_periodo_atual > 0:
#   direcao = 'up'
#   cor_valor = 'green'
# elif valor_periodo_atual < 0:
#   direcao = 'down'
#   cor_valor = 'red'
#   valor_cartao = str(valor_cartao)[1:]
# else:
#   direcao = 'right'
#   cor_valor = 'gray'
  
# json_igpm = {
#     'nome': 'Índice Geral de Preços Mercado (IGP-M)',
#     'descricao': 'Variação mensal',
#     'fonte': 'FGV',
#     'stats': [
#         {
#             'titulo': 'Brasil',
#             'valor': str(valor_cartao)+'%',
#             'direcao': direcao,
#             'cor_valor': cor_valor,
#             'desc_serie': 'Variação percentual mensal',
#             'serie_tipo': 'data',
#             'referencia': referencia,
#             'y_label': {
#                 'prefixo_sufixo': 'sufixo',
#                 'label': '%'
#             },
#             'serie_labels': {
#                 'x': 'Data',
#                 'y': 'Variação',
#             },
#             'serie': newlist,
#         },       
#     ]
# }


# path_save_json = util.config['path_save_json']['path']
# name_json = 'igpm'

# with open(path_save_json + name_json +'.json', 'w', encoding='utf-8') as f:
#     json.dump(json_igpm, f, ensure_ascii=False, indent=4)
# print('- JSON armazenado')

# ######################################################
# #Upload
# upload_files_to_github(name_json)
# print('- JSON enviado para o GitHub')
