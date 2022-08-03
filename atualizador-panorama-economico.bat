set /A COUNTER=1
chcp 65001
@ECHO OFF
:loop



echo %Counter%
cls
echo ATUALIZANDO 'Utilização da Capacidade Instalada da Indústria' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\capacidade_industria_transf.py"
echo 'Utilização da Capacidade Instalada da Indústria' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Índice de Confiança Industrial' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\confianca_industrial.py"
echo 'Índice de Confiança Industrial' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Exportações e importações' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\comex_modificado.py"
echo 'Exportações e importações' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls


echo %Counter%
cls
echo ATUALIZANDO 'Estoque efetivo em relação ao planejado da Indústria' [%Counter%/15]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\estoque_efetivo.py"
echo 'Estoque efetivo em relação ao planejado da Indústria' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls


echo %Counter%
cls
echo ATUALIZANDO 'Perspectiva do Emprego da Indústria' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\expectativa_emprego.py"
echo 'Perspectiva do Emprego da Indústria' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Índice de Atividade Econômica' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\ibc.py"
echo 'Índice de Atividade Econômica' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls




echo %Counter%
cls
echo ATUALIZANDO 'Índice de Confiança do Consumidor' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\icc_novo.py"
echo 'Índice de Confiança do Consumidor' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls




echo %Counter%
cls
echo ATUALIZANDO 'Taxa de Desocupação' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\desocupacao_novo.py"
echo 'Taxa de Desocupação' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls




echo %Counter%
cls
echo ATUALIZANDO 'Índice Geral de Preços – Mercado (IGP-M)' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\igpm.py"
echo 'Índice Geral de Preços – Mercado (IGP-M)' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls



echo %Counter%
cls
echo ATUALIZANDO 'Índice Nacional de Preços ao Consumidor - INPC' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\inpc_novo.py"
echo 'Índice Nacional de Preços ao Consumidor - INPC' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls



echo %Counter%
cls
echo ATUALIZANDO 'Intenção de Investir na Indústria' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\intencao_invest.py"
echo 'Intenção de Investir na Indústria' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

 
ech
cls
echo ATUALIZADO 'Ìndice Nacional de Preços ao Consumidor Amplo - IPCA' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe"G:\IEL\OBSERVATORIO\ETL\panorama economico\ipca_nova_versao.py"
echeços ao Consumidor Amplo - IPCA' ATUALIZADO!
set
tim
cls


ech
cls
echo ATUALIZANDO 'Produção Física Industrial' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\pim_novo.py"
echo 'Produção Física Industrial' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul 
cls

echo %Counter%
cls
echo ATUALIZANDO 'Saldo de Empregados da Ind. de Transformação' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\test_caged.py"
echo 'Saldo de Empregados da Ind. de Transformação' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls



echo %Counter%
cls
echo ATUALIZANDO 'Custo Unitário Básico de Construção - CUB' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\Cub_m².py"
echo 'Custo Unitário Básico de Construção - CUB' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls


echo %Counter%
cls
echo ATUALIZANDO 'Custo Unitário Básico de Construção - Variação Mensal' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\cub_var_mensal.py"
echo 'Custo Unitário Básico de Construção - Variação Mensal' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls

echo %Counter%
cls
echo ATUALIZANDO 'Cube Variação Anual' [%Counter%/14]
C:/Users/pablofelix.iel/AppData/Local/Microsoft/WindowsApps/python3.9.exe "G:\IEL\OBSERVATORIO\ETL\panorama economico\Cub_variacao_anual.py"
echo 'Cube Variação Anual' ATUALIZADO!
set /A COUNTER=%COUNTER%+1
timeout /t 3 /nobreak > nul
cls




cls
echo A execução será retomada em alguns minutos...
timeout /t 1800 /nobreak > nul
 

set /A COUNTER=1

goto loop