import time

from adamnite.merkle_tree import hash_sha256
from adamnite.serialization import Serializable
from adamnite.transactions import Transaction


class Block(Serializable):
    def __init__(
            self,
            height: int = 1,
            previous_hash: str = 'previous_hash',
            proposer: str = 'proposer',
            witnesses=['witnesses'],
            signature: str = 'signature',
            transactions=[Transaction(), Transaction()],
    ):
        self.previous_hash = previous_hash
        self.height = height
        self.timestamp: int = int(time.time())
        self.proposer = proposer
        self.signature = signature
        self.witnesses = witnesses
        self.transactions_root: int = 444
        self.transactions = transactions
        self.block_hash = self.hash()

    def valid(self):
        return self.height == self.height

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

        self.block_hash = hash_sha256(BlockHash().serialize())
        return self.block_hash
