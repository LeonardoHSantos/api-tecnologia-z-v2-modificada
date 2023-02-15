import threading
from plataform.startAPI import StartAPI
from config_db import USER_IQ, PASSWORD_IQ

from plataform.controllers.services_aux import status_services

import logging
from time import sleep

logging.basicConfig(
    level=logging.INFO,
    filename="logs_api/logs_api.log",
    encoding="utf-8",
    format="""----------------------------------------------\nLogRecord: %(asctime)s | Level: %(levelname)s | Message: %(message)s | Module: %(module)s | Pathname: %(pathname)s | Line: %(lineno)d | ProcessName: %(processName)s""")

def monitoring_status():
    while True:
        try:
            if status_services.STATUS_MESSAGES_WSS == False and status_services.STATUS_TEMP_CONN == True:
                if status_services.TT_RECONNECT < status_services.MAX_RECONNECT:
                    msg_warning = f"WARNING | TENTANDO SE RECONECTAR COM WEBSOCKET: {e} | TENTATIVA: {status_services.TT_RECONNECT} de {status_services.MAX_RECONNECT}"
                    logging.error(msg_warning)
                    run = StartAPI(identifier=USER_IQ, password=PASSWORD_IQ)
                    run.connect_plataform_wss()
                    status_services.TT_RECONNECT += 1
                    sleep(3)
                else:
                    msg_warning = f"WARNING | O SISTEMA ATINGIU O LIMITO MÁXIMO DE TENTATIVAS PARA RECONNEXÃO | TENTATIVAS: {status_services.TT_RECONNECT} de {status_services.MAX_RECONNECT}"
                    logging.warning(msg_warning)
                    msg_warning = f"CRITICAL | SISTEMA ENCERRADO DEVIDO A QUANTIDADE MAX DE RECONEXÃO| TENTATIVAS: {status_services.TT_RECONNECT} de {status_services.MAX_RECONNECT}"
                    logging.critical(msg_warning)
                    quit()
        except Exception as e:
            msg_error = f"TENTATIVAS: {status_services.TT_RECONNECT} | ERRO AO TENTAR SE RECONECTAR COM WEBSOCKET: {e}"
            logging.error(msg_error)

def start_microservices_api():
    run = StartAPI(identifier=USER_IQ, password=PASSWORD_IQ)
    threading.Thread(target=monitoring_status).start()
    run.connect_plataform_wss()
    
start_microservices_api()