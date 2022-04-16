import asyncio
import copy
import json

from pathlib import Path
from socket import socket, AF_INET6, SOCK_STREAM
from adamnite.logging import logger
from adamnite.peer import Peer, ConnectedPeer, TIMEOUT
from adamnite.serialization import INT_SIZE, serialize, deserialize


class Node:
    def __init__(self, port=6101):
        self.sock = socket(AF_INET6, SOCK_STREAM)
        self.sock.bind(('::', port))
        self.myself = Peer("::ffff:127.0.0.1", port)
        self.peers: set = import_peers()
        self.connected_peers = set()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.connect())
        self.loop.create_task(self.request_peers())

    async def start_serving(self):
        logger.info("Start Serving")
        server = await asyncio.start_server(self.accept, sock=self.sock)
        await server.serve_forever()

    async def accept(self, reader, writer):
        ip, port, _, _ = writer.get_extra_info('peername')
        port, _ = deserialize(await reader.read(INT_SIZE), to=int())
        peer = Peer(ip, port)
        if peer in self.connected_peers:
            return
        self.connected_peers.add(
            ConnectedPeer(self, ip, port, reader, writer)
        )
        logger.info(f"Connection from {ip} {port}")

    async def connect(self):
        peers = copy.deepcopy(self.peers)
        for peer in peers:
            if peer in self.connected_peers:
                continue
            conn = asyncio.open_connection(peer.ip, peer.port)
            try:
                reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
            except ConnectionError:
                continue
            writer.write(serialize(self.myself.port))
            connected_peer = ConnectedPeer(
                self,
                peer.ip, peer.port,
                reader, writer
            )
            self.connected_peers.add(connected_peer)
            logger.info(f"Connection to {peer.ip} {peer.port}")
        await asyncio.sleep(3)
        self.loop.create_task(self.connect())

    async def request_peers(self):
        for peer in self.connected_peers:
            peer.request_connected_peers()
        logger.info(f'Currently Connected {len(self.connected_peers)}')
        await asyncio.sleep(3)
        self.loop.create_task(self.request_peers())

    def export_peers(self) -> tuple:
        peers = []
        for peer in self.connected_peers:
            peers.append(Peer(peer.ip, peer.port))
        return tuple(peers)

    def remove_not_connected_peers(self):
        connected = set()
        for peer in self.connected_peers:
            if peer.connected:
                connected.add(peer)
        self.connected_peers = connected


def import_peers() -> set:
    path = Path.cwd() / 'resources' / 'peers.json'
    with open(Path(path), 'r') as file:
        peers = file.read()
    peers = json.loads(peers)
    peers = {Peer(peer[0], peer[1]) for peer in peers}
    assert isinstance(peers, set)
    return peers
