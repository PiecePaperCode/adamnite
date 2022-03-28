import unittest

from adamnite.block import Block


class TestBlock(unittest.TestCase):
    block = Block(
        height=1,
        previous_hash="123",
        proposer="123",
        witnesses=["123", "123"],
        signature="1233",
    )

    def test_block(self):
        self.assertEqual(self.block.height, 1)
