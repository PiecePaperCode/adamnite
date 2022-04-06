import os
import keyring

from adamnite.serialization import deserialize, serialize
from secp256k1 import PrivateKey


class Account:
    def __init__(self):
        curve = PrivateKey(privkey=os.urandom(32))
        self.private_key: bytes = curve.private_key
        self.public_key: bytes = curve.pubkey.serialize()
        self.address: bytes = self.public_key

    def valid(self):
        assert PrivateKey(
            self.private_key
        ).pubkey.serialize() == self.public_key
        return True


class Wallet:
    accounts = []
    service_name = "PyAdamnite"
    username = 'wallet'
    if keyring.get_password('PyAdamnite', 'wallet'):
        accounts, size = deserialize(
            bytes.fromhex(keyring.get_password(service_name, username)),
            [Account()]
        )
    else:
        accounts = [Account() for i in range(100)]
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
                [Account()]
            )

    def delete_wallet(self):
        keyring.delete_password(self.service_name, self.username)
