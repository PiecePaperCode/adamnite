import time
from typing import Union

import base58

from adamnite.account import PrivateAccount
from adamnite.crypto import sha512, sign, validate
from adamnite.tree import merkle_tree
from adamnite.serialization import Serializable, serialize


class Block(Serializable):
    def __init__(
            self,
            previous_hash: bytes,
            height: int,
            proposer: PrivateAccount,
            witnesses: tuple = (),
            transactions: Union[tuple, list] = (),
    ):
        self.previous_hash = previous_hash
        self.height = height
        self.timestamp: int = int(time.time())
        self.proposer: bytes = proposer.public_account().address
        self.signature: bytes = sign(proposer.private_key, self.proposer)
        self.witnesses = witnesses
        transactions = sorted(transactions, key=lambda x: x.nonce)
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
        return BlockHeader

    def hash(self):
        class BlockHash:
            previous_hash = self.previous_hash
            height = self.height
            timestamp = self.timestamp
            proposer = self.proposer
            signature = self.signature
            witnesses = self.witnesses
            transactions_root = self.transactions_root

        block_hash = sha512(serialize(BlockHash))
        return block_hash

    def valid(self):
        assert validate(
            public_key=base58.b58decode(self.proposer),
            signature=self.signature,
            message=self.proposer
        )
        assert self.hash() == self.block_hash
        assert self.previous_hash != self.block_hash
        assert self.transactions == \
               sorted(self.transactions, key=lambda x: x.nonce)
        assert self.transactions_root == merkle_tree(
            [
                serialize(transaction)
                for transaction in self.transactions
            ]
        )
        assert any([transaction.valid() for transaction in self.transactions])
        return True
