from secp256k1 import PrivateKey, PublicKey, ECDSA

from adamnite.account import Account
from adamnite.serialization import serialize


class Transaction:
    def __init__(
            self,
            sender: Account = Account(),
            amount: int = 1,
            receiver: bytes = b'',
            message: bytes = b'',
            fee: int = 0,
    ):
        self.sender = sender.public_key
        self.amount = amount
        self.receiver = receiver
        self.message = message
        self.fee = fee
        self.signature = self.signature(sender.private_key)

    def valid(self):
        assert 0 < self.amount
        assert -1 < self.fee
        serialized_header = serialize(self.header())
        signature = ECDSA().ecdsa_deserialize(self.signature)
        valid = PublicKey(
            self.sender, raw=True
        ).ecdsa_verify(serialized_header, signature)
        return valid

    def signature(self, private_key):
        serialized_header = serialize(self.header())
        return ECDSA().ecdsa_serialize(
            PrivateKey(private_key).ecdsa_sign(serialized_header)
        )

    def header(self):
        class Sign:
            sender = self.sender
            receiver = self.receiver
            amount = self.amount
            fee = self.fee
            message = self.message
        return Sign()