import json
import time
from collections import deque
from ws4py.websocket import WebSocket
from redis import StrictRedis
from app import settings
from common.redis_queue import RedisQueue


r_queue = RedisQueue("all_players", **settings.REDIS_QUEUE_KWARGS)
redis_client = StrictRedis(**settings.REDIS_QUEUE_KWARGS)


class PubSubPool():
    def __init__(self, size=20):
        self._free_channels = deque(
            ("queue_channel:{}".format(i) for i in range(0, 20)))
        self._occupied_channels = deque(maxlen=size)
        self._pub_subs = {
            c: self._make_pub_sub(c) for c in self._free_channels}

    def join(self):
        while len(self._free_channels) == 0:
            time.sleep(0.2)

        channel = self._free_channels.pop()
        self._occupied_channels.append(channel)
        return channel, self._pub_subs[channel]

    def free_pub_sub(self, channel):
        self._occupied_channels.remove(channel)
        self._free_channels.remove(channel)

    def _make_pub_sub(self, channel):
        pubsub = redis_client.pubsub()
        pubsub.subscribe(channel)
        return pubsub


pub_sub_pool = PubSubPool()


def join_queue(socket, data):
    _id = data["id"]
    channel, pubsub = pub_sub_pool.join()
    r_queue.put(channel)
    generator = pubsub.listen()

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