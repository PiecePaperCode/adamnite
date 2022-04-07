import hashlib
from Crypto.Hash import RIPEMD160


def sha512(of: bytes) -> bytes:
    assert isinstance(of, bytes)
    return bytes(hashlib.sha512(of).digest())


def ripmed160(of: bytes) -> bytes:
    assert isinstance(of, bytes)
    h = RIPEMD160.new()
    h.update(of)
    return h.digest()
