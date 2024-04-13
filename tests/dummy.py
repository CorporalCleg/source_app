class StubSocket:
    def __init__(self, *args):
        self.received_data = []

    def connect(self, *args):
        return 0

    def recv(self, maxsize=None):
        return '3 2 6'.encode()

    def sendall(self, data):
        self.sent_data.append(data)

    def send(self, data):
        self.received_data.append(data)
        return self.received_data

    def close(self):
        pass

class StubSocketModule:
    def __getattr__(self, name):
        if name == 'socket':
            return StubSocket
        raise AttributeError(name)