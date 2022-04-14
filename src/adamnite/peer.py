import asyncio
import time

from adamnite.message import *
from adamnite.serialization import INT_SIZE, from_number, deserialize, serialize


TIMEOUT = 0.3


class Peer:
    def __init__(self, ip, port):
        self.ip: str = ip
        self.port: int = port

    # __hash__ and __eq__ make Peer comparable to each other
    def __hash__(self):
        return hash(hash(self.ip) + hash(self.port))

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port


class ConnectedPeer:
    def __init__(self, node, ip, port, reader, writer):
        self.node = node
        self.ip = ip
        self.port = port
        self.reader = reader
        self.writer = writer
        self.last_seen = int(time.time())
        self.connected = True
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.incoming())

    async def incoming(self):
        try:
            await self.receive()
        except (BrokenPipeError, ConnectionError, AssertionError):
            self.connected = False
            await asyncio.sleep(90)
        self.node.loop.create_task(self.incoming())

    async def receive(self):
        size_byte = await self.reader.read(INT_SIZE)
        size, _ = from_number(size_byte, int())
        payload = await asyncio.wait_for(
            self.reader.read(size),
            timeout=TIMEOUT
        )
        assert len(payload) == size
        message_byte = size_byte + payload
        message, _ = deserialize(message_byte, to=Message())
        handlers = {
            REQUEST: {
                PEERS: lambda: self.send_connected_peers(message_byte)
            },
            RESPONSE: {
                PEERS: lambda: self.receive_connected_peers(message_byte)
            }
        }
        valid_type = message.type in handlers
        valid_resource = not valid_type \
            or message.resource in handlers[message.type]
        if valid_type and valid_resource:
            handler = handlers[message.type][message.resource]
            handler()
        self.last_seen = int(time.time())

    def send_connected_peers(self, message_byte: bytes):
        message, _ = deserialize(message_byte, to=Request())
        connected_peers = self.node.export_peers()
        response = Response(payload=connected_peers)
        self.writer.write(serialize(response))

    def request_connected_peers(self):
        request = Request(resource=PEERS, query=SELECT_ALL)
        self.writer.write(serialize(request))

    def receive_connected_peers(self, message_byte: bytes):
        message, _ = deserialize(message_byte, to=Response((Peer("", 0),)))
        for peer in message.payload:
            self.node.peers.add(peer)

    # __hash__ and __eq__ make Peer comparable to each other
    def __hash__(self):
        return hash(hash(self.ip) + hash(self.port))

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port
