import asyncio
import time

from socket import socket, AF_INET6, SOCK_STREAM
from adamnite.serialization import INT_SIZE, from_number

TIMEOUT = 0.3


class Peer:
    def __init__(self, ip, port, reader, writer):
        self.ip = ip
        self.port = port
        self.reader: Reader = reader
        self.writer: Writer = writer
        self.last_seen = int(time.time())
        self.connected = True
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.incoming())

    async def incoming(self):
        size, _ = from_number(await self.reader.read(INT_SIZE), int())
        message = await asyncio.shield(
            asyncio.wait_for(
                self.reader.read(size),
                timeout=TIMEOUT
            )
        )
        if message == b'PING':
            self.writer.write(b'PONG')

    # __hash__ and __eq__ make Peer comparable to each other by ip
    def __hash__(self):
        return hash(self.ip)

    def __eq__(self, other):
        assert isinstance(other, type(self)), NotImplemented
        return self.ip == other.ip


class Node:
    def __init__(self, port=6101):
        self.peers: set = set()
        self.sock = socket(AF_INET6, SOCK_STREAM)
        self.sock.bind(('::', port))

    async def start_serving(self):
        server = await asyncio.start_server(self.accept, sock=self.sock)
        await server.serve_forever()

    async def accept(self, reader, writer):
        ip, port, _, _ = writer.get_extra_info('peername')
        self.peers.add(Peer(ip, port, reader, writer))


class Reader:
    async def read(self, size: int) -> bytes:
        pass


class Writer:
    def write(self, msg: bytes):
        pass
