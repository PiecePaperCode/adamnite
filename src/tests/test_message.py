import asyncio
import unittest
import random

from adamnite.account import PrivateAccount
from adamnite.block import Block
from adamnite.blockchain import BlockChain
from adamnite.genesis import GENESIS_BLOCK, GENESIS_TRANSACTION, \
    GENESIS_ACCOUNT, COINBASE
from adamnite.message import *
from adamnite.node import Node
from adamnite.peer import Peer, TIMEOUT
from adamnite.serialization import deserialize, serialize, INT_SIZE, from_number
from adamnite.transaction import Transaction
from tests.test_blockchain import generate_random_block
from tests.test_node import connect

PORT = random.randint(6101, 6198)


class TestMessages(unittest.TestCase):
    block = GENESIS_BLOCK
    sender = PrivateAccount()
    receiver = PrivateAccount().public_account()
    transaction = Transaction(
        sender=sender,
        receiver=receiver,
        amount=100,
    )

    def setUp(self) -> None:
        global PORT
        PORT = random.randint(6101, 7000)
        self.node = Node(port=PORT)
        self.node.block_chain = BlockChain(GENESIS_BLOCK)
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.node.start_serving())

    def test_transaction_message(self):
        message = Response(
            payload=(self.transaction,)
        )
        self.assertEqual(message.resource, TRANSACTIONS)
        message_bytes = serialize(message)
        restored_message, _ = deserialize(message_bytes, Message())
        restored_transaction, _ = deserialize(
            from_=message_bytes,
            to=Response((self.transaction,))
        )
        self.assertEqual(100, restored_transaction.payload[0].amount)

    def test_block_message(self):
        message = Response(
            payload=(self.block,)
        )
        message_bytes = serialize(message)
        restored_message, _ = deserialize(
            from_=message_bytes,
            to=message
        )
        self.assertEqual(0, restored_message.payload[0].height)

    def test_peer_message(self):
        message = Response(
            payload=(Peer("127.0.0.1", 6101),)
        )
        message_bytes = serialize(message)
        restored_message, _ = deserialize(
            from_=message_bytes,
            to=message
        )
        self.assertEqual(6101, restored_message.payload[0].port)

    def test_send_peer_message(self):
        async def run_test():
            peers = (Peer("::ffff:127.0.0.1", PORT),)
            block_message = await send_message(PEERS, peers)
            return block_message.payload

        response = self.loop.run_until_complete(run_test())
        self.assertEqual(response[0].ip, '::ffff:127.0.0.1')

    def test_send_block_message(self):
        async def run_test() -> list[Block]:
            block_message = await send_message(BLOCKS, (GENESIS_BLOCK,))
            return block_message.payload

        blocks = self.loop.run_until_complete(run_test())
        self.assertEqual(blocks[0].height, 0)

    def test_send_transaction_message(self):
        async def run_test() -> set[Transaction]:
            transactions_message = await send_message(
                TRANSACTIONS,
                (GENESIS_TRANSACTION,)
            )
            return transactions_message.payload

        self.node.block_chain.pending_transactions.append(GENESIS_TRANSACTION)
        transactions = self.loop.run_until_complete(run_test())
        self.assertEqual(transactions[0], GENESIS_TRANSACTION)

    def disable_test_send_block_response(self):
        async def run_test():
            previous_hash = GENESIS_BLOCK.block_hash
            reader, writer = await connect(PORT)
            blocks = []
            for i in range(1, 99):
                new_block = generate_random_block(
                    previous_hash=previous_hash,
                    height=i
                )
                blocks.append(new_block)
                previous_hash = new_block.block_hash
            response = Response(blocks)
            writer.write(serialize(response))
            while len(self.node.block_chain.chain) < 99:
                await asyncio.sleep(0.1)

        self.loop.run_until_complete(asyncio.wait_for(run_test(), 10))
        self.assertEqual(self.node.block_chain.height, 98)


async def send_message(resource: int, payload_type: tuple):
    message = Request(
        resource=resource,
        query=SELECT_ALL
    )
    reader, writer = await connect(PORT)
    writer.write(serialize(message))
    size_byte = await reader.read(INT_SIZE)
    size, _ = from_number(size_byte, int())
    payload = await asyncio.wait_for(
        reader.read(size),
        timeout=TIMEOUT
    )
    assert len(payload) == size
    message_byte = size_byte + payload
    message, _ = deserialize(message_byte, Response(payload_type))
    return message
