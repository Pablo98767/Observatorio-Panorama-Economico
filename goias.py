from indicadores_mineracao_extracao import *
from logzero import logger

def main():
                    
    path_destino_dados_goias = 'G:/IEL/OBSERVATORIO/ETL/INDICADORES/MINERACAO/dados extraidos/goias/'
                 
    #Extração individual
    # extracao_mineracao('2021', 'GO', 'CO', path_destino_dados_goias)

    #Extração apenas dos dados de Goiás
    path_destino_dados_brasil = 'G:/IEL/OBSERVATORIO/ETL\/NDICADORES/MINERACAO/dados extraidos/brasil/'
    niveis_territoriais = {'CO':['GO']}
    anos = ['2021', '2020','2019','2018','2017','2016']

    for ano in anos:
        for regiao, estados in niveis_territoriais.items():
            for estado in estados:
                extracao_mineracao(ano, estado, regiao, path_destino_dados_goias)


    # #Extração de todos os dados do Brasil ou por região
    # niveis_territoriais = {'SE':['MG', 'SP', 'ES', 'RJ'], 'CO':['GO', 'MT', 'DF']}
    # anos = ['2021', '2020','2019','2018','2017','2016]
    # for ano in anos:
    #     for regiao, estados in niveis_territoriais.items():
    #         for estado in estados:
    #             extracao_mineracao(ano, estado, regiao, path_destino_dados_brasil)



if __name__ == "__main__":
    
    logger.error('*' * 80)
    logger.error('Inicialização do aplicativo')
    logger.error('*' * 80)

    main()

    logger.error('*' * 80)
    logger.error('Finalização do aplicativo')
    logger.error('*' * 80)
