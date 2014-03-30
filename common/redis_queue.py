import redis

# Thx to Peter Hoffmann
# http://peter-hoffmann.com/2012/python-simple-queue-redis-queue.html

class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""

        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, min=0, max=5, callback=None):
        data = self.__db.lrange(self.key, min, max)
        if callback:
            return callback(data)
        return data

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)