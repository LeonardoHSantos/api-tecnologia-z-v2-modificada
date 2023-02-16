import logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs_api/logs_api.log",
    encoding="utf-8",
    format="""----------------------------------------------\nLogRecord: %(asctime)s | Level: %(levelname)s | Message: %(message)s | Module: %(module)s | Pathname: %(pathname)s | Line: %(lineno)d | ProcessName: %(processName)s""")

import config_db
from plataform.db.conn import connetion_db


def insert_analysis(object_analysis):
    print(f"######### object_analysis: {object_analysis}")
    conn = connetion_db()
    cursor = conn.cursor()
    print(" ------- CONECTION OPEN DATABASE | INSERT ------- ")
    try:
        

        active = object_analysis["active"]
        direction = object_analysis["direction"]
        resultado = object_analysis["resultado"]
        padrao = object_analysis["padrao"]
        alert_datetime = object_analysis["alert_datetime"]
        expiration_alert = object_analysis["expiration_alert"]
        expiration_alert_timestamp = object_analysis["expiration_alert_timestamp"]
        status_alert = object_analysis["status_alert"]
        name_strategy = object_analysis["name_strategy"]
        mercado = object_analysis["mercado"]
        alert_time_update = object_analysis["alert_time_update"]
        # alert_time_update


        comando_query = f'''
        SELECT * FROM {config_db.TABLE_OPERATIONS}
        WHERE
        active = "{active}" and padrao = "{padrao}" and expiration_alert = "{expiration_alert}" and name_strategy = "{name_strategy}"
        '''
        cursor.execute(comando_query)
        result_query = cursor.fetchall()

        tt_query = len(result_query)
        print(f"TT Query: {result_query}")
        if tt_query == 0:
            comando_insert = f'''
            INSERT INTO {config_db.TABLE_OPERATIONS}
            (active, direction, resultado, padrao, alert_datetime, expiration_alert, expiration_alert_timestamp, status_alert, name_strategy, mercado, alert_time_update)
            VALUES
            (
                "{active}", "{direction}", "{resultado}", "{padrao}", "{alert_datetime}", "{expiration_alert}", "{expiration_alert_timestamp}", "{status_alert}", "{name_strategy}", "{mercado}", "{alert_time_update}"
            )
            '''
            print(comando_insert)
            cursor.execute(comando_insert)
            conn.commit()
            print(" ****** Registro inserido com sucesso. Database desconectado. ****** ")
        else:
            comando_update = f'''
            UPDATE {config_db.TABLE_OPERATIONS}
            SET direction = "{direction}", status_alert = "{status_alert}", resultado = "{resultado}", alert_time_update = "{alert_time_update}"
            WHERE name_strategy = "{name_strategy}" and expiration_alert = "{expiration_alert}" and id >= 0
            '''
            cursor.execute(comando_update)
            conn.commit()
            print(comando_update)
            print(" ****** Registro atualizado com sucesso. Database desconectado. ****** ")
        cursor.close()
        conn.close()
    
    except Exception as e:
        msg_error = f"#### ERROR-1 | DATABASE | INSERT: {e} ####"
        print(msg_error)
        logging.error(msg_error)
        try:
            cursor.close()
            conn.close()
        except Exception as e:
            msg_error = f"#### ERROR-2 | DATABASE | INSERT: {e} ####"
            print(msg_error)
            logging.error(msg_error)


# def insert_analysis(object_analysis):
#     print(f"######### object_analysis: {object_analysis}")
#     conn = connetion_db()
#     cursor = conn.cursor()
#     print(" ------- CONECTION OPEN DATABASE ------- ")
#     try:
#         alert_datetime = object_analysis["alert_datetime"]
#         id_active = object_analysis["id_active"]
#         active = object_analysis["active"]
#         mercado = object_analysis["mercado"]
#         direction = object_analysis["direction"]
#         padrao = object_analysis["padrao"]
#         name_strategy = object_analysis["name_strategy"]
#         expiration = object_analysis["expiration"]
#         alert_type = object_analysis["alert_type"]
#         category_alert = object_analysis["category_alert"]
#         result = object_analysis["result"]

#         if direction == "-" and alert_type == "alert-open-operation":
#             alert_type = "-"
#             result = "-"
#         alert_time_update = alert_datetime

#         comando_query = f'''
#         SELECT * FROM {config_db.TABLE_OPERATIONS}
#         WHERE
#         active = "{active}" and mercado = "{mercado}" and padrao = "{padrao}" and expiration = "{expiration}"
#         '''
#         cursor.execute(comando_query)
#         result_query = cursor.fetchall()

#         tt_query = len(result_query)
#         print(f"TT Query: {result_query}")
#         if tt_query == 0:
#             comando_insert = f'''
#             INSERT INTO {config_db.TABLE_OPERATIONS}
#             (alert_datetime, id_active, active, mercado, direction, padrao, name_strategy, expiration, alert_type, alert_time_update, category_alert, result)
#             VALUES
#             (
#                 "{alert_datetime}", {id_active}, "{active}", "{mercado}", "{direction}", "{padrao}", "{name_strategy}", "{expiration}", "{alert_type}",
#                 "{alert_time_update}", "{category_alert}", "{result}"
#             )
#             '''
#             cursor.execute(comando_insert)
#             conn.commit()
#             print(comando_insert)
#             print(" ****** Registro inserido com sucesso. Database desconectado. ****** ")
#         else:
#             comando_update = f'''
#             UPDATE {config_db.TABLE_OPERATIONS}
#             SET direction = "{direction}", alert_time_update = "{alert_time_update}", alert_type = "{alert_type}", category_alert = "{category_alert}", result = "{result}"
#             WHERE id_active = {id_active} and name_strategy = "{name_strategy}" and expiration = "{expiration}" and id >= 0
#             '''
#             cursor.execute(comando_update)
#             conn.commit()
#             print(comando_update)
#             print(" ****** Registro atualizado com sucesso. Database desconectado. ****** ")
#         cursor.close()
#         conn.close()
    
#     except Exception as e:
#         msg_error = f"#### ERROR-1 | DATABASE | INSERT: {e} ####"
#         print(msg_error)
#         logging.error(msg_error)
#         try:
#             cursor.close()
#             conn.close()
#         except Exception as e:
#             msg_error = f"#### ERROR-2 | DATABASE | INSERT: {e} ####"
#             print(msg_error)
#             logging.error(msg_error)
      



