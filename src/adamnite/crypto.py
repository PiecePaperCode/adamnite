import os
import hashlib

from Crypto.Hash import RIPEMD160
from secp256k1 import PrivateKey, ECDSA, PublicKey


def sha512(of: bytes) -> bytes:
    assert isinstance(of, bytes)
    return bytes(hashlib.sha512(of).digest())


def ripmed160(of: bytes) -> bytes:
    assert isinstance(of, bytes)
    h = RIPEMD160.new()
    h.update(of)
    return h.digest()


def secp256k1(private_key=os.urandom(32)) -> (bytes, bytes):
    curve = PrivateKey(privkey=private_key)
    private_key: bytes = curve.private_key
    public_key: bytes = curve.pubkey.serialize()
    return private_key, public_key


def sign(private_key: bytes, message: bytes) -> bytes:
    signature = ECDSA().ecdsa_serialize(
        PrivateKey(private_key).ecdsa_sign(message)
    )
    return signature


def validate(public_key: bytes, signature: bytes, message: bytes):
    signature = ECDSA().ecdsa_deserialize(signature)
    valid = PublicKey(
        public_key, raw=True
    ).ecdsa_verify(message, signature)
    return valid
