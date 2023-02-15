import logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs_api/logs_api.log",
    encoding="utf-8",
    format="""----------------------------------------------\nLogRecord: %(asctime)s | Level: %(levelname)s | Message: %(message)s | Module: %(module)s | Pathname: %(pathname)s | Line: %(lineno)d | ProcessName: %(processName)s""")

import websocket
from datetime import datetime
from plataform.controllers.services_aux import status_services
# from plataform.controllers.wss_controller.channels_wss.channels import ChannelsWSS

from plataform.controllers.prepare_data_controller.prepare_data_analysis import PrepareDataAnalysis
# from plataform.controllers.process_data_controller.process_data_candles import Process_data_candles
from plataform.controllers.prepare_data_controller.prepare_data import convert_to_json
from plataform.controllers.process_data_controller.process_data_active_open import process_open_actives

class Websocket_client:
    def __init__(self):
        self.wss = websocket.WebSocketApp(
            url=status_services.URL_WSS, 
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
    def on_message(self, message):
        message = convert_to_json(message)
        # print(message)

        if message["name"] == "initialization-data":
            process_open_actives(message["msg"])

        elif message["name"] == "candles":
            PrepareDataAnalysis.analysis_data(request_id=message["request_id"], message=message["msg"]["candles"])
            # Process_data_candles(request_id=message["request_id"]).process_data_candles(message=message["msg"]["candles"])


        else:
            print(message)
            if message["name"] == "profile":
                try:
                    status_services.ID_USER_ACCOUNT_REAL = message["msg"]["balances"][0]["id"]
                    status_services.ID_USER_ACCOUNT_PRACTICE = message["msg"]["balances"][1]["id"]
                    status_services.STATUS_TEMP_CONN = True
                    status_services.STATUS_MESSAGES_WSS = True
                    status_services.TT_RECONNECT = 0
                    
                    print(f"IDS | REAL: {status_services.ID_USER_ACCOUNT_REAL} | PRACTICE: {status_services.ID_USER_ACCOUNT_PRACTICE} | STATUS_MESSAGES_WSS: {status_services.STATUS_MESSAGES_WSS}")
                except Exception as e:
                    msg_error_profile = f"Error/Message Profile: {e}"
                    print(msg_error_profile)
                    logging.debug(msg_error_profile)



    def on_open(self):
        status_services.STATUS_CONNECT_WSS = True
        msg_status_conn = f"### Conexão estabelecida com websocket | {datetime.now()} | Status CONN: {status_services.STATUS_CONNECT_WSS} ###"
        print(msg_status_conn)
        logging.info(msg_status_conn)

    def on_error(self, error):
        try:
            logging.error(f"### Erro com a conexão websocket: {error} ###")
        except Exception as e:
            logging.error(f"### Error/Exception websocket {e} ###")
    
    def on_close(self):
        status_services.STATUS_CONNECT_WSS = False
        status_services.STATUS_MESSAGES_WSS = False
        self.wss.close()
        try:
            logging.warning(f"### Conexão encerrada com websocket | {datetime.now()} ###")
        except Exception as e:
            logging.error(f"### on_close/Exception websocket {e} ###")


    

