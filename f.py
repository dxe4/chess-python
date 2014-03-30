import asyncio
import asyncio_redis


def example():
    # Create connection
    connection = yield from asyncio_redis.Connection.create(host='localhost', port=6379)
    # Create subscriber.
    subscriber = yield from connection.start_subscribe()
    # Subscribe to channel.
    yield from subscriber.subscribe([ 'our-channel' ])
    # Inside a while loop, wait for incoming events.
    while True:
        reply = yield from subscriber.next_published()
        print('Received: ', repr(reply.value), 'on channel', reply.channel)


asyncio.get_event_loop().run_until_complete(example())
asyncio.get_event_loop().run_forever()