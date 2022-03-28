import time


class Transaction:
    def __init__(
            self,
            sender: str = None,
            receiver: str = None,
            amount: int = 0,
            fee: int = 0,
            message: str = None,
            signature: str = None,
    ):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.message = message
        self.signature = signature
        self.timestamp: int = int(time.time())
        self.hash = hash(self)
