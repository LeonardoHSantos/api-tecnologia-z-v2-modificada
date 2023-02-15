import logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs_api/logs_api.log",
    encoding="utf-8",
    format="""----------------------------------------------\nLogRecord: %(asctime)s | Level: %(levelname)s | Message: %(message)s | Module: %(module)s | Pathname: %(pathname)s | Line: %(lineno)d | ProcessName: %(processName)s""")


from time import sleep
from plataform.controllers.services_aux import status_services
from plataform.controllers.services_aux import variables, constants

from plataform.controllers.wss_controller.channels_wss.channels import ChannelsWSS
from plataform.controllers.wss_controller.send_message_wss import send_message_wss

from plataform.controllers.datetime_controller.expiration_operations import datetime_now
from plataform.controllers.datetime_controller.expiration_operations import expiration_operation_M5 
from plataform.controllers.datetime_controller.expiration_operations import check_expiration_operation_M5


class BaseStrategy:
    def strategy_M5():
        try:
            while True:
                dt = datetime_now(tzone="America/Sao Paulo")
                second = dt.second
                minute = dt.minute

                ####### CHAMADA PADRÃO 1 ########
                if second == 4 and minute in constants.OBJECT_MINUTES_P1_AND_P2.keys():        # init
                    BaseStrategy.strategy_M5_P1( second=second, minute=minute, category_alert="comum", result="process")
                elif second == 24 and minute in constants.OBJECT_MINUTES_P1_AND_P2_30s.keys(): # atention
                    BaseStrategy.strategy_M5_P1( second=second, minute=minute, category_alert="attention", result="process")
                elif second == 47 and minute in constants.OBJECT_MINUTES_P1_AND_P2_10s.keys(): # open operation
                    BaseStrategy.strategy_M5_P1( second=second, minute=minute, category_alert="open-operation", result="open")

                ######## CHAMADA PADRÃO 2 ########
                elif second == 10 and minute in constants.OBJECT_MINUTES_P1_AND_P2.keys():     # init
                    BaseStrategy.strategy_M5_P2( second=second, minute=minute, category_alert="comum", result="process")
                elif second == 32 and minute in constants.OBJECT_MINUTES_P1_AND_P2_30s.keys(): # attention
                    BaseStrategy.strategy_M5_P2( second=second, minute=minute, category_alert="attention", result="process")
                elif second == 53 and minute in constants.OBJECT_MINUTES_P1_AND_P2_10s.keys(): # open operation
                    BaseStrategy.strategy_M5_P2( second=second, minute=minute, category_alert="open-operation", result="open")


                ######## CHAMADA VERFICAÇÃO OPERAÇÕES PADRÃO 1 ########
                elif second == 4 and minute in constants.OBJECT_CHECK_P1_AND_P2.keys():
                    BaseStrategy.check_results_operations(padrao="PADRAO-M5-V1", category_alert="checking-operations", result="checking")
                
                ######## CHAMADA VERFICAÇÃO OPERAÇÕES PADRÃO 2 ########
                elif second == 14 and minute in constants.OBJECT_CHECK_P1_AND_P2.keys():
                    BaseStrategy.check_results_operations(padrao="PADRAO-M5-V2", category_alert="checking-operations", result="checking")

        except Exception as e:
            msg_error = f"ERROR BaseStrategy.strategy_M5 | Error: {e}"
            print(msg_error)
            logging.error(msg_error)


    def strategy_M5_P1(second, minute, category_alert, result):
        try:
            sleep(1)
            print("Acionado -> strategy_M5 - PADRAO-M5-V1")
            expiration = expiration_operation_M5() # return object: expiration | expiration_timestamp
            print(f"------> expirations: {expiration}")
            message_actives_open = ChannelsWSS.get_actives_open()
            send_message_wss(message=message_actives_open)
            
            if len(variables.DATAFRAME_ACTIVES_OPEN) >= 1:
                print(f"tt DataFrame: {len(variables.DATAFRAME_ACTIVES_OPEN)}")
                for i in range(len(variables.DATAFRAME_ACTIVES_OPEN)):
                    active_id   = variables.DATAFRAME_ACTIVES_OPEN["id"][i]
                    active_name = variables.DATAFRAME_ACTIVES_OPEN["PADRAO-M5-V1"][i]
                    print(active_id, active_name, int(expiration["expiration_timestamp"]))

                    request_name = None
                    if category_alert == "comum":
                        request_name = f"{active_name} {constants.OBJECT_MINUTES_P1_AND_P2[minute]} {category_alert} {result}"
                    elif category_alert == "attention":
                        request_name = f"{active_name} {constants.OBJECT_MINUTES_P1_AND_P2_30s[minute]} {category_alert} {result}"
                    elif category_alert == "open-operation":
                        request_name = f"{active_name} {constants.OBJECT_MINUTES_P1_AND_P2_10s[minute]} {category_alert} {result}"

                    msg = ChannelsWSS.get_candles(
                        id_active=int(active_id),
                        timeframe=300,
                        expiration=int(expiration["expiration_timestamp"]),
                        amount=6,
                        active_name= request_name
                        )
                    send_message_wss(msg)
        except Exception as e:
            msg_error = f"ERROR BaseStrategy.strategy_M5_P1 | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
    
    def strategy_M5_P2(second, minute, category_alert, result):
        try:
            sleep(1)
            print("Acionado -> strategy_M5 - PADRAO-M5-V2")
            expiration = expiration_operation_M5() # return object: expiration | expiration_timestamp
            print(f"------> expirations: {expiration}")
            message_actives_open = ChannelsWSS.get_actives_open()
            send_message_wss(message=message_actives_open)
            
            if len(variables.DATAFRAME_ACTIVES_OPEN) >= 1:
                print(f"tt DataFrame: {len(variables.DATAFRAME_ACTIVES_OPEN)}")
                for i in range(len(variables.DATAFRAME_ACTIVES_OPEN)):
                    active_id   = variables.DATAFRAME_ACTIVES_OPEN["id"][i]
                    active_name = variables.DATAFRAME_ACTIVES_OPEN["PADRAO-M5-V2"][i]
                    print(active_id, active_name, int(expiration["expiration_timestamp"]))

                    request_name = None
                    if category_alert == "comum":
                        request_name = f"{active_name} {constants.OBJECT_MINUTES_P1_AND_P2[minute]} {category_alert} {result}"
                    elif category_alert == "attention":
                        request_name = f"{active_name} {constants.OBJECT_MINUTES_P1_AND_P2_30s[minute]} {category_alert} {result}"
                    elif category_alert == "open-operation":
                        request_name = f"{active_name} {constants.OBJECT_MINUTES_P1_AND_P2_10s[minute]} {category_alert} {result}"

                    msg = ChannelsWSS.get_candles(
                        id_active=int(active_id),
                        timeframe=300,
                        expiration=int(expiration["expiration_timestamp"]),
                        amount=6,
                        active_name= request_name
                        )
                    send_message_wss(msg)
        except Exception as e:
            msg_error = f"ERROR BaseStrategy.strategy_M5_P2 | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
            
    def check_results_operations(padrao, category_alert, result):
        try:
            sleep(1)
            print(f"Acionado -> check_result_operation - {padrao}")
            expiration = check_expiration_operation_M5() # return object: expiration | expiration_timestamp
            print(f"------> expirations: {expiration}")
            message_actives_open = ChannelsWSS.get_actives_open()
            send_message_wss(message=message_actives_open)
            
            if len(variables.DATAFRAME_ACTIVES_OPEN) >= 1:
                print(f"tt DataFrame: {len(variables.DATAFRAME_ACTIVES_OPEN)}")
                for i in range(len(variables.DATAFRAME_ACTIVES_OPEN)):
                    active_id   = variables.DATAFRAME_ACTIVES_OPEN["id"][i]
                    active_name = variables.DATAFRAME_ACTIVES_OPEN[padrao][i]
                    print(active_id, active_name, int(expiration["expiration_timestamp"]))

                    request_name = f"{active_name} {category_alert} {result}"

                    msg = ChannelsWSS.get_candles(
                        id_active=int(active_id),
                        timeframe=300,
                        expiration=int(expiration["expiration_timestamp"]),
                        amount=2,
                        active_name= request_name
                        )
                    send_message_wss(msg)
        except Exception as e:
            msg_error = f"ERROR BaseStrategy.check_results_operations | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
    
    
            
