import unittest

from adamnite.genesis import GENESIS_TRANSACTIONS
from adamnite.message import Response, TRANSACTIONS, Message, RESPONSE
from adamnite.serialization import deserialize, serialize


class TestCrypto(unittest.TestCase):
    def test_transaction_message(self):
        message = Response(TRANSACTIONS, GENESIS_TRANSACTIONS)
        self.assertEqual(message.resource, TRANSACTIONS)
        message_bytes = serialize(message)
        restored_message, _ = deserialize(message_bytes, Message())
        if restored_message.type == RESPONSE \
                and restored_message.resource == TRANSACTIONS:
            restored_transaction, _ = deserialize(
                message_bytes, Response(TRANSACTIONS, GENESIS_TRANSACTIONS)
            )
            self.assertEqual(1, restored_transaction.payload[0].amount)
        self.assertEqual(restored_message.resource, TRANSACTIONS)
