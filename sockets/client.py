import asyncio
import websockets

@asyncio.coroutine
def hello():
    print("-")
    websocket = yield from websockets.connect('ws://localhost:8765/')
    name = "dsa"
    yield from websocket.send(name)
    print("> {}".format(name))
    greeting = yield from websocket.recv()
    print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())