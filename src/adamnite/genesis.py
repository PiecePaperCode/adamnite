from adamnite.block import Block
from adamnite.account import PrivateAccount
from adamnite.transaction import Transaction


COINBASE = 10000
GENESIS_ACCOUNT = PrivateAccount()
GENESIS_TRANSACTION = Transaction(
    sender=GENESIS_ACCOUNT,
    receiver=GENESIS_ACCOUNT.public_account(),
    message=b'Adamnite: A scalable and secure blockchain platform'
)
GENESIS_TRANSACTIONS: tuple = (
    GENESIS_TRANSACTION,
)
GENESIS_BLOCK = Block(
    previous_hash=bytes(64),
    height=0,
    proposer=GENESIS_ACCOUNT,
    witnesses=(GENESIS_ACCOUNT.public_account(),),
    transactions=GENESIS_TRANSACTIONS,
)
