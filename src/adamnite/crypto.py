import hashlib


def sha512(of: bytes):
    assert isinstance(of, bytes)
    return bytes(hashlib.sha512(of).digest())
