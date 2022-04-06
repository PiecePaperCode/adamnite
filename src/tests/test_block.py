import unittest

from adamnite.block import Block


class TestBlock(unittest.TestCase):
    block = Block()

    def test_block(self):
        self.assertEqual(self.block.height, 1)
        self.assertIsInstance(self.block.block_hash, bytes)
        self.assertTrue(self.block.valid())

    def test_serialize_block(self):
        self.assertIsInstance(self.block.serialize(), bytes)

    def test_deserialize_block(self):
        serialized_block = self.block.serialize()
        block = Block()
        block.deserialize(serialized_block)
        self.assertEqual(block.previous_hash, self.block.previous_hash)
        self.assertEqual(
            block.transactions[0].amount,
            self.block.transactions[0].amount
        )
        self.assertEqual(block.timestamp, self.block.timestamp)
        self.assertEqual(block.block_hash, self.block.block_hash)

    def test_block_header(self):
        self.assertEqual(self.block.header().height, 1)

    def test_block_hash(self):
        self.assertIsInstance(self.block.hash(), bytes)
