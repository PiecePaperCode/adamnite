import unittest
from random import randint

from adamnite.account import PrivateAccount
from adamnite.block import Block
from adamnite.blockchain import BlockChain
from adamnite.transaction import Transaction


class TestBlock(unittest.TestCase):

    def test_generate_valid_blockchain(self):
        block_chain = BlockChain()
        previous_block = block_chain.chain[0]
        for i in range(1, 9):
            new_block = generate_random_block(
                previous_block.block_hash,
                i
            )
            block_chain.append(new_block)
            previous_block = new_block
        self.assertTrue(block_chain.valid())


def generate_random_block(previous_hash: bytes, height: int):
    assert len(previous_hash) == 64
    private_account = PrivateAccount()
    block = Block(
        previous_hash=previous_hash,
        height=height,
        proposer=private_account,
        witnesses=(b'rXkdZC8p1ZWJHVkTx4RDtNMf5vuvZTLYpXKRSUWgt8rL',),
        transactions=generate_random_transactions(private_account),
    )
    return block


def generate_random_transactions(sender: PrivateAccount) -> tuple:
    transactions = []
    for i in range(randint(13, 99)):
        transaction = Transaction(
            sender,
            sender.public_account()
        )
        transactions.append(transaction)
    return tuple(transactions)
