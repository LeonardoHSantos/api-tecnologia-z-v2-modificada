import requests
from plataform.controllers.prepare_data_controller.prepare_data import convert_to_json

def auth_broker(url, identifier, password):
    data = {
        "identifier": identifier,
        "password": password
    }
    r = requests.post(url=url, data=data).content
    return convert_to_json(r)