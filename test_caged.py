from cgi import print_arguments
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


#Acessando planilha
table_caged = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/saldo-caged-industria-da-transformacao-diego.xlsx")
df = pd.DataFrame(table_caged.values)
df.columns = df.iloc[0]
df = df.iloc[1:]
df.columns = ['referencia', 'indice_br','indice_go']
df['referencia'] =  pd.to_datetime(df['referencia'],  format='%d%b%Y:%H:%M:%S.%f')
df.sort_values('referencia', inplace =True) 
df = df.reset_index(drop=True)
df.dropna(inplace =True)

df['referencia'] = df['referencia'].astype(str)
df['referencia'] = df['referencia'].str[:7]
get_colums = table_caged[['referencia', 'Brasil']]
print(get_colums)

#Automatizar a referência, parte responsável pelo mês.
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
ano_referencia = df['referencia'][-1:].iloc[0][:4]
mes_referencia = int(df['referencia'][4:].iloc[0][-2:])
referencia = meses_ano[mes_referencia-1] + '/' + ano_referencia

#extraindo o ultimo dado de brasil
print("agora...fazendo a extração ultimo dado de brasil...")
ultimos_dado_br = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/saldo-caged-industria-da-transformacao-diego.xlsx")
ultimo_dado_br = ultimos_dado_br.loc[0,'Brasil']
print(ultimo_dado_br)
print("Ultimo dado de brasil extraido com sucesso!")


#extraindo o dado de goiás 
ultimos_dado_go = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/saldo-caged-industria-da-transformacao-diego.xlsx")
ultimo_dado_go = ultimos_dado_go.loc[0,'Goiás']
print(ultimo_dado_go)
print("Ultimo dado de Goiás extraído com sucesso!")

#Criando série histórica
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
print("Iniciando o condicionamento!")

if str(ultimos_dado_br) < '0':
    direcao_br = 'down'
    cor_br = 'red'       
    
else:
    direcao_br = 'up'
    cor_br = 'green'


if str(ultimos_dado_go) < '0' :
    direcao_go = 'down'
    cor_go = 'red'

else:
    direcao_go = 'up'
    cor_go = 'green'

print('- Valores do cartão foram armazenados')

# Json caged template

caged_json = {

    'nome': 'Saldo de Empregados da Ind. de Transformação',
    'descricao': 'Saldo de empregados = Admitidos - Desligados',
    'fonte': 'MTE',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(ultimo_dado_br), 
            'direcao': direcao_br,
            'cor_valor': cor_br,
            'referencia': referencia,
            'desc_serie': 'Saldo de empregados por mês',
            'serie_tipo': 'data',
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '',
            },


            'serie_labels': {
                'x': 'Data',
                'y': 'Valor'
            },

            'serie': serie_go, # aqui está goiás , porque valor de goiás e a de brasil, sim...saiu errado.
        },

        {
            'titulo': 'Goiás',
            'valor': str(ultimo_dado_go),
            'direcao': direcao_go,
            'cor_valor': cor_go,
            'referencia': referencia,
            'desc_serie': 'Saldo de empregados por mês',
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

print(caged_json)

path_save_json = util.config['path_save_json']['path']
name_json = 'saldo_desemprego_caged'
with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
 json.dump(caged_json, f, indent=4, sort_keys=True, default=str)
print('- JSON armazenado')
upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')
print('- Saldo de Empregados da Ind. de Transformação atualizado com sucesso!')