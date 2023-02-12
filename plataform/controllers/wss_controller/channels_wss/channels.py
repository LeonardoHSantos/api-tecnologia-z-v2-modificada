from plataform.controllers.prepare_data_controller.prepare_data import prepare_dict_to_message_websocket
from plataform.controllers.prepare_data_controller.prepare_data import convert_to_string


class ChannelsWSS:
    def send_ssid(ssid):
        name = "ssid"
        message = ssid
        return prepare_dict_to_message_websocket(name=name, message=message, request_id="")
    
    def get_actives_open():
        name = "sendMessage"
        message = {"name": "get-initialization-data", "version": "3.0", "body": {}}
        request_id = "get-underlying-list"
        return prepare_dict_to_message_websocket(name=name, message=message, request_id=request_id)

    def get_candles(id_active, timeframe, expiration, amount, active_name):
        name = 'sendMessage'
        message = {
            'name': 'get-candles',
            'version': '2.0',
            'body': {
                'active_id': id_active,
                'size': timeframe,
                'to': expiration,
                'count': amount,
            }
        }
        request_id = active_name
        return prepare_dict_to_message_websocket(name=name, message=message, request_id=request_id) 
    

