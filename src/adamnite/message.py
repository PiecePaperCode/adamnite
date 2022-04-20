from typing import Union

from adamnite.serialization import INT_SIZE, serialize


PEERS = 0
TRANSACTIONS = 1
BLOCKS = 2
ACCOUNTS = 3

REQUEST = 0
RESPONSE = 1

SELECT_ALL: tuple[int] = (0,)


class Message:
    def __init__(self):
        self.size = INT_SIZE
        self.type: int = REQUEST
        self.resource: int = PEERS


class Request:
    def __init__(
            self,
            resource: int = PEERS,
            query: tuple[int] = SELECT_ALL,
    ):
        self.size: int = (INT_SIZE * 2) + len(serialize(query))
        self.type: int = REQUEST
        self.resource: int = resource
        self.query: tuple = query


class Response:
    def __init__(
            self,
            payload: Union[tuple, list],
    ):
        self.size = (INT_SIZE * 2) + len(serialize(payload))
        self.type: int = RESPONSE
        resource_lookup = {
            "Block": BLOCKS,
            "Transaction": TRANSACTIONS,
            "Peer": PEERS,
        }
        self.resource: int = resource_lookup[type(payload[0]).__name__]
        self.payload = payload
