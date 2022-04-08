import os
import unittest

from adamnite.account import PrivateAccount, Wallet


class TestAccount(unittest.TestCase):
    account = PrivateAccount()
    wallet = Wallet()

    def test_account(self):
        self.assertTrue(self.account.valid())
        self.assertTrue(self.account.public_account().valid())
        print(self.account.public_account().address)

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
