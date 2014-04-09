import json

from ws4py.websocket import WebSocket


def join_queue(_json):
    pass

def move(_json):
    pass

def game_operation(_json):
    pass

type_funcs = {
    "join_queue": join_queue,
    "move": move,
    "game_operation": game_operation,
}

class CoolSocket(WebSocket):
    def _process_message(self, _json):
        type = _json["type"]
        
        if not type in type_funcs.keys():
            raise Exception("Unexpected type %s" % repr(type))

        type_funcs[type](_json)

    def opened(self):
        print("socket opened", self)

    def closed(self, code, reason=None):
        print("socket closed", self)

    def received_message(self, message):
        # security reasons
        if len(message.data) > 1000:
            self.close(1856, "message too long")

        try:
            _json = json.loads(message.data.decode("utf-8"))
        except:
            # security reasons
            self.close(reason="Input is not json")
            raise
        self._process_message(_json)