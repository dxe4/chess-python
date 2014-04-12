import json
import time
from app import settings
from common.redis_queue import RedisQueue
from ws4py.websocket import WebSocket
from redis import StrictRedis
from collections import deque, namedtuple

r_queue = RedisQueue("all_players", **settings.REDIS_QUEUE_KWARGS)
redis_client = StrictRedis(**settings.REDIS_QUEUE_KWARGS)
PubSub = namedtuple("channel", "pubsub")


class PubSubPool():
    def __init__(self, size=20):
        self._free_pub_subs = deque(
            (self._make_pub_sub(i) for i in range(0, 20)), maxlen=size)
        self._occupied_pub_subs = deque(maxlen=size)

    @property
    def pub_sub(self):
        while len(self._free_pub_subs) == 0:
            time.sleep(0.2)

        pubsub = self._free_pub_subs.pop()
        self._occupied_pub_subs.append(pubsub)
        return pubsub

    def _make_pub_sub(self, channel_number):
        channel = "queue_channel:{}".format(channel_number)
        pubsub = redis_client.pubsub()
        pubsub.subscribe(channel)
        return PubSub(channel_number, pubsub)

pub_sub_pool = PubSubPool()

def join_queue(socket, data):
    _id = data["id"]
    pub_sub = pub_sub_pool.pub_sub()
    r_queue.put(pub_sub.channel)
    generator = pub_sub.pubsub.listen()

    stop = False
    while not stop:
        msg = next(generator)
        print("msg", msg)
        if msg["type"] == "message":
            stop = True

    print("done")


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