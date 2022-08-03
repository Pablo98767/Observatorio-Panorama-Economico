

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

# ACESSA A PLANILHA
table_cub= pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/CUB - dados mensais - iel -diego.xlsx")# Defina o caminho da planilha onde será extraído os dados.
df = pd.DataFrame(table_cub.values)
df.columns = df.iloc[0]
df = df.iloc[1:]
df.columns = ['referencia', 'indice']
df['referencia'] =  pd.to_datetime(df['referencia'],  format='%d%b%Y:%H:%M:%S.%f')
df.sort_values('referencia', inplace =True) 
df = df.reset_index(drop=True)
df.dropna(inplace =True)
df['referencia'] = df['referencia'].astype(str)
df['referencia'] = df['referencia'].str[:7]
get_colums = table_cub[['Período', 'Valor em R$']]
print(get_colums)


#Puxar dados de referência, parte responsável por captar o mês e o ano.
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
ano_referencia = df['referencia'][-1:].iloc[0][:4]
mes_referencia = int(df['referencia'][5:].iloc[0][-2:])
referencia = meses_ano[mes_referencia-1] + '/' + ano_referencia
print(referencia)


#Extrai um dado especíco da  coluna Valor em R$ da planilha...
print("agora...fazendo a extração ultimo dado ...")
ultimos_dado_go = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/CUB - dados mensais - iel -diego.xlsx") #definir aqui o diretório da planilha
ultimo_dado_go = ultimos_dado_go.loc[0,'Valor em R$']
print(ultimo_dado_go)
print("Ultimo dado extraido com sucesso!")
print("Criando série histórica...")

serie_go= []
now = datetime.now()
ano_atual = now.year
ano_anterior = ano_atual - 1


for i, row in df.iterrows():
  mes = row[0][:7].replace('-', '')
  mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
  mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")
  serie_go.append({'x': mes, 'y': row[1]})
 
print('- Série criada')


# EXEMPLO DE CONDICIONAMENTO PARA ARMAZENAR DEFINIR A SETA DO CARTÃO

print(" - Iniciando o condicionamento!")

if str(ultimos_dado_go) > '0' :
    direcao_go = 'down'
    cor_go = 'red'

else:
    direcao_go = 'up'
    cor_go = 'green'

print('- Valores do cartão foram armazenados')

# Json  template

cub_json = {

    'nome': 'Custo Unitário Básico de Construção - CUB',
    'descricao': 'Variação mensal em reais por m²', 
    'fonte': 'Sinduscon - GO',
    'stats': [      
        {
            'titulo': 'Goiás',
            'valor': str(ultimo_dado_go),
            'direcao': direcao_go,
            'cor_valor': cor_go,
            'referencia': referencia,
            'desc_serie': 'Custo Médio por m² (R$)',
            'serie_tipo': 'data',
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '',
            },

            'serie_labels': {
                'x': 'Data',
                'y': 'Valor'
            },

            'serie': serie_go, # aqui está goiás , porque valor de goiás é a de brasil, sim...saiu ao contrário.
        },
    ]
  }

print(cub_json)

#SALVAR JSON E FAZER UPLOAD PARA O GITHUB.
path_save_json = util.config['path_save_json']['path']
name_json = 'custo_unitario_basico_construcao'

with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
 json.dump(cub_json, f, indent=4, sort_keys=True, default=str)
print('- JSON armazenado')
upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')
print('- Custo Unitário Básico de Construção - CUB atualizado com sucesso!')
