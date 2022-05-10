import os
import base58

from os.path import exists
from adamnite.crypto import secp256k1
from adamnite.serialization import deserialize, serialize


class PrivateAccount:
    def __init__(self):
        self.private_key, self.public_key = secp256k1(os.urandom(32))
        self.nonce = 0

    def public_account(self):
        return PublicAccount(public_key=self.public_key)

    def valid(self):
        _, public_key = secp256k1(self.private_key)
        assert self.public_key == public_key
        return True


class PublicAccount:
    def __init__(self, address=None, public_key=None):
        public_key = public_key or base58.b58decode(address)
        self.address = base58.b58encode(public_key)

    def valid(self):
        public_key = base58.b58decode(self.address)
        assert len(public_key) == 33 and isinstance(public_key, bytes)
        return True


class Wallet:
    def __init__(self, block_chain=None):
        self.block_chain = block_chain
    accounts: list[PrivateAccount] = []

    if exists('resources/wallet.nite'):
        with open('resources/wallet.nite', 'rb') as wallet:
            accounts, read = deserialize(wallet.read(), [PrivateAccount()])
    else:
        accounts = [
            PrivateAccount()
            for i in range(2)
        ]
        with open('resources/wallet.nite', 'wb') as wallet:
            wallet.write(serialize(accounts))

    def balance(self) -> int:
        if self.block_chain is None:
            return -1
        total_balance = 0
        for account in self.accounts:
            address = account.public_account().address
            if address in self.block_chain.accounts:
                total_balance += self.block_chain.accounts[address]
        return total_balance

    def export_wallet(self, file):
        with open(file, 'wb') as wallet:
            wallet.write(serialize(self.accounts))

    def import_wallet(self, file):
        with open(file, 'rb') as wallet:
            self.accounts, size = deserialize(
                wallet.read(),
                [PrivateAccount()]
            )
