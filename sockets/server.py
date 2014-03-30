import asyncio
import websockets

@asyncio.coroutine
def hello(websocket, uri):
    print("-----")
    name = yield from websocket.recv()
    print("< {}".format(name))
    greeting = "Hello {}!".format(name)
    print("> {}".format(greeting))
    yield from websocket.send(greeting)


start_server = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

