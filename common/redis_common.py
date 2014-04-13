from collections import deque
import time
import redis
from app import settings


class PubSubPool():
    def __init__(self, size=20):
        self.redis_client = redis.StrictRedis(**settings.REDIS_QUEUE_KWARGS)
        self._free_channels = deque(
            ("queue_channel:{}".format(i) for i in range(0, size)))
        self._occupied_channels = deque(maxlen=size)
        self._pub_subs = {
            c: self._make_pub_sub(c) for c in self._free_channels}

    def join(self):
        while len(self._free_channels) == 0:
            time.sleep(0.5)

        channel = self._free_channels.pop()
        self._occupied_channels.append(channel)
        return channel, self._pub_subs[channel]

    def free_pub_sub(self, channel):
        self._occupied_channels.remove(channel)
        self._free_channels.remove(channel)

    def _make_pub_sub(self, channel):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        return pubsub


class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue'):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(**settings.REDIS_QUEUE_KWARGS)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue. 

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)