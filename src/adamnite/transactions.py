from adamnite.account import Account
from adamnite.crypto import validate, sign
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
        self.signature = self.sign(sender.private_key)

    def valid(self) -> bool:
        assert 0 < self.amount
        assert -1 < self.fee
        serialized_header = serialize(self.header())
        valid = validate(self.sender, self.signature, serialized_header)
        return valid

    def sign(self, private_key) -> bytes:
        serialized_header = serialize(self.header())
        signature = sign(private_key, serialized_header)
        return signature

    def header(self):
        class Sign:
            sender = self.sender
            receiver = self.receiver
            amount = self.amount
            fee = self.fee
            message = self.message
        return Sign()
