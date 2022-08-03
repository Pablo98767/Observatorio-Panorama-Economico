

#BIBLIOTECAS NECESSÁRIAS!


from sys import displayhook
import pandas as pd
import json
from upload import *
import util as utils
from util import *
from github import Github
from datetime import datetime
from openpyxl import load_workbook
import locale


# ACESSA A PLANILHA
table_cub = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/CUB - dados mensais - iel -diego.xlsx", sheet_name="Variação 12 meses e anual")# Defina o caminho da planilha onde será extraído os dados.
df = pd.DataFrame(table_cub.values)
df.columns = df.iloc[0]
df = df.iloc[1:]
df.columns = ['referencia', 'indice_br','indice_go','variacao_panorama_12_Meses','variacao_anual_panorama']
df['referencia'] =  pd.to_datetime(df['referencia'],  format='%d%b%Y:%H:%M:%S.%f')
df.sort_values('referencia', inplace =True) 
df = df.reset_index(drop=True)
df.dropna(inplace =True)

df['referencia'] = df['referencia'].astype(str)
df['referencia'] = df['referencia'].str[:7]
get_colums = table_cub[['Período','Variação 12 Meses','Variação Anual']]
print(get_colums)

#Automatizar a referência, parte responsável pelo mês.
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
ano_referencia = df['referencia'][-1:].iloc[0][:4]
mes_referencia = int(df['referencia'][5:].iloc[0][-2:])
referencia = meses_ano[mes_referencia-1] + '/' + ano_referencia


# EXEMPLO PARA EXTRAIR DADOS ESPECÍFICOS.


 #Extrai um dado especíco de uma coluna...
print("agora...fazendo a extração ultimo dado de brasil...")
ultimos_dado_br = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/CUB - dados mensais - iel -diego.xlsx", sheet_name="Variação 12 meses e anual") #definir aqui o diretório da planilha#
#print(ultimos_dado_br.loc[0, 'Variação - Panorama 12 Meses'])
ultimo_dado_br = ultimos_dado_br.loc[0, 'Variação - Panorama 12 Meses']
print(ultimo_dado_br)
print("Ultimo dado de brasil extraido com sucesso!")

#OBS : este código está errado, pois retorna um lista gigante quando armazenada no json!


# EXEMPLO PARA EXTRAIR DADOS ESPECÍFICOS.

 #Extrai um dado específico de outra coluna!
ultimos_dado_go = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/CUB - dados mensais - iel -diego.xlsx", sheet_name="Variação 12 meses e anual")
#print(ultimos_dado_go.loc[1, 'Variação Anual Panorama'])
ultimo_dado_go = ultimos_dado_go.loc[0,'Variação Anual Panorama']
print(ultimo_dado_go)
print("Ultimo dado de Goiás extraído com sucesso!")

#OBS : este código está errado, pois retorna um lista gigante quando armazenada no json! 



#EXEMPLO DE SÉRIE HISTÓRICA

print("Criando série histórica...")


serie_br = []
serie_go= []
now = datetime.now()
ano_atual = now.year
ano_anterior = ano_atual - 1



for i, row in df.iterrows():
  mes = row[0][:7].replace('-', '')
  mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
  mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")
  serie_go.append({'x': mes, 'y': row[1]})
  serie_br.append({'x': mes, 'y': row[2]})
 
print('- Série criada')


# EXEMPLO DE CONDICIONAMENTO PARA CRIAR DEFINIR A SETA DO CARTÃO

print("Iniciando o condicionamento!")

if str(ultimos_dado_br) > '0':
    direcao_br = 'down'
    cor_br = 'red'
   
else:
    direcao_br = 'up'
    cor_br = 'green'

if str(ultimos_dado_go) > '0' :
    direcao_go = 'down'
    cor_go = 'red'

else:
    direcao_go = 'up'
    cor_go = 'green'

print('- Valores do cartão foram armazenados')

# Json  template

cub_variacao_anual_json = {

    'nome': 'Custo Unitário Básico de Construção - Variação Anual',
    'descricao': 'Variação 12 Meses - Anual',
    'fonte': ' Sinduscon - GO',
    'stats': [
        {  
            'titulo': 'Variação 12 Meses',
            'valor': str(ultimo_dado_br) + '%',
            'direcao': direcao_br,
            'cor_valor': cor_br,
            'referencia': referencia,
            'desc_serie': 'Variação nos últimos 12 meses',
            'serie_tipo': 'data',
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '',
            },

            'serie_labels': {
                'x': 'Data',
                'y': 'Valor'
            },

            'serie': serie_go, 
        },


        {
            'titulo': 'Variação Anual',
            'valor':  str(ultimo_dado_go) + '%' , # CORRIGIR A VARIÁVEL, subtituir este núemero pela variável! conversar com Samuel para suporte!
            'direcao': direcao_go,
            'cor_valor': cor_go,
            'referencia': referencia,
            'desc_serie': 'Variação Anual',
            'serie_tipo': 'data',
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '',
            },

            'serie_labels': {
                'x': 'Data',
                'y': 'Valor'
            },
            'serie': serie_br, # aqui está o valor de brasil, porque o valor de brasil é o de goiás, sim... está errado.
        },
    ]
  }

print(cub_variacao_anual_json)
 


# SALVAR JSON E FAZER UPLOAD PARA O GITHUB.

path_save_json = util.config['path_save_json']['path']
name_json = 'cub_variacao_anual'
with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
 json.dump(cub_variacao_anual_json, f, indent=4, sort_keys=True, default=str)
print('- JSON armazenado')
upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')
print('- Cube Variação Anual atualizado com sucesso!')
