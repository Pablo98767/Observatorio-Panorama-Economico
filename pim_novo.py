
from gettext import install
from mailbox import NotEmptyError
from msilib.schema import tables
from venv import create
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json 
from datetime import date
import util as util
from util import *
from upload import *
from github import Github


start = date(2019, 12, 1)
end = date(2022, 5, 1)
#end = date.today()
dates = pd.date_range(start, end, freq='M') + pd.offsets.MonthBegin(n=1)

lista_periodos = []
for i in range(len(dates)):
  year = str(dates[i].year)

  if dates[i].month < 10:
    month = '0' + str(dates[i].month)
    lista_periodos.append(int(year+month))
  else:
    month = str(dates[i].month)
    lista_periodos.append(int(year+month))

def cath_referencia(mes):
    # if mes[:3] == 'jan':
    #   mes = 'Jan/'+(str(mes[-4:])).capitalize()
    # else:
    #   mes = 'Jan-'+(mes[:3]+ '/' +mes[-4:]).capitalize()
    mes = (mes[:3]+ '/' +mes[-4:]).capitalize()
    return mes

def cath_serie():
  serie_go = []
  serie_br = []
  for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/8159/n1/1/p/{0}/v/11601/N3/52/f/u'
    url = url.format(mes)
    dados = requests.get(url)
    soup = bs(dados.content, "html5lib")
    dados = json.loads(soup.text)

    try:
      mes = pd.to_datetime(mes, format='%Y%m', errors='coerce')
      mes = mes.strftime("%Y-%m-%dT%H:%M:%SZ")
      valor_br = dados[-2]['V']
      mes_referencia = dados[2]['D2N']
      if str(valor_br) != '...':
        referencia_br = mes
        serie_br.append({'x': mes, 'y': float(valor_br)})

      valor_go = dados[2]['V']
      mes_referencia = dados[1]['D2N']
      if str(valor_go) != '...':
        serie_go.append({'x': mes, 'y': float(valor_go)})
        
    except IndexError:
      break

  return {'serie_go': serie_go, 'serie_br': serie_br}      
 
# def direcao_seta(series, serie_escolhida):
#   valor_periodo_anterior = series[serie_escolhida][-2:][0]['y']
#   valor_periodo_atual = series[serie_escolhida][-2:][1]['y']

#   if valor_periodo_atual > valor_periodo_anterior:
#     direcao_seta = 'up'
#   elif valor_periodo_atual < valor_periodo_anterior:
#     direcao_seta = 'down'
#   else:
#     direcao_seta = 'right'

#   return direcao_seta

def cath_cartao(federacao):
  
  for mes in lista_periodos:
    url = 'http://api.sidra.ibge.gov.br/values/t/8159/n1/1/p/{0}/v/11601/N3/52/f/u'
    url = url.format(mes)
    dados = requests.get(url)
    soup = bs(dados.content, "html5lib")
    dados = json.loads(soup.text)

    try:
      valor = dados[federacao]['']
      print(valor)
     
      if str(valor) != '...':
        mes_referencia = dados[1]['D2N']
        ultimo_dado = {'mes': mes_referencia, 'valor': valor}
      
    except IndexError:
      break

  valor_periodo_atual = float(ultimo_dado['valor'])  
  if valor_periodo_atual >= 0:
    cor_valor = 'green'
    valor_periodo_atual = str(valor_periodo_atual)

  else:
    cor_valor = 'red'
    valor_periodo_atual = str(valor_periodo_atual)[1:]  

  ultimo_dado.update({
      'referencia': cath_referencia(ultimo_dado['mes']), 
      'valor': valor_periodo_atual,
      'cor_valor': cor_valor,
  })

  return ultimo_dado  

# def direcao_seta(federacao):
  
#   meses_ano = {'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04', 'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08', 'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'}

#   for mes in lista_periodos:
#     url = 'http://api.sidra.ibge.gov.br/values/t/3653/n1/1/p/{0}/v/3140/N3/52/f/u'
#     url = url.format(mes)
#     dados = requests.get(url)
#     soup = bs(dados.content, "html5lib")
#     dados = json.loads(soup.text)

#     try:
#       valor = dados[federacao]['V']
#       if str(valor) != '...':
#         mes_referencia = dados[1]['D2N']
#         valor_periodo_atual = float(valor)
#         ultimo_mes = str(mes)
      
#     except IndexError:
#       break

#   ano_periodo_atual = ultimo_mes[:4]
#   mes_periodo_atual = ultimo_mes[4:]
#   ano_periodo_anterior = str(int(ano_periodo_atual) - 1)
#   mes_periodo_anterior = mes_periodo_atual
#   periodo_anterior = ano_periodo_anterior + mes_periodo_anterior

#   url = 'http://api.sidra.ibge.gov.br/values/t/3653/n1/1/p/{0}/v/3140/N3/52/f/u'
#   url = url.format(periodo_anterior)
#   dados = requests.get(url)
#   soup = bs(dados.content, "html5lib")
#   dados = json.loads(soup.text)
#   if str(valor) != '...':
#     valor_periodo_anterior = float(dados[federacao]['V'])


#   if valor_periodo_atual < 0:
#     direcao = 'down'
#   elif valor_periodo_atual > 0:
#     direcao = 'up'
#   else:
#     direcao = 'right'
#   print(valor_periodo_atual)
#   print(type(valor_periodo_anterior))
#   print(valor_periodo_atual)
#   print(direcao)
#   return direcao



series = cath_serie()

def cartao_valor(valor):

  if valor >= 0:
    cor_valor = 'green'
    direcao = 'up'
    valor = str(valor)

  else:
    cor_valor = 'red'
    direcao = 'down'
    valor = str(valor)[1:] 

  return [cor_valor, direcao, valor]

 
cartao_br = cath_cartao(1)
cartao_go = cath_cartao(2)

cartao_br_outras_info = cartao_valor(series['serie_br'][-1:][0]['y'])
cartao_go_outras_info = cartao_valor(series['serie_go'][-1:][0]['y'])

print(cartao_br_outras_info)
print(cartao_go_outras_info)

pim = {
    'nome': 'Produção Física Industrial',
    'descricao': 'Variação percentual em relação ao mesmo período do ano anterior',
    'fonte': 'IBGE - PIM-PF',
    'stats': [
        {
            'titulo': 'Brasil',
            'valor': str(cartao_br_outras_info[2]) +'%',
            'direcao': cartao_br_outras_info[1],
            'cor_seta': 'orange',
            'cor_valor':cartao_br_outras_info[0],
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': cartao_br['referencia'],
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%',
            },

            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': series['serie_br'],

        },

        {
            'titulo': 'Goiás',
            'valor': str(cartao_go_outras_info[2])+'%',
            'direcao': cartao_go_outras_info[1],
            'cor_valor': cartao_go_outras_info[0],
            'desc_serie': 'Variação percentual mensal',
            'serie_tipo': 'data',
            'referencia': cartao_go['referencia'],
            'y_label': {
                'prefixo_sufixo': 'sufixo',
                'label': '%',
            },
            

            'serie_labels': {
                'x': 'Data',
                'y': 'Variação'
            },
            'serie': series['serie_go'],
        }
    ]
}

print(pim)
 
path_save_json = util.config['path_save_json']['path']
name_json = 'pim'


################### Salva o pim_mesclagem.JSON 
with open(path_save_json + name_json + '.json', 'w', encoding='utf-8') as f:
    json.dump(pim, f, ensure_ascii=False, indent=4)
print('- JSON armazenado')

upload_files_to_github(name_json)
print('- JSON enviado para o GitHub')