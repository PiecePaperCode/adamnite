import unittest

from adamnite.account import PrivateAccount
from adamnite.block import Block
from adamnite.blockchain import BlockChain
from adamnite.genesis import GENESIS_ACCOUNT, COINBASE, GENESIS_BLOCK
from adamnite.transaction import Transaction


class TestBlock(unittest.TestCase):

    def setUp(self) -> None:
        GENESIS_ACCOUNT.nonce = 1

    def test_generate_valid_blockchain(self):
        block_chain = BlockChain(GENESIS_BLOCK)
        previous_hash = GENESIS_BLOCK.block_hash
        for i in range(1, 99):
            new_block = generate_random_block(
                previous_hash=previous_hash,
                height=i
            )
            block_chain.append(new_block)
            previous_hash = new_block.block_hash
        self.assertEqual(99, len(block_chain.chain))
        self.assertEqual(98, block_chain.height)
        self.assertEqual(
            892000,
            block_chain.accounts[GENESIS_ACCOUNT.public_account().address]
        )

    def test_mint_new_block(self):
        block_chain = BlockChain(GENESIS_BLOCK)
        receiver = PrivateAccount()
        block_chain.pending_transactions.append(
            Transaction(
                sender=GENESIS_ACCOUNT,
                receiver=receiver.public_account(),
                amount=1
            )
        )
        block_chain.mint(GENESIS_ACCOUNT)
        self.assertEqual(2, len(block_chain.chain))
        self.assertEqual(0, len(block_chain.pending_transactions))


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
