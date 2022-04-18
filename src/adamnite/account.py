import os
import base58
import keyring

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
    accounts = []
    service_name = "PyAdamnite"
    username = 'wallet'
    if keyring.get_password('PyAdamnite', 'wallet'):
        accounts, size = deserialize(
            bytes.fromhex(keyring.get_password(service_name, username)),
            [PrivateAccount()]
        )
    else:
        accounts = [PrivateAccount() for i in range(100)]
        keyring.set_password(
            service_name,
            username,
            serialize(accounts).hex()
        )

    def export_wallet(self, file):
        with open(file, 'wb') as wallet:
            wallet.write(serialize(self.accounts))

    def import_wallet(self, file):
        with open(file, 'rb') as wallet:
            self.accounts, size = deserialize(
                wallet.read(),
                [PrivateAccount()]
            )

    def delete_wallet(self):
        keyring.delete_password(self.service_name, self.username)
