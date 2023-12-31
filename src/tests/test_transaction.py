import unittest

from secp256k1 import PrivateKey, PublicKey, ECDSA

from adamnite.account import Wallet, PrivateAccount
from adamnite.transaction import Transaction
from adamnite.serialization import serialize, deserialize


class TestTransaction(unittest.TestCase):
    private_account_1: PrivateAccount = Wallet.accounts[0]
    private_account_2: PrivateAccount = Wallet.accounts[1]
    private_key: bytes = private_account_1.private_key
    public_key: bytes = private_account_1.public_key
    transaction = Transaction(
        sender=private_account_1,
        receiver=private_account_2.public_account(),
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
        self.assertTrue(self.transaction.valid())
        self.assertFalse(self.transaction.is_staking())

    def test_transaction_equality(self):
        self.private_account_1.nonce = 0
        transaction2 = Transaction(
            sender=self.private_account_1,
            receiver=self.private_account_2.public_account(),
            amount=100,
            fee=1,
            message=b'Test Transaction'
        )
        transaction2.nonce = self.transaction.nonce
        self.assertTrue(self.transaction == transaction2)

    def test_staking_transaction(self):
        staking = Transaction(
            sender=self.private_account_1,
            receiver=self.private_account_1.public_account(),
            amount=100,
            fee=1,
            message=b'Test Staking'
        )
        self.assertTrue(staking.valid())
        self.assertTrue(staking.is_staking())
