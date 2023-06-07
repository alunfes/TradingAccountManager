import threading
import json

class WSCommData:
    @classmethod
    def initialize(cls):
        cls.__send_ws_message = []
        cls.__received_ws_message = []
        cls.lock = threading.Lock()

    @classmethod
    def send_message(cls, message_type:str, bot_name:str, contents):
        with cls.lock:
            cls.__send_ws_message.append(json.dumps({'type':message_type, 'from':bot_name, 'to':'tam', 'contents':contents}))
    
    @classmethod
    def get_send_message(cls):
        with cls.lock:
            if len(cls.__send_ws_message) > 0:
                data = cls.__send_ws_message.pop(0)
                return data
            else:
                return None

    @classmethod
    def get_received_message(cls):
        with cls.lock:
            if len(cls.__received_ws_message) > 0:
                data = cls.__received_ws_message.pop(0)
                return json.loads(data)
            else:
                return None
    
    @classmethod
    def add_received_message(cls, message):
        with cls.lock:
            cls.__received_ws_message.append(message)