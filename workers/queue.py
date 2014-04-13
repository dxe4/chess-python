import time
from uuid import uuid4
from redis import StrictRedis
from app.settings import REDIS_QUEUE_KWARGS
from common import RedisQueue
from multiprocessing import Process



def match_players():
    queue = RedisQueue("all_players")
    _redis = StrictRedis(**REDIS_QUEUE_KWARGS)
    while True:
        if queue.qsize() < 2:
            time.sleep(0.5)
            continue

        left, right = queue.get(), queue.get()
        game_id = str(uuid4())
        _redis.publish(left, game_id)
        _redis.publish(right, game_id)


def start_match_process():
    p = Process(target=match_players)
    p.start()
