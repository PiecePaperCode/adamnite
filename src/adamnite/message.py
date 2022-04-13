from adamnite.block import Block
from adamnite.node import Peer
from adamnite.serialization import INT_SIZE
from adamnite.transactions import Transaction

REQUEST = 0
RESPONSE = 1
PEERS = 0
TRANSACTIONS = 1
BLOCKS = 2
ACCOUNTS = 3
SELECT_ALL: tuple = (b'SELECT ALL',)


class Message:
    def __init__(self):
        self.size = INT_SIZE
        self.type: int = REQUEST
        self.resource: int = PEERS


class Request:
    def __init__(
            self,
            resource: int = PEERS,
            query: tuple = SELECT_ALL,
    ):
        self.size: int = (INT_SIZE * 2)
        self.type: int = REQUEST
        self.resource: int = resource
        self.query: tuple = query


class Response:
    def __init__(
            self,
            payload: tuple,
    ):
        self.size = (INT_SIZE * 2) + len(payload)
        self.type: int = RESPONSE
        resource_lookup = {
            Block.__name__: BLOCKS,
            Transaction.__name__: TRANSACTIONS,
            Peer.__name__: PEERS,
        }
        self.resource: int = resource_lookup[type(payload[0]).__name__]
        self.payload = payload
