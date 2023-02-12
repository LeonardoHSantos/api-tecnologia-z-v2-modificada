import json

def convert_to_json(data):
    return json.loads(data)

def convert_to_string(data):
    return json.dumps(data).replace("'", '"')

def prepare_dict_to_message_websocket(name, message, request_id):
    return json.dumps(dict(name=name, msg=message, request_id=request_id)).replace("'", '"')