import logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs_api/logs_api.log",
    encoding="utf-8",
    format="""----------------------------------------------\nLogRecord: %(asctime)s | Level: %(levelname)s | Message: %(message)s | Module: %(module)s | Pathname: %(pathname)s | Line: %(lineno)d | ProcessName: %(processName)s""")

import pandas as pd
from plataform.controllers.services_aux import variables, actives

def process_open_actives(dados):
        try:
            print("processando dados ativos abertos --------------------------------------------------")
            lista_ativos = [
                [], # 0 - id
                [], # 1 - name
                [], # 2 - ticker
                [], # 3 - is_suspended
                [], # 4 - enabled

                [], # 5 - mercado
                [], # 6 - PADRAO-M5-V1
                [], # 7 - PADRAO-M5-V2
            ]
           
            for i in dados["binary"]["actives"]:
                try:
                    id   = dados["binary"]["actives"][i]["id"]
                    name = dados["binary"]["actives"][i]["name"]
                    ticker = dados["binary"]["actives"][i]["ticker"]
                    is_suspended = dados["binary"]["actives"][i]["is_suspended"]
                    enabled = dados["binary"]["actives"][i]["enabled"]
                    # print("******** Data Open Actives: ", id, name, ticker, is_suspended, enabled)
                    
                    if enabled == True and ticker in actives.PARIDADES.keys(): #and is_suspended == False:
                        
                        lista_ativos[0].append(id)
                        lista_ativos[1].append(name)
                        lista_ativos[2].append(ticker)
                        lista_ativos[3].append(is_suspended)
                        lista_ativos[4].append(enabled)

                        if "OTC" in ticker:
                            lista_ativos[5].append("otc")
                        else:
                            lista_ativos[5].append("aberto")

                        lista_ativos[6].append(f"{ticker}-M5-V1-300")
                        lista_ativos[7].append(f"{ticker}-M5-V2-300")
                    
                except Exception as e:
                    print(e)
            if len(lista_ativos[0]) >= 1:
                variables.DATAFRAME_ACTIVES_OPEN = pd.DataFrame(list(zip(
                        lista_ativos[0],
                        lista_ativos[1],
                        lista_ativos[2],
                        lista_ativos[3],
                        lista_ativos[4],
                        lista_ativos[5],
                        lista_ativos[6], lista_ativos[7],
                    )),
                    columns=[
                        "id", "name", "ticker", "is_suspended", "enabled",
                        "mercado",
                        "PADRAO-M5-V1", "PADRAO-M5-V2"
                    ])
            else:
                variables.DATAFRAME_ACTIVES_OPEN = None

            print(variables.DATAFRAME_ACTIVES_OPEN)
        except Exception as e:
            variables.DATAFRAME_ACTIVES_OPEN = None
            msg_error = f"ERROR process_open_actives | Error: {e}"
            print(msg_error)
            logging.error(msg_error)