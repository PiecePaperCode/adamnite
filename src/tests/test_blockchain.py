import unittest

from random import randint
from adamnite.account import PrivateAccount
from adamnite.block import Block
from adamnite.blockchain import BlockChain
from adamnite.genesis import GENESIS_BLOCK, GENESIS_ACCOUNT
from adamnite.transaction import Transaction


class TestBlock(unittest.TestCase):

    def test_generate_valid_blockchain(self):
        block_chain = BlockChain()
        previous_hash = GENESIS_BLOCK.block_hash
        for i in range(1, 9):
            new_block = generate_random_block(
                previous_hash=previous_hash,
                height=i
            )
            assert new_block.valid()
            block_chain.append(new_block)
            previous_hash = new_block.block_hash
        self.assertTrue(block_chain.valid())
        self.assertEqual(len(block_chain.chain), 9)


def generate_random_block(previous_hash: bytes, height: int) -> Block:
    assert len(previous_hash) == 64
    private_account = GENESIS_ACCOUNT
    block = Block(
        previous_hash=previous_hash,
        height=height,
        proposer=private_account,
        witnesses=tuple(),
        transactions=generate_random_transactions(private_account),
    )
    return block


def generate_random_transactions(sender: PrivateAccount) -> tuple[Transaction]:
    transactions = []
    for i in range(randint(13, 999)):
        receiver = PrivateAccount()
        transaction = Transaction(
            sender=sender,
            receiver=receiver.public_account(),
            amount=randint(1, 10)
        )
        transactions.append(transaction)
    return tuple(transactions)
