from adamnite.block import Block
from adamnite.account import PrivateAccount, PublicAccount
from adamnite.transactions import Transaction

GENESIS_ACCOUNT = PrivateAccount()
GENESIS_TRANSACTIONS = (
    Transaction(
        sender=GENESIS_ACCOUNT,
        receiver=PublicAccount(
            address=b'rXkdZC8p1ZWJHVkTx4RDtNMf5vuvZTLYpXKRSUWgt8rL'
        ),
        message=b'Adamnite: A scalable and secure blockchain platform'
    ),
)
GENESIS_BLOCK = Block(
    previous_hash=bytes(64),
    height=0,
    proposer=GENESIS_ACCOUNT,
    witnesses=(b'rXkdZC8p1ZWJHVkTx4RDtNMf5vuvZTLYpXKRSUWgt8rL',),
    transactions=GENESIS_TRANSACTIONS,
)
