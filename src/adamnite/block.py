import time


class Block:
    def __init__(
            self,
            height: int = 1,
            previous_hash: str = None,
            proposer: str = None,
            witnesses: [str] = None,
            signature: str = None,
            transactions: [object] = None,
    ):
        self.previous_hash = previous_hash
        self.block_hash = hash(self)
        self.timestamp: int = int(time.time())
        self.proposer = proposer
        self.height = height
        self.signature = signature
        self.transactions_root = None
        self.transactions = transactions
        self.witnesses = witnesses

    def valid(self):
        return self.height == self.height

    def header(self):
        class BlockHeader:
            height = self.height
            previous_hash = self.previous_hash
            proposer = self.proposer
            witnesses = self.witnesses
            signature = self.signature
            timestamp = self.timestamp
            block_hash = hash(self)

        return BlockHeader
