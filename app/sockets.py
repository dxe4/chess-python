from ws4py.websocket import WebSocket


class CoolSocket(WebSocket):
    def opened(self):
        print("socket opened", self)

    def closed(self, code, reason=None):
        print("socket closed", self)

    def received_message(self, message):
        print("received", message)
        self.send(message.data, message.is_binary)