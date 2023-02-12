from plataform.controllers.services_aux import status_services

def send_message_wss(message):
    return status_services.WSS_OBJ.wss.send(message)