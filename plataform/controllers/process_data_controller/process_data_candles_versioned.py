import logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs_api/logs_api.log",
    encoding="utf-8",
    format="""----------------------------------------------\nLogRecord: %(asctime)s | Level: %(levelname)s | Message: %(message)s | Module: %(module)s | Pathname: %(pathname)s | Line: %(lineno)d | ProcessName: %(processName)s""")



import pandas as pd
from plataform.controllers.services_aux import variables
from plataform.controllers.datetime_controller.expiration_operations import datetime_now
from plataform.controllers.datetime_controller.expiration_operations import expiration_operation_M5
from plataform.controllers.datetime_controller.expiration_operations import check_expiration_operation_M5
from plataform.controllers.datetime_controller.expiration_operations import timestemp_converter_to_local

class Process_data_candles:
    def __init__(self, request_id) -> None:
        self.request_id = request_id
        self.list_request_id = request_id.split()

    def process_generic(self, data):
        try:
            data[["open", "close", "min", "max"]] = data[["open", "close", "min", "max"]].astype(float, errors="raise")
            print("DataFrame atualizado | Type -> Float: open, close, min, max")
            list_temp = [
                [], # 0 - status close
            ]
            for i in range(len(data)):
                try:
                    if data["close"][i] > data["open"][i]:
                        list_temp[0].append("alta")
                    elif data["close"][i] < data["open"][i]:
                        list_temp[0].append("baixa")
                    else:
                        list_temp[0].append("sem mov.")
                except Exception as e:
                    print(f"Erro durante a validação de fechamento dos candles: {e}")
                    list_temp[0].append("error/validation candle")
            data["status close"] = list_temp[0]
            return data
        except Exception as e:
            msg_error = f"ERROR Process_data_candles.process_generic | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
    
    def create_obtect_analysis(self, strategy, active_name, direction, alert_type, category_alert, result):
        try:
            id_active = variables.DATAFRAME_ACTIVES_OPEN[ variables.DATAFRAME_ACTIVES_OPEN[strategy] == active_name]["id"].values[0]
            active    = variables.DATAFRAME_ACTIVES_OPEN[ variables.DATAFRAME_ACTIVES_OPEN[strategy] == active_name]["ticker"].values[0]
            mercado   = variables.DATAFRAME_ACTIVES_OPEN[ variables.DATAFRAME_ACTIVES_OPEN[strategy] == active_name]["mercado"].values[0]

            
            # 16/02/2023 campos com "x" são essenciais para alerta no painel:
            # - option_id                                 varchar(55)
            # - open_time                                 varchar(25)
            # - expiration_time                           varchar(25)
            # - mercado                                   varchar(15)
            # - name_estrategy                            varchar(55)
            #--------------------------------------------------------------------------
            # x id                                        bigint(20) AI PK
            # x direction                                 varchar(4)
            # x active                                    varchar(20)
            # x resultado                                 varchar(25)
            # x padrao                                    varchar(25)
            # x alert_datetime                            varchar(25)
            # x expiration_alert                          varchar(25)
            # x expiration_alert_timestamp                varchar(55)
            # x status_alert                              varchar(55)
            
            
            object_analyzed = {
                # "direction": "call",
                "direction": direction,
                "active": active,
                "resultado": result,
                "padrao": strategy,
                "alert_datetime": datetime_now(tzone="America/Sao Paulo").strftime('%Y-%m-%d %H:%M:%S'),
                "expiration_alert": expiration_operation_M5()["expiration"].strftime('%Y-%m-%d %H:%M:%S'), # expiration | expiration_timestamp,
                "expiration_alert_timestamp": expiration_operation_M5()["expiration_timestamp"], # expiration | expiration_timestamp,
                "status_alert": alert_type,

                "alert_time_update": datetime_now(tzone="America/Sao Paulo").strftime('%Y-%m-%d %H:%M:%S'),
                "name_strategy": active_name,
                "mercado": mercado,
                "process_action": "analysis",
            }
            print(f"----------->>> {strategy}/{active_name}/{active} | Mensagem pronta para envio: {object_analyzed}")
            return object_analyzed
        except Exception as e:
            msg_error = f"ERROR Process_data_candles.create_obtect_analysis | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
            return "error | object_analyzed"

    def create_obtect_check_operation(self, strategy, active_name, status_close, category_alert, result):
        try:
            id_active = variables.DATAFRAME_ACTIVES_OPEN[ variables.DATAFRAME_ACTIVES_OPEN[strategy] == active_name]["id"].values[0]
            active    = variables.DATAFRAME_ACTIVES_OPEN[ variables.DATAFRAME_ACTIVES_OPEN[strategy] == active_name]["ticker"].values[0]
            
            
            object_check_operation = {
                "active": active,
                "padrao": strategy,
                "resultado": result,
                "status_close": status_close,
                "name_strategy": active_name,
                "expiration_alert": check_expiration_operation_M5()["expiration"].strftime('%Y-%m-%d %H:%M:%S'), # expiration | expiration_timestamp,
                "alert_time_update": datetime_now(tzone="America/Sao Paulo").strftime('%Y-%m-%d %H:%M:%S'),
                "process_action": "checking_results_operations",
                # "id_active": id_active,
                # "category_alert": category_alert,
            }
            print(f"----------->>> {strategy}/{active_name}/{active} | Mensagem pronta para envio: {object_check_operation}")
            return object_check_operation
        except Exception as e:
            msg_error = f"ERROR Process_data_candles.create_obtect_check_operation | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
            return "error | object_check_operation"

    def process_data_candles(self, message):
        try:
            print(f"Request_ID: {self.request_id}")
            if self.list_request_id[1] == "checking-operations":
                self.active_name     = self.list_request_id[0]
                self.category_alert  = self.list_request_id[1]
                self.result          = self.list_request_id[2]
                return self.check_data_operation(data=message)
            else:
                self.active_name     = self.list_request_id[0]
                self.alert_type      = self.list_request_id[1]
                self.category_alert  = self.list_request_id[2]
                self.result          = self.list_request_id[3]
                return self.analysis_data_principal(data=message)
        except Exception as e:
            msg_error = f"ERROR Process_data_candles.process_data_candles | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
    
    def analysis_data_principal(self, data):
        try:
            data = pd.DataFrame(data)
            if self.active_name in variables.DATAFRAME_ACTIVES_OPEN["PADRAO-M5-V1"].values:
                print(" ********** processando estratégia: PADRAO-M5-V1 ********** ")
                try:
                    list_replace_from = list(map(lambda x: timestemp_converter_to_local(int(x), "UTC", "America/Sao Paulo"), data["from"].values))
                    list_active_name  = list(map(lambda x: self.active_name, range(len(data["from"].values))))
                    print(f"valor: {list_replace_from}")
                    data["from"] = list_replace_from
                    data["active_name"] = list_active_name
                    data = self.process_generic(data)
                    print(data)
                    direction = "-"
                    try:
                        if data["status close"][0] == "baixa" and data["status close"][1] == "alta" and data["status close"][2] == "alta":
                            if data["status close"][3] == "baixa" and data["status close"][4] == "baixa" and data["status close"][5] == "alta":
                                direction = "call"
                        elif data["status close"][0] == "alta" and data["status close"][1] == "baixa" and data["status close"][2] == "baixa":
                            if data["status close"][3] == "alta" and data["status close"][4] == "alta" and data["status close"][5] == "baixa":
                                direction = "put"
                        print(f" ----------------  Fim análise PADRAO-M5-V1 direction: {direction} ----------------")
                    except Exception as e:
                        print(f"---> Erro durante validação de direção PADRAO-M5-V1: {e}")
                    
                    object_analysis = self.create_obtect_analysis(
                        strategy="PADRAO-M5-V1",
                        active_name=self.active_name,
                        direction=direction,
                        alert_type = self.alert_type,
                        category_alert=self.category_alert,
                        result=self.result,
                    )
                    # print(object_analysis)
                    return object_analysis
                except Exception as e:
                    print(e)
            
            elif self.active_name in variables.DATAFRAME_ACTIVES_OPEN["PADRAO-M5-V2"].values:
                print(" ********** processando estratégia: PADRAO-M5-V2 ********** ")
                try:
                    list_replace_from = list(map(lambda x: timestemp_converter_to_local(int(x), "UTC", "America/Sao Paulo"), data["from"].values))
                    list_active_name  = list(map(lambda x: self.active_name, range(len(data["from"].values))))
                    print(f"valor: {list_replace_from}")
                    data["from"] = list_replace_from
                    data["active_name"] = list_active_name
                    data = self.process_generic(data)
                    print(data)
                    direction = "-"
                    try:
                        if data["status close"][0] == "baixa" and data["status close"][1] == "alta" and data["status close"][2] == "baixa":
                            if data["status close"][3] == "baixa" and data["status close"][4] == "baixa" and data["status close"][5] == "baixa":
                                direction = "call"
                        elif data["status close"][0] == "alta" and data["status close"][1] == "baixa" and data["status close"][2] == "alta":
                            if data["status close"][3] == "alta" and data["status close"][4] == "alta" and data["status close"][5] == "alta":
                                direction = "put"
                        print(f" ----------------  Fim análise PADRAO-M5-V2 direction: {direction} ----------------")
                    except Exception as e:
                        print(f"---> Erro durante validação de direção PADRAO-M5-V2: {e}")
                    
                    object_analysis = self.create_obtect_analysis(
                        strategy="PADRAO-M5-V2",
                        active_name=self.active_name,
                        direction=direction,
                        alert_type = self.alert_type,
                        category_alert=self.category_alert,
                        result=self.result
                    )
                    # print(object_analysis)
                    return object_analysis       
                except Exception as e:
                    print(e)
        except Exception as e:
            msg_error = f"ERROR Process_data_candles.analysis_data_principal | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
        


    def check_data_operation(self, data):
        try:
            data = pd.DataFrame(data)
            if self.active_name in variables.DATAFRAME_ACTIVES_OPEN["PADRAO-M5-V1"].values:
                print(" ********** processandoestratégia: PADRAO-M5-V1 ********** ")
                try:
                    list_replace_from = list(map(lambda x: timestemp_converter_to_local(int(x), "UTC", "America/Sao Paulo"), data["from"].values))
                    list_active_name  = list(map(lambda x: self.active_name, range(len(data["from"].values))))
                    print(f"valor: {list_replace_from}")
                    data["from"] = list_replace_from
                    data["active_name"] = list_active_name
                    data = self.process_generic(data)
                    print(data)

                    status_close = None
                    try:
                        if data["status close"][0] == "baixa":
                            status_close = "put"
                        elif data["status close"][0] == "alta":
                            status_close = "call"
                        else:
                            status_close = "empate"
                        
                        print(f"\n\n\n ************ Status Close: {status_close} ************")
                    except Exception as e:
                        print(f"Erro ao analisar status close: {e}")
                    
                    obtect_check_operation = self.create_obtect_check_operation(
                        strategy="PADRAO-M5-V1",
                        active_name=self.active_name,
                        status_close=status_close,
                        category_alert=self.category_alert,
                        result=self.result,
                    )
                    print(obtect_check_operation)
                    return obtect_check_operation
                except Exception as e:
                    print(e)
            
            elif self.active_name in variables.DATAFRAME_ACTIVES_OPEN["PADRAO-M5-V2"].values:
                print(" ********** processandoestratégia: PADRAO-M5-V2 ********** ")
                try:
                    list_replace_from = list(map(lambda x: timestemp_converter_to_local(int(x), "UTC", "America/Sao Paulo"), data["from"].values))
                    list_active_name  = list(map(lambda x: self.active_name, range(len(data["from"].values))))
                    print(f"valor: {list_replace_from}")
                    data["from"] = list_replace_from
                    data["active_name"] = list_active_name
                    data = self.process_generic(data)
                    print(data)

                    try:
                        status_close = None
                        if data["status close"][0] == "baixa":
                            status_close = "put"
                        elif data["status close"][0] == "alta":
                            status_close = "call"
                        else:
                            status_close = "empate"
                        
                        print(f"\n\n\n ************ Status Close: {status_close} ************")
                    except Exception as e:
                        print(f"Erro ao analisar status close: {e}")
                    
                    obtect_check_operation = self.create_obtect_check_operation(
                        strategy="PADRAO-M5-V2",
                        active_name=self.active_name,
                        status_close=status_close,
                        category_alert=self.category_alert,
                        result=self.result,
                    )
                    print(obtect_check_operation)
                    return obtect_check_operation
                except Exception as e:
                    print(e)
        except Exception as e:
            msg_error = f"ERROR Process_data_candles.check_data_operation | Error: {e}"
            print(msg_error)
            logging.error(msg_error)
        