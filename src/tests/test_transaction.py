import unittest

from secp256k1 import PrivateKey, PublicKey, ECDSA

from adamnite.account import Account
from adamnite.transactions import Transaction
from adamnite.serialization import serialize, deserialize


class TestTransaction(unittest.TestCase):
    curve = PrivateKey()
    private_key: bytes = curve.private_key
    public_key: bytes = curve.pubkey.serialize()
    transaction = Transaction(
        sender=Account(),
        receiver=public_key,
        amount=100,
        fee=1,
        message=b'Transaction'
    )

    def test_curve(self):
        message = b'Hello'
        signature = ECDSA().ecdsa_serialize(
            PrivateKey(self.private_key).ecdsa_sign(message)
        )
        signature = ECDSA().ecdsa_deserialize(signature)
        valid = PublicKey(
            self.public_key, raw=True
        ).ecdsa_verify(message, signature)
        self.assertTrue(valid)

    def test_serialisation_transaction(self):
        bytes_class = serialize(self.transaction)
        restored_class, _ = deserialize(bytes_class, Transaction())
        self.assertEqual(self.transaction.sender, restored_class.sender)

    def test_valid_transaction(self):
        self.assertTrue(self.transaction.valid())
