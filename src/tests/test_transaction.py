import unittest

from secp256k1 import PrivateKey, PublicKey, ECDSA

from adamnite.account import Wallet, PrivateAccount
from adamnite.transactions import Transaction
from adamnite.serialization import serialize, deserialize


class TestTransaction(unittest.TestCase):
    private_account: PrivateAccount = Wallet.accounts[0]
    private_key: bytes = private_account.private_key
    public_key: bytes = private_account.public_key
    transaction = Transaction(
        sender=private_account,
        receiver=private_account.public_account(),
        amount=100,
        fee=1,
        message=b'Test Transaction'
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
        restored_class, _ = deserialize(bytes_class, self.transaction)
        self.assertEqual(self.transaction.sender, restored_class.sender)
        self.assertEqual(self.transaction.receiver, restored_class.receiver)

    def test_valid_transaction(self):
        self.assertEqual(Wallet.accounts[0].nonce, 1)
        self.assertTrue(self.transaction.valid())
