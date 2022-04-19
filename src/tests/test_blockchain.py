import unittest

from adamnite.account import PrivateAccount
from adamnite.block import Block
from adamnite.blockchain import BlockChain
from adamnite.genesis import GENESIS_BLOCK, GENESIS_ACCOUNT, COINBASE
from adamnite.transaction import Transaction


class TestBlock(unittest.TestCase):

    def test_generate_valid_blockchain(self):
        block_chain = BlockChain()
        previous_hash = GENESIS_BLOCK.block_hash
        for i in range(1, 100):
            new_block = generate_random_block(
                previous_hash=previous_hash,
                height=i
            )
            block_chain.append(new_block)
            previous_hash = new_block.block_hash
        self.assertEqual(len(block_chain.chain), 100)
        self.assertEqual(
            block_chain.accounts[GENESIS_ACCOUNT.public_account().address],
            (100 * COINBASE) - (10 * 100 * 99)
        )


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
    for i in range(10):
        receiver = PrivateAccount()
        transaction = Transaction(
            sender=sender,
            receiver=receiver.public_account(),
            amount=100
        )
        transactions.append(transaction)
    return tuple(transactions)
