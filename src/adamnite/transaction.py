import base58

from adamnite.account import PrivateAccount, PublicAccount
from adamnite.crypto import validate, sign
from adamnite.serialization import serialize


class Transaction:
    def __init__(
            self,
            sender: PrivateAccount,
            receiver: PublicAccount,
            amount: int = 1,
            message: bytes = b'',
            fee: int = 0,
    ):
        self.sender: bytes = sender.public_account().address
        self.amount = amount
        self.receiver: bytes = receiver.address
        self.message = message
        self.fee = fee
        self.nonce = sender.nonce
        sender.nonce += 1
        self.signature = self.sign(sender.private_key)

    def valid(self) -> bool:
        assert 0 < self.amount
        assert 0 <= self.fee
        serialized_header = serialize(self.header())
        public_key = base58.b58decode(self.sender)
        valid = validate(public_key, self.signature, serialized_header)
        return valid

    def is_staking(self) -> bool:
        return self.sender == self.receiver

    def sign(self, private_key) -> bytes:
        serialized_header = serialize(self.header())
        signature = sign(private_key, serialized_header)
        return signature

    def header(self):
        class Sign:
            sender = self.sender
            amount = self.amount
            receiver = self.receiver
            message = self.message
            fee = self.fee
            nonce = self.nonce
        return Sign

    # __hash__ and __eq__ make Transactions comparable to each other
    def __hash__(self):
        return hash(hash(self.sender) + hash(self.nonce))

    def __eq__(self, other):
        return self.sender == other.sender and self.nonce == other.nonce
