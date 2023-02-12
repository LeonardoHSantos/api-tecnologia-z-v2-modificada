import logging
from time import sleep

logging.basicConfig(
    level=logging.INFO,
    filename="logs_api/logs_api.log",
    encoding="utf-8",
    format="""----------------------------------------------\nLogRecord: %(asctime)s | Level: %(levelname)s | Message: %(message)s | Module: %(module)s | Pathname: %(pathname)s | Line: %(lineno)d | ProcessName: %(processName)s""")


import threading
from plataform.controllers.http_controller.auth import auth_broker

from plataform.controllers.services_aux import status_services
from plataform.controllers.wss_controller.client.client import Websocket_client
from plataform.controllers.wss_controller.channels_wss.channels import ChannelsWSS
from plataform.controllers.wss_controller.send_message_wss import send_message_wss

from plataform.controllers.base_strategy.base import BaseStrategy



class StartAPI:
    def __init__(self, identifier, password):
        self.identifier = identifier
        self.password = password
        
    def auth_user_broker(self):
        return auth_broker(url=status_services.URL_HTTP, identifier=self.identifier, password=self.password)

    def active_strategy(self):
        status_services.THREDING_STRATEGY = threading.Thread(target=BaseStrategy.strategy_M5).start()


    def connect_plataform_wss(self):
        try:
            auth = self.auth_user_broker()
            if auth["code"] == "success":
                print(auth)
                logging.info(f'Usuário e Senhas validos. Status auth: {auth["code"]}')
                msg_ssid = ChannelsWSS.send_ssid(auth["ssid"])
                print("MSG SSID: ", msg_ssid)
                logging.debug("***********testando debug***********")
                status_services.WSS_OBJ = Websocket_client()
                status_services.THREDING_WSS = threading.Thread(target=status_services.WSS_OBJ.wss.run_forever).start()
                try:
                    while True:
                        if status_services.STATUS_CONNECT_WSS == True:
                            logging.info(f'STATUS_CONNECT_WSS: {status_services.STATUS_CONNECT_WSS}')
                            send_message_wss(msg_ssid)
                            print(" ************ Mensagem enviada | SSID ************ ")
                            break
                    while True:
                        if status_services.STATUS_MESSAGES_WSS == True:
                            msg_check_services = f"Check status services | STATUS_CONNECT_WSS: {status_services.STATUS_CONNECT_WSS} | STATUS_MESSAGES_WSS: {status_services.STATUS_MESSAGES_WSS}"
                            msg_ids_accounts = f"ID Accounts | REAL: {status_services.ID_USER_ACCOUNT_PRACTICE} | PRACTICE: {status_services.ID_USER_ACCOUNT_PRACTICE}"
                            logging.info(msg_check_services)
                            print(msg_check_services)
                            print(msg_ids_accounts)
                            print(" ----------- get candles activated first time ----------- ")
                            msg_get_candles_open = ChannelsWSS.get_actives_open()
                            print(msg_get_candles_open)
                            send_message_wss(message=msg_get_candles_open)
                            print("----------------- end first -----------")

                            self.active_strategy()
                            break

                except Exception as e:
                    logging.error(f" *** Error/Module: Loop While StartAPI.connect_plataform_wss: {e} *** ")
            else:
                logging.error(f"ERROR AUTHENTICATION. USERNAME OR PASSWORD IS INVALID: {auth}") 
        except Exception as e:
            logging.error(f" *** ERROT/MODULE: StartAPI.connect_plataform_wss: {e} *** ")
    
    
            

    


        
    