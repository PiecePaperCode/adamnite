import os
import unittest

from adamnite.account import PrivateAccount, Wallet
from adamnite.blockchain import BlockChain


class TestAccount(unittest.TestCase):
    account = PrivateAccount()
    block_chain = BlockChain()
    wallet = Wallet(block_chain)
    block_chain.accounts[account.public_account().address] = 100
    wallet.accounts = [account]

    def test_account(self):
        self.assertTrue(self.account.valid())
        self.assertTrue(self.account.public_account().valid())

    def test_wallet(self):
        self.assertTrue(self.wallet.accounts[0].valid())
        wallet_file = 'wallet.nite'
        self.wallet.export_wallet(wallet_file)
        self.wallet.import_wallet(wallet_file)
        os.remove(wallet_file)
        self.assertTrue(any(
            [
                account.valid()
                for account in self.wallet.accounts
            ]
        ))
        self.assertEqual(self.wallet.balance(), 100)
