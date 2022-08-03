import time
import urllib
import urllib.parse
from http.client import RemoteDisconnected
from socket import gaierror, gethostbyname
from urllib.request import urlopen

import pandas as pd
import requests
import urllib3
from bs4 import BeautifulSoup

from functions import *


def extracao_mineracao(ano, sigla_estado, regiao, path_destino_extracao):
   
    print("################################")
    print('Buscando substâncias...')
    lista_substancias = cath_substancias(regiao, sigla_estado, ano).values
    print('Ok!')
    print('Buscando lista de municipios...')
    lista_municipios = cath_municipios(regiao, sigla_estado, ano).values
    print('Ok!')
    print('\n')
    print('Iniciando extração...')

    url = 'https://sistemas.anm.gov.br/arrecadacao/extra/Relatorios/cfem/maiores_arrecadadores.aspx'
    
    df_final = pd.DataFrame()
    response = cath_requests()

    soup = BeautifulSoup(response.content, 'html5lib')

    data = { 
        tag['name']: tag['value'] 
        for tag in soup.select('input[name^=ctl00]') if tag.get('value')
    }

    state = { 
        tag['name']: tag['value'] 
        for tag in soup.select('input[name^=__]')   
    }

    payload = data.copy()
    payload.update(state)

    payload.update({
        "ctl00$ContentPlaceHolder1$nu_Ano": ano,
        "ctl00$ContentPlaceHolder1$regiao": regiao,
        "__EVENTTARGET": "ctl00$ContentPlaceHolder1$regiao",
    })

    response = cath_response(payload)
    soup = BeautifulSoup(response.content, 'html5lib')

    state = { 
        tag['name']: tag['value'] 
        for tag in soup.select('input[name^=__]')
    }

    payload.update(state)
    payload.update({
        "ctl00$ContentPlaceHolder1$Estado": sigla_estado,
        "__EVENTTARGET": "ctl00$ContentPlaceHolder1$Estado",
    })

    response = cath_response(payload)
    soup = BeautifulSoup(response.content, 'html5lib')

    quantidade_coletas = len(lista_municipios) * len(lista_substancias)

    for cidade in lista_municipios:
        
        for substancia in lista_substancias:

            substancia_agrupadora = substancia[0]
            codigo_municipio = cidade[0] 

            print('\n')
            print("### Restam: " + str(quantidade_coletas) + " coletas")
            quantidade_coletas = quantidade_coletas - 1 
            print('Estado:' + sigla_estado)
            print("Cidade:" + cidade[1])
            print("Substancia:" + substancia[1])

            state = { tag['name']: tag['value']
                    for tag in soup.select('input[name^=__]')
            }

            payload.update(state)
            payload.update({
                "ctl00$ContentPlaceHolder1$subs_agrupadora": substancia_agrupadora,
                "__EVENTTARGET": "ctl00$ContentPlaceHolder1$subs_agrupadora"
                
            })

            response = cath_response(payload)
            soup = BeautifulSoup(response.content, 'html5lib')
            
            
            state = { tag['name']: tag['value']
                    for tag in soup.select('input[name^=__]')
                    }
                    

            payload.update(state)
            payload.update({
                "ctl00$ContentPlaceHolder1$Municipio": codigo_municipio,
                "ctl00$ContentPlaceHolder1$rdComparacao": 'dsc_nome_razao',
                "ctl00$ContentPlaceHolder1$btnGera": "Gera"
            })

            response = cath_response(payload)

            df_list = pd.read_html(response.text)
            df_list = pd.read_html(str(response.text),encoding = 'utf-8', decimal=',', thousands='.')
            df_atual = pd.DataFrame()

            for i, df_atual in enumerate(df_list):
                df_atual

            if(len(df_atual) > 1):
                df_atual.drop(["Arrecadador (Empresa)"][0], axis=1)
                df_atual.columns = df_atual.columns.droplevel()
                df_atual = df_atual.drop(["Arrecadador (Empresa)"], axis=1)
                df_atual = df_atual.drop(["Arrecadador (Empresa).1"], axis=1)
                df_atual.drop(df_atual.tail(1).index,inplace=True) 
                df_atual.rename(columns={'Arrecadador (Empresa).2': 'Arrecadador (Empresa)'}, inplace = True)
                df_atual.rename(columns={'% RecolhimentoCFEM': '%RecolhimentoCFEM'}, inplace = True)
                df_atual = pd.DataFrame(df_atual, columns = ['Arrecadador (Empresa)', 'Qtde Títulos', 'Operação', 'RecolhimentoCFEM', '%RecolhimentoCFEM', 'municipio', 'Sub_Agrupadoras'])
                df_atual = df_atual.astype({"Operação": str, "RecolhimentoCFEM": str})
                df_atual["Operação"] = df_atual["Operação"].apply(lambda x: x.replace(".",","))
                df_atual["RecolhimentoCFEM"] = df_atual["RecolhimentoCFEM"].apply(lambda x: x.replace(".",","))
                df_atual['municipio'] = cidade[1]
                df_atual['Estado'] = sigla_estado
                df_atual['Sub_Agrupadoras'] = substancia[1]
                df_atual['ano'] = ano
                df_final = pd.concat([df_final, df_atual])
                df_final = df_final.reset_index(drop=True)
                print('#############################')
                df_final.to_csv(path_destino_extracao + sigla_estado + ano +'.csv', encoding ='latin', sep=';')
 
