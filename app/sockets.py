import json
from functools import wraps
from ws4py.websocket import WebSocket
from common import RedisQueue, WebSocketPubSubPool
from concurrent.futures import ThreadPoolExecutor
from game.chess import make_game_engine

r_queue = RedisQueue("all_players")
pub_sub_pool = WebSocketPubSubPool("queue_channel", 20)
message_pool = ThreadPoolExecutor(20)

games = {}


def run_in_pool(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        message_pool.submit(f, *args, **kwargs)

    return wrapper


@run_in_pool
def join_queue(socket:WebSocket, data):
    # keep this order to avoid state conflict
    channel, pubsub = pub_sub_pool.join()
    r_queue.put(channel)
    # {'pattern': None, 'type': 'message', 'data': b'30ae154a-2397-4945-aeed-48dad6c603b6', 'channel': 'queue_channel:19'}
    msg = pub_sub_pool.next_message(channel, pubsub)
    uid = msg['data']
    if not uid in games:
        games[uid] = make_game_engine()

    games[uid].join_game(data["player"])
    socket.send(uid)


def move(socket:WebSocket, data):
    pass


def game_operation(socket:WebSocket, data):
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
            raise Exception("Unexpected type %s" % repr(_type))

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

        try:
            _json = json.loads(message.data.decode("utf-8"))
        except:
            # security reasons
            self.close(reason="Input is not json")
            raise
        self._process_message(_json)
