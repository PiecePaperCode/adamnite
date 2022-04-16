from adamnite.block import Block
from adamnite.genesis import GENESIS_BLOCK


class BlockChain:
    def __init__(self):
        self.chain: list = [GENESIS_BLOCK]

    def valid(self):
        valid_block = any([
            block.valid()
            for block in self.chain
        ])
        valid_chain = any([
            self.chain[i].block_hash == self.chain[i + 1].previous_hash
            for i in range(0, len(self.chain) - 1)
        ])
        return valid_block and valid_chain

    def append(self, block: Block):
        self.chain.append(block)
        assert self.valid()
