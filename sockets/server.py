import asyncio
import websockets
import json
import time

@asyncio.coroutine
def _websocket(websocket, uri):
    while True:
        if not websocket.open:
            break
        data = yield from websocket.recv()
        try:
            data = json.loads(data)
        except:
            data = {"data":data, "type": "None"}

        if data["type"] == "init":
            greeting = "Hello {}!".format("client")
            yield from websocket.send(greeting)
            websocket.initialized = True
        else:
            # data = yield from websocket.recv()
            print(websocket.initialized)


start_server = websockets.serve(_websocket, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

