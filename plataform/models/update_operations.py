import logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs_api/logs_api.log",
    encoding="utf-8",
    format="""----------------------------------------------\nLogRecord: %(asctime)s | Level: %(levelname)s | Message: %(message)s | Module: %(module)s | Pathname: %(pathname)s | Line: %(lineno)d | ProcessName: %(processName)s""")

import config_db
from plataform.db.conn import connetion_db


def update_operations(obtect_check_operation):
    print(f"######### object_analysis: {obtect_check_operation}")
    conn = connetion_db()
    cursor = conn.cursor()
    print(" ------- CONECTION OPEN DATABASE ------- ")
    try:
        alert_time_update = obtect_check_operation["alert_time_update"]
        id_active = obtect_check_operation["id_active"]
        active = obtect_check_operation["active"]
        status_close = obtect_check_operation["status_close"]
        padrao = obtect_check_operation["padrao"]
        name_strategy = obtect_check_operation["name_strategy"]
        expiration = obtect_check_operation["expiration"]
        category_alert = obtect_check_operation["category_alert"]
        # result = obtect_check_operation["result"]

        comando_query = f'''
        SELECT * FROM {config_db.TABLE_OPERATIONS}
        WHERE
        active = "{active}" and padrao = "{padrao}" and name_strategy = "{name_strategy}" and expiration = "{expiration}"
        '''
        cursor.execute(comando_query)
        result_query = cursor.fetchall()
        print(f"\n\n--------------- Resultado da query: {result_query}\n\n")

        alert_type = "verified_operation"
        if len(result_query) >=1:
            operation_query = result_query[0][5]
            print(f"************************ operarion_query Database: {operation_query}")

            if operation_query == "-":
                comando_update = f'''
                UPDATE {config_db.TABLE_OPERATIONS}
                SET alert_time_update = "{alert_time_update}", alert_type = "{alert_type}", category_alert = "{category_alert}", result = "N/C-{status_close}"
                WHERE id_active = {id_active} and name_strategy = "{name_strategy}" and expiration = "{expiration}" and id >= 0
                '''
                cursor.execute(comando_update)
                conn.commit()
                print(comando_update)
                print(" ****** NONE --->>> OPERATION RESULT/UPDATE | Registro atualizado com sucesso. Database desconectado. ****** ")
            
            elif operation_query != "-" and status_close == "empate":
                comando_update = f'''
                UPDATE {config_db.TABLE_OPERATIONS}
                SET alert_time_update = "{alert_time_update}", alert_type = "{alert_type}", category_alert = "{category_alert}", result = "{status_close}"
                WHERE id_active = {id_active} and name_strategy = "{name_strategy}" and expiration = "{expiration}" and id >= 0
                '''
                cursor.execute(comando_update)
                conn.commit()
                print(comando_update)
                print(" ****** EMPATE --->>> OPERATION RESULT/UPDATE | Registro atualizado com sucesso. Database desconectado. ****** ")

            elif operation_query == status_close:
                comando_update = f'''
                UPDATE {config_db.TABLE_OPERATIONS}
                SET alert_time_update = "{alert_time_update}", alert_type = "{alert_type}", category_alert = "{category_alert}", result = "win"
                WHERE id_active = {id_active} and name_strategy = "{name_strategy}" and expiration = "{expiration}" and id >= 0
                '''
                cursor.execute(comando_update)
                conn.commit()
                print(comando_update)
                print(" ****** OPERATION RESULT/UPDATE | Registro atualizado com sucesso. Database desconectado. ****** ")
            
            elif operation_query != "-" and operation_query != status_close and status_close != "empate":
                comando_update = f'''
                UPDATE {config_db.TABLE_OPERATIONS}
                SET alert_time_update = "{alert_time_update}", alert_type = "{alert_type}", category_alert = "{category_alert}", result = "loss"
                WHERE id_active = {id_active} and name_strategy = "{name_strategy}" and expiration = "{expiration}" and id >= 0
                '''
                cursor.execute(comando_update)
                conn.commit()
                print(comando_update)
                print(" ****** OPERATION RESULT/UPDATE | Registro atualizado com sucesso. Database desconectado. ****** ")
        else:
            print(f" ****************** NENHUM REGISTRO ENCONTRADO ****************** {result_query}")

        cursor.close()
        conn.close()
        

    except Exception as e:
        msg_error = f"#### ERROR-1 DATABASE | UPDATE/OPERATION: {e} ####"
        logging.error(msg_error)
        try:
            cursor.close()
            conn.close()
        except Exception as e:
            msg_error = f"#### ERROR-2 DATABASE | UPDATE/OPERATION: {e} ####"
            logging.error(msg_error)