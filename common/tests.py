import unittest
from multiprocessing.pool import Pool
from multiprocessing import Process
from redis import StrictRedis
from common import PubSubPool, RedisQueue


class TestRedis(unittest.TestCase):
    def setUp(self):
        self.pool = PubSubPool("channel", size=2)
        self.queue = RedisQueue("test_q")

    def test_board_init(self):
        channel, pubsub = self.pool.join()
        assert "channel" in channel
        # pubsub.listen()

if __name__ == '__main__':
    unittest.main()
