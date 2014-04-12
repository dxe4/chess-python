import json
# TODO probably doesn't need a module?
from app import settings
from common.redis_queue import RedisQueue
from ws4py.websocket import WebSocket
from redis import StrictRedis

r_queue = RedisQueue("all_players", **settings.REDIS_QUEUE_KWARGS)
r = StrictRedis(**settings.REDIS_QUEUE_KWARGS)


def join_queue(socket, data):
    _id = data["id"]
    r_queue.put(_id)
    pubsub = r.pubsub()
    channel = "pending:{}".format(_id)

    stop = False

    pubsub.subscribe(channel)
    generator = pubsub.listen()

    while not stop:
        msg = next(generator)
        if msg["type"] == "message":
            stop = True

    pubsub.unsubscribe(channel)


def move(socket, data):
    pass


def game_operation(socket, data):
    pass


type_funcs = {
    "join_queue": join_queue,
    "move": move,
    "game_operation": game_operation,
}


class CoolSocket(WebSocket):

    def _parse_input(self, _json):
        print(_json)
        _type = _json.get("type", None)
        data = _json.get("data", None)

        if _type not in type_funcs.keys():
            raise Exception("Unexpected type %s" % repr(type))

        elif data is None:
            raise Exception("No data provided")

        return _type, data

    def _process_message(self, _json):
        _type, data = self._parse_input(_json)
        type_funcs[_type](self, data)

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