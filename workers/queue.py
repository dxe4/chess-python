import time
from uuid import uuid4
from redis import StrictRedis
from app.settings import REDIS_QUEUE_KWARGS
from common import RedisQueue



def match_players():
    queue = RedisQueue("all_players")
    _redis = StrictRedis(**REDIS_QUEUE_KWARGS)
    while True:
        time.sleep(0.5)
        if queue.qsize() < 2:
            continue

        left, right = queue.get(), queue.get()
        game_id = str(uuid4())
        _redis.publish(left, game_id)
        _redis.publish(right, game_id)