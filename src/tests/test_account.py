import os
import unittest

from adamnite.account import Account, Wallet


class TestAccount(unittest.TestCase):
    account = Account()
    wallet = Wallet()

    def test_account(self):
        self.assertTrue(self.account.valid())

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
        self.wallet.delete_wallet()
