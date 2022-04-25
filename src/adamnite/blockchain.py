from copy import deepcopy
from adamnite.account import PrivateAccount, Wallet
from adamnite.block import Block
from adamnite.genesis import COINBASE, ADAMNITE_GENESIS_BLOCK
from adamnite.transaction import Transaction


class BlockChain:
    def __init__(
        self,
        proposer=Wallet.accounts[0],
        genesis_block=ADAMNITE_GENESIS_BLOCK,
    ):
        self.proposer: PrivateAccount = proposer
        self.height: int = 0
        self.accounts: dict = {}
        self.nonce: dict = {}
        self.chain: list[Block] = [genesis_block]
        self.pending_transactions: list[Transaction] = []
        self.apply_coinbase(genesis_block.proposer)
        self.apply_transactions(genesis_block.transactions)

    def append(self, block: Block):
        self.chain.append(block)
        if not self.valid(after_height=self.height):
            self.chain.pop()
            return
        self.height += 1
        assert self.height == len(self.chain) - 1
        self.apply_coinbase(block.proposer)
        self.apply_transactions(block.transactions)

    def valid(self, after_height=0):
        for i in range(after_height + 1, len(self.chain)):
            block = self.chain[i]
            previous_block = self.chain[i - 1]
            if not block.previous_hash == previous_block.block_hash \
                    or not block.height - 1 == previous_block.height \
                    or not block.valid() \
                    or not self.proof_of_king(block) \
                    or not self.valid_transactions(block.transactions):
                return False
        return True

    def valid_transactions(self, transactions: tuple[Transaction]):
        nonce = deepcopy(self.nonce)
        for transaction in transactions:
            nonce[transaction.sender] += 1
            total = transaction.amount + transaction.fee
            if transaction.sender not in self.accounts:
                return False
            elif self.accounts[transaction.sender] <= total:
                return False
            elif transaction.sender not in self.nonce:
                return False
            elif not transaction.nonce <= nonce[transaction.sender]:
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
            if self.nonce[transaction.sender] != transaction.nonce:
                continue
            total = transaction.amount + transaction.fee
            self.accounts[transaction.sender] -= total
            self.nonce[transaction.sender] += 1
            if transaction.receiver not in self.accounts:
                self.accounts[transaction.receiver] = transaction.amount
                self.nonce[transaction.receiver] = 0
            else:
                self.accounts[transaction.receiver] += transaction.amount
            if transaction in self.pending_transactions:
                self.pending_transactions.remove(transaction)

    def proof_of_king(self, block):
        king: bytes = max(self.accounts, key=self.accounts.get)
        if block.proposer != king:
            return False
        return True

    def mint(self):
        king: bytes = max(self.accounts, key=self.accounts.get)
        if self.proposer.public_account().address != king \
                or len(self.pending_transactions) == 0:
            return
        new_block = Block(
            previous_hash=self.chain[-1].block_hash,
            height=self.height + 1,
            proposer=self.proposer,
            witnesses=(self.proposer.public_account(),),
            transactions=self.pending_transactions,
        )
        self.append(new_block)
