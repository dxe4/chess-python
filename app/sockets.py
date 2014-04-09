import json
# TODO probably doesn't need a module?
from common.redis_queue import RedisQueue

from ws4py.websocket import WebSocket


def join_queue(data):
    pass


def move(data):
    pass


def game_operation(data):
    pass


type_funcs = {
    "join_queue": join_queue,
    "move": move,
    "game_operation": game_operation,
}


class CoolSocket(WebSocket):

    def _parse_input(self, _json):
        _type = _json.get("type", None)
        data = _json.get("data", None)

        if _type not in type_funcs.keys():
            raise Exception("Unexpected type %s" % repr(type))

        elif data is None:
            raise Exception("No data provided")

        return _type , data

    def _process_message(self, _json):
        _type, data = self._parse_input(_json)
        type_funcs[_type](data)

    def opened(self):
        print("socket opened", self)

    def closed(self, code, reason=None):
        print("socket closed", self)

    def received_message(self, message):
        # security reasons
        if len(message.data) > 1000:
            self.close(1856, "message too long")
        print(message.data)
        try:
            _json = json.loads(message.data.decode("utf-8"))
        except:
            # security reasons
            self.close(reason="Input is not json")
            raise
        self._process_message(_json)