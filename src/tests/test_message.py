import asyncio
import unittest
import random

from adamnite.account import PrivateAccount
from adamnite.block import Block
from adamnite.genesis import GENESIS_BLOCK, GENESIS_TRANSACTION
from adamnite.message import *
from adamnite.node import Node
from adamnite.peer import Peer, TIMEOUT
from adamnite.serialization import deserialize, serialize, INT_SIZE, from_number
from adamnite.transaction import Transaction

from tests.test_node import connect

PORT = random.randint(6101, 6198)


class TestCrypto(unittest.TestCase):
    block = GENESIS_BLOCK
    sender = PrivateAccount()
    receiver = PrivateAccount().public_account()
    transaction = Transaction(
        sender=sender,
        receiver=receiver,
        amount=100,
    )

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

    node = Node(port=PORT)
    node.peers = {Peer('::ffff:127.0.0.1', PORT)}
    loop = asyncio.get_event_loop()
    loop.create_task(node.start_serving())

    def disable_test_send_peer_message(self):
        async def run_test():
            peers = (Peer("::ffff:127.0.0.1", PORT),)
            block_message = await send_message(PEERS, peers)
            return block_message.payload

        response = self.loop.run_until_complete(run_test())
        self.assertEqual(response[0].ip, '::ffff:127.0.0.1')

    def disable_send_block_message(self):
        async def run_test() -> list[Block]:
            block_message = await send_message(BLOCKS, (GENESIS_BLOCK,))
            return block_message.payload

        blocks = self.loop.run_until_complete(run_test())
        self.assertEqual(blocks[0].height, 0)

    def disable_send_transaction_message(self):
        self.node.block_chain.pending_transactions.add(GENESIS_TRANSACTION)

        async def run_test() -> set[Transaction]:
            transactions_message = await send_message(
                TRANSACTIONS,
                (GENESIS_TRANSACTION,)
            )
            return transactions_message.payload

        transactions = self.loop.run_until_complete(run_test())
        self.assertEqual(transactions[0], GENESIS_TRANSACTION)


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
