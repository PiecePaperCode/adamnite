from adamnite.block import Block
from adamnite.genesis import GENESIS_BLOCK, COINBASE
from adamnite.transaction import Transaction


class BlockChain:
    def __init__(self):
        self.accounts: dict = {}
        self.nonce: dict = {}
        self.chain: list[Block] = [GENESIS_BLOCK]
        self.height: int = 0
        self.apply_coinbase(GENESIS_BLOCK.proposer)
        self.apply_transactions(GENESIS_BLOCK.transactions)

    def append(self, block: Block):
        self.chain.append(block)
        if not self.valid(from_=self.height + 1):
            self.chain.pop()
            return
        self.height += 1
        assert self.height == len(self.chain) - 1
        self.apply_coinbase(block.proposer)
        self.apply_transactions(block.transactions)

    def valid(self, from_=1):
        for i in range(from_, len(self.chain)):
            block = self.chain[i]
            previous_block = self.chain[i-1]
            if not block.previous_hash == previous_block.block_hash \
                    or not block.height - 1 == previous_block.height \
                    or not block.valid() \
                    or not self.valid_transactions(block.transactions):
                return False
        return True

    def valid_transactions(self, transactions: tuple[Transaction]):
        nonce = {}
        for transaction in transactions:
            if transaction.sender not in self.nonce:
                return False
            elif transaction.sender not in nonce:
                nonce[transaction.sender] = self.nonce[transaction.sender]
            else:
                nonce[transaction.sender] += 1
            total = transaction.amount + transaction.fee
            if transaction.sender not in self.accounts:
                return False
            elif self.accounts[transaction.sender] <= total:
                return False
            elif nonce[transaction.sender] != transaction.nonce:
                print(nonce)
                print(nonce[transaction.sender], transaction.nonce)
                return False
        return True

    def apply_coinbase(self, proposer: bytes):
        if proposer not in self.accounts:
            self.accounts[proposer] = COINBASE
            self.nonce[proposer] = 0
        else:
            self.accounts[proposer] += COINBASE

    def apply_transactions(self, transactions: tuple[Transaction]):
        for transaction in transactions:
            total = transaction.amount + transaction.fee
            self.accounts[transaction.sender] -= total
            self.nonce[transaction.sender] += 1
            if transaction.receiver not in self.accounts:
                self.accounts[transaction.receiver] = transaction.amount
                self.nonce[transaction.receiver] = 0
            else:
                self.accounts[transaction.receiver] += transaction.amount
