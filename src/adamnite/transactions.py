import time


class Transaction:
    def __init__(
            self,
            sender: str = 'sender',
            receiver: str = 'receiver',
            amount: int = 1,
            fee: int = 0,
            message: str = 'message',
            signature: str = 'signature',
    ):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.message = message
        self.signature = signature
        self.timestamp: int = int(time.time())
        self.hash = b"55"
