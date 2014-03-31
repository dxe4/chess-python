import asyncio
import asyncio_redis


def example():
    key = "foobar"
    # Create connection
    connection = yield from asyncio_redis.Connection.create(host='localhost', port=6379)
    # Create subscriber.
    a = yield from connection.rpushx("foobar", "1")
    b = yield from connection.rpush("foobar", ["2"])
    # Subscribe to channel.
    x = yield from connection.lrange("foobar", 0, 5)
    d = yield from x.aslist()
    print(d)

asyncio.get_event_loop().run_until_complete(example())
asyncio.get_event_loop().run_forever()