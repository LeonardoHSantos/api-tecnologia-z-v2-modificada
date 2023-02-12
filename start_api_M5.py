from plataform.startAPI import StartAPI
from config_db import USER_IQ, PASSWORD_IQ


def start_microservices_api():
    run = StartAPI(identifier=USER_IQ, password=PASSWORD_IQ)
    run.connect_plataform_wss()
    

start_microservices_api()
