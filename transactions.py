import blockchainutils
import re
import rlp #Based of PyEthereum Implementation
from ecdsa import VerifyingKey, BadSignatureError

class Transaction():
    def _init_(*args):
        self = args[0]
        if len(args) == 2:
            self.parse(args[1])
        else:
            self.number = args[1]
            self.recevier = args[2]
            self.amount = args[3]
            self.fee = args[4]
            self.message = args[5]
            self.timestamp = args[6]


    def message_parsing(self,message):
        if re.match('^[0-9a-fA-F]*$',data):
            data = data.decode('hex')
        o = rlp.unparse(data)
        self.nonce = o[0]
        self.to = o[1]
        self.value = o[2]
        self.fee = o[3]
        self.data = rlp.decode(o[4])
        self.v = o[5]
        self.r = o[6]
        self.s = o[7]
        hash = hashing(rlp.encode)

    def create_signature(self,secret):
        self.signature = secret.sign(self.hash().rlp.encode)

    def verify_signature(self, verifying_key: VerifyingKey):
        try:
            verifying_key.verify(bytes.fromhex(self.signature),
                      self.display().encode("utf-8"))
            return True
        except BadSignatureError:
            return False
