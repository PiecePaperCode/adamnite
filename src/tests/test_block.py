import unittest

from adamnite.genesis import GENESIS_BLOCK


class TestBlock(unittest.TestCase):
    block = GENESIS_BLOCK

    def test_block(self):
        self.assertEqual(self.block.height, 0)
        self.assertEqual(self.block.previous_hash, bytes(64))
        self.assertIsInstance(self.block.block_hash, bytes)
        self.assertTrue(self.block.valid())

    def test_serialize_block(self):
        self.assertIsInstance(self.block.serialize(), bytes)

    def test_deserialize_block(self):
        serialized_block = self.block.serialize()
        block = GENESIS_BLOCK
        block.deserialize(serialized_block)
        self.assertEqual(block.previous_hash, self.block.previous_hash)
        self.assertEqual(
            block.transactions[0].amount,
            self.block.transactions[0].amount
        )
        self.assertEqual(block.timestamp, self.block.timestamp)
        self.assertEqual(block.block_hash, self.block.block_hash)

    def test_block_header(self):
        self.assertEqual(self.block.header().height, 0)

    def test_block_hash(self):
        self.assertIsInstance(self.block.hash(), bytes)
