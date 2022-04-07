import time

from secp256k1 import PrivateKey, ECDSA
from adamnite.account import Account
from adamnite.crypto import sha512
from adamnite.tree import merkle_tree
from adamnite.serialization import Serializable, serialize
from adamnite.transactions import Transaction


class Block(Serializable):
    def __init__(
            self,
            previous_hash: bytes = b'previous_hash',
            height: int = 1,
            account: Account = Account(),
            witnesses: list = ('witnesses', 'witnesses'),
            transactions: list = (Transaction(), Transaction()),
    ):
        self.previous_hash = previous_hash
        self.height = height
        self.timestamp: int = int(time.time())
        self.proposer: bytes = account.public_key
        self.signature: bytes = ECDSA().ecdsa_serialize(
            PrivateKey(account.private_key).ecdsa_sign(self.proposer)
        )
        self.witnesses = witnesses
        self.transactions_root: bytes = merkle_tree(
            [
                serialize(transaction)
                for transaction in transactions
            ]
        )
        self.transactions = transactions
        self.block_hash = self.hash()

    def header(self):
        class BlockHeader(Serializable):
            previous_hash = self.previous_hash
            height = self.height
            timestamp = self.timestamp
            proposer = self.proposer
            signature = self.signature
            witnesses = self.witnesses
            transactions_root = self.transactions_root
            block_hash = self.block_hash

        return BlockHeader()

    def hash(self):
        class BlockHash(Serializable):
            previous_hash = self.previous_hash
            height = self.height
            timestamp = self.timestamp
            proposer = self.proposer
            signature = self.signature
            witnesses = self.witnesses
            transactions_root = self.transactions_root

        self.block_hash = sha512(BlockHash().serialize())
        return self.block_hash

    def valid(self):
        assert self.hash() == self.block_hash
        assert self.transactions_root == merkle_tree(
            [
                serialize(transaction)
                for transaction in self.transactions
            ]
        )
        assert any([transaction.valid() for transaction in self.transactions])
        return True
