import asyncio
import copy
import logging
import time

from socket import socket, AF_INET6, SOCK_STREAM
from adamnite.message import Message, PEERS, REQUEST, Request, Response, \
    RESPONSE, SELECT_ALL
from adamnite.serialization import INT_SIZE, from_number, serialize, deserialize


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
        self.reader: Reader = reader
        self.writer: Writer = writer
        self.last_seen = int(time.time())
        self.connected = True
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.incoming())

    async def incoming(self):
        size_byte = await self.reader.read(INT_SIZE)
        size, _ = from_number(size_byte, int())
        payload = await asyncio.wait_for(
            self.reader.read(size),
            timeout=TIMEOUT
        )
        assert len(payload) == size
        message_byte = size_byte + payload
        message, _ = deserialize(message_byte, to=Message())
        handler = {
            REQUEST: {
                PEERS: lambda: self.send_connected_peers(message_byte)
            },
            RESPONSE: {
                PEERS: lambda: self.receive_connected_peers(message_byte)
            }
        }
        valid_type = message.type in handler
        valid_resource = not valid_type \
            or message.resource in handler[message.type]
        if valid_type and valid_resource:
            handler[message.type][message.resource]()
        self.last_seen = int(time.time())
        self.node.loop.create_task(self.incoming())

    def send_connected_peers(self, message_byte: bytes):
        message, _ = deserialize(message_byte, to=Request())
        connected_peers = self.node.export_peers()
        response = Response(payload=connected_peers)
        self.writer.write(serialize(response))

    def receive_connected_peers(self, message_byte: bytes):
        message, _ = deserialize(message_byte, to=Response((Peer("", 0),)))
        for peer in message.payload:
            host_ip = peer.ip == "::ffff:127.0.0.1"
            host_port = peer.port == self.node.listening_port
            if host_ip and host_port:
                continue
            self.node.peers.add(peer)

    def request_connected_peers(self):
        request = Request(resource=PEERS, query=SELECT_ALL)
        self.writer.write(serialize(request))

    # __hash__ and __eq__ make Peer comparable to each other
    def __hash__(self):
        return hash(hash(self.ip) + hash(self.port))

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port


class Node:
    def __init__(self, port=6101):
        self.listening_port = port
        self.peers = set()
        self.connected_peers = set()
        self.sock = socket(AF_INET6, SOCK_STREAM)
        self.sock.bind(('::', port))
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.connect())
        self.loop.create_task(self.request_peers())

    async def start_serving(self):
        logging.log(logging.INFO, "Start Serving")
        server = await asyncio.start_server(self.accept, sock=self.sock)
        await server.start_serving()

    async def accept(self, reader, writer):
        ip, port, _, _ = writer.get_extra_info('peername')
        port, _ = deserialize(await reader.read(INT_SIZE), to=int())
        self.connected_peers.add(
            ConnectedPeer(self, ip, port, reader, writer)
        )
        logging.log(logging.INFO, f"Connection from {ip} {port}")

    async def connect(self):
        peers = copy.deepcopy(self.peers)
        for peer in peers:
            host_ip = peer.ip == "::ffff:127.0.0.1"
            host_port = peer.port == self.listening_port
            if host_ip and host_port:
                continue
            conn = asyncio.open_connection(peer.ip, peer.port)
            try:
                reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
            except ConnectionError:
                continue
            writer.write(serialize(self.listening_port))
            connected_peer = ConnectedPeer(
                self,
                peer.ip, peer.port,
                reader, writer
            )
            self.connected_peers.add(connected_peer)
            connected_peer.request_connected_peers()
            logging.log(logging.INFO, f"Connection to {peer.ip} {peer.port}")
        await asyncio.sleep(3)
        self.loop.create_task(self.connect())

    async def request_peers(self):
        for peer in self.connected_peers:
            peer.request_connected_peers()
        await asyncio.sleep(3)
        self.loop.create_task(self.request_peers())
        logging.log(logging.INFO, f"Sync Peers")

    def export_peers(self) -> tuple:
        peers = []
        for peer in self.connected_peers:
            peers.append(Peer(peer.ip, peer.port))
        return tuple(peers)


class Reader:
    async def read(self, size: int) -> bytes:
        pass


class Writer:
    def write(self, msg: bytes):
        pass

    def close(self):
        pass
