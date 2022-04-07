
import unittest

from adamnite.crypto import sha512, ripmed160


class TestCrypto(unittest.TestCase):
    def test_sha512(self):
        assert len(sha512(b'123')) == 512 / 8
        self.assertIsInstance(sha512(b'123'), bytes)

    def test_ripmed160(self):
        assert len(ripmed160(b'123')) == 160 / 8
        self.assertIsInstance(ripmed160(b'123'), bytes)
