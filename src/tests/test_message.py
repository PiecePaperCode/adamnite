import unittest

from adamnite.account import PrivateAccount
from adamnite.genesis import GENESIS_BLOCK
from adamnite.message import Response, TRANSACTIONS, Message
from adamnite.node import Peer
from adamnite.serialization import deserialize, serialize
from adamnite.transactions import Transaction


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
