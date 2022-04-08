import asyncio
import time

from socket import socket, AF_INET6, SOCK_STREAM


class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.last_seen = int(time.time())

    def dictionary(self) -> dict:
        address = f'{self.ip}:{self.port}'
        return {address: Peer(self.ip, self.port)}


class Node:
    def __init__(self, port=6101):
        self.peers: dict = Peer('127.0.0.1', 6199).dictionary()
        self.sock = socket(AF_INET6, SOCK_STREAM)
        self.sock.bind(('::', port))

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.serve_forever())

    async def serve_forever(self):
        await asyncio.gather(
            self.server(),
            self.client(),
        )

    async def server(self):
        server = await asyncio.start_server(self.receive, sock=self.sock)
        async with server:
            await server.serve_forever()

    async def client(self):
        while True:
            await self.connect()

    async def receive(self, reader, writer):
        ip, port, _, _ = writer.get_extra_info('peername')
        self.peers.update(Peer(ip, port).dictionary())
        await receive(reader, writer)

    async def connect(self):
        for address, p in self.peers.items():
            conn = asyncio.open_connection(p.ip, p.port)
            try:
                reader, writer = await asyncio.wait_for(conn, timeout=3)
            except ConnectionError:
                continue
            await send(writer)
        await asyncio.sleep(1)


async def receive(reader, writer):
    request: bytes = b'Hi i am the Server\n'
    writer.write(request)
    request: bytes = await reader.read(255)
    writer.write(request + b'\n')
    writer.close()


async def send(writer):
    writer.write(b'Hi i am the Client\n')
    writer.close()


Node().start()
