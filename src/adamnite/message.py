from adamnite.serialization import INT_SIZE, serialize

REQUEST = 0
RESPONSE = 1
PEERS = 0
TRANSACTIONS = 1
BLOCKS = 2


class Message:
    def __init__(self):
        self.size = INT_SIZE
        self.type: int = REQUEST
        self.resource: int = PEERS


class Request:
    def __init__(
            self,
            resource: int = PEERS,
    ):
        self.size = (INT_SIZE * 2)
        self.type: int = REQUEST
        self.resource: int = resource


class Response:
    def __init__(
            self,
            resource,
            payload,
    ):
        self.size = (INT_SIZE * 2) + len(payload)
        self.type: int = RESPONSE
        self.resource: int = resource
        self.payload = payload
