import asyncio
import time

from adamnite.genesis import *
from adamnite.message import *
from adamnite.logging import logger
from adamnite.serialization import INT_SIZE, from_number, deserialize, serialize


TIMEOUT = 1


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
        except (BrokenPipeError, ConnectionError, AssertionError) as e:
            self.connected = False
            # self.node.remove_not_connected_peers()
            logger.info(f"Disconnected {self.ip} {self.port} {e}")
            return
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
                PEERS: lambda: self.send_connected_peers(message_byte),
                BLOCKS: lambda: self.send_blocks(message_byte),
                TRANSACTIONS: lambda: self.send_transactions(message_byte),
            },
            RESPONSE: {
                PEERS: lambda: self.receive_connected_peers(message_byte),
                BLOCKS: lambda: self.receive_blocks(message_byte),
                TRANSACTIONS: lambda: self.receive_transactions(message_byte),
            }
        }
        valid_type = message.type in handlers
        assert valid_type
        valid_resource = message.resource in handlers[message.type]
        assert valid_resource
        handler = handlers[message.type][message.resource]
        handler()
        self.last_seen = int(time.time())

    def send_connected_peers(self, message_byte: bytes):
        message, size = deserialize(message_byte, to=Request())
        assert len(message_byte) == size
        connected_peers = self.node.export_peers()
        response = Response(payload=connected_peers)
        self.writer.write(serialize(response))

    def request_connected_peers(self):
        request = Request(resource=PEERS, query=SELECT_ALL)
        self.writer.write(serialize(request))

    def receive_connected_peers(self, message_byte: bytes):
        message, size = deserialize(message_byte, to=Response((Peer("", 0),)))
        assert len(message_byte) == size
        for peer in message.payload:
            self.node.peers.add(peer)

    def send_blocks(self, message_byte: bytes):
        message, size = deserialize(message_byte, to=Request())
        assert len(message_byte) == size
        if message.query == SELECT_ALL:
            response = Response(payload=self.node.block_chain.chain)
            self.writer.write(serialize(response))
            return
        blocks = []
        for height in message.query:
            if height <= self.node.block_chain.height:
                blocks.append(self.node.block_chain.chain[height])
            elif self.node.block_chain.height < height:
                blocks.append(self.node.block_chain.chain[-1])
                break
        response = Response(payload=blocks)
        self.writer.write(serialize(response))

    def request_blocks(self, query=SELECT_ALL):
        request = Request(resource=BLOCKS, query=query)
        self.writer.write(serialize(request))

    def receive_blocks(self, message_byte: bytes):
        message, size = deserialize(message_byte, to=Response((GENESIS_BLOCK,)))
        assert len(message_byte) == size
        for block in message.payload:
            self.node.block_chain.append(block)

    def send_transactions(self, message_byte: bytes):
        message, size = deserialize(message_byte, to=Request())
        assert len(message_byte) == size
        transactions: list = self.node.block_chain.pending_transactions
        if len(transactions) == 0:
            return
        response = Response(payload=transactions)
        self.writer.write(serialize(response))

    def request_transactions(self):
        request = Request(resource=TRANSACTIONS, query=SELECT_ALL)
        self.writer.write(serialize(request))

    def receive_transactions(self, message_byte: bytes):
        message, size = deserialize(
            message_byte,
            to=Response((GENESIS_TRANSACTION,))
        )
        assert len(message_byte) == size
        for transaction in message.payload:
            assert transaction.valid()
            if transaction not in self.node.block_chain.pending_transactions:
                self.node.block_chain.pending_transactions.append(transaction)

    # __hash__ and __eq__ make Peer comparable to each other
    def __hash__(self):
        return hash(hash(self.ip) + hash(self.port))

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port
