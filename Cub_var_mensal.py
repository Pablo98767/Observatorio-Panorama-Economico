

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
''

# ACESSA A PLANILHA
table_cub = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/CUB - dados mensais - iel -diego.xlsx", sheet_name="Variação Mensal")# Defina o caminho da planilha onde será extraído os dados.
df = pd.DataFrame(table_cub.values)
df.columns = df.iloc[0]
df = df.iloc[1:]
df.columns = ['referencia', 'indice_go','valor_panorama']
df['referencia'] =  pd.to_datetime(df['referencia'],  format='%d%b%Y:%H:%M:%S.%f')
df.sort_values('referencia', inplace =True) 
df = df.reset_index(drop=True)
df.dropna(inplace =True)
df['referencia'] = df['referencia'].astype(str)
df['referencia'] = df['referencia'].str[:7]
get_colums = table_cub[['Período', 'Valor Panorama(%)']]
print(get_colums)


#Automatizar a referência, parte responsável pelo mês.
meses_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
ano_referencia = df['referencia'][-1:].iloc[0][:4]
mes_referencia = int(df['referencia'][5:].iloc[0][-2:])
referencia = meses_ano[mes_referencia-1] + '/' + ano_referencia

# EXEMPLO PARA EXTRAIR DADOS ESPECÍFICOS.

 #Extrai um dado especíco de uma coluna...
print("agora...fazendo a extração ultimo dado de Goiás...")
ultimos_dado_go = pd.read_excel("G:/IEL/OBSERVATORIO/ETL/planilhas de dados/CUB - dados mensais - iel -diego.xlsx", sheet_name="Variação Mensal") #definir aqui o diretório da planilha
#print(ultimos_dado_go.loc[0, 'Valor Panorama(%)'])
ultimo_dado_go = ultimos_dado_go.loc[0,'Valor Panorama(%)']
print(ultimo_dado_go)
print("Ultimo dado de Goiás extraido com sucesso!")

#OBS : este código está errado, pois retorna um lista gigante quando armazenada no json!


#EXEMPLO DE SÉRIE HISTÓRICA

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


# EXEMPLO DE CONDICIONAMENTO PARA CRIAR DEFINIR A SETA DO CARTÃO


print("Iniciando o condicionamento!")

if str(ultimos_dado_go) > '0' :
    direcao_go = 'down'
    cor_go = 'red' 

else:
    direcao_go = 'up'
    cor_go = 'green'

print('- Valores do cartão foram armazenados')



# Json  template
cub_var_mensal = {

    'nome': 'Custo Unitário Básico de Construção - Variação Mensal ',
    'descricao': 'Variação percentual - Mensal',
    'fonte': 'Sinduscon - GO',
    'stats': [
        {
            'titulo': 'Goiás',
            'valor': str(ultimo_dado_go)+'%', 
            'direcao': direcao_go,
            'cor_valor': cor_go,
            'referencia': referencia,
            'desc_serie': 'Custo Básico de contrução - Variação Anual',
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
      ]
   }

print(cub_var_mensal)

#SALVAR JSON E FAZER UPLOAD PARA O GITHUB.

path_save_json = util.config['path_save_json']['path']
name_json = 'cub_variacao_mensal'

with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
 json.dump(cub_var_mensal, f, indent=4, sort_keys=True, default=str)
print('- JSON armazenado')
upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')
print('- Custo Unitário Básico de Construção - Variação Mensal atualizado com sucesso!')
