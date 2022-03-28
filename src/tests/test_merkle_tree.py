import random
import unittest

from adamnite import serialization
from adamnite.merkle_tree import hash_sha256, merkle_tree
from adamnite.transactions import Transaction


class MerkleTree(unittest.TestCase):
    def test_tree_root(self):
        expected_root = hash_sha256(
            hash_sha256(
                hash_sha256(
                    hash_sha256(bytes(1)) + hash_sha256(bytes(2))
                )
                +
                hash_sha256(
                    hash_sha256(bytes(3)) + hash_sha256(bytes(4))
                )
            )
            +
            hash_sha256(
                hash_sha256(
                    hash_sha256(bytes(5)) + hash_sha256(bytes(5))
                )
                +
                hash_sha256(
                    hash_sha256(bytes(5)) + hash_sha256(bytes(5))
                )
            )
        )
        custom_list = [1, 2, 3, 4, 5]
        custom_list = [bytes(item) for item in custom_list]
        root = merkle_tree(custom_list)
        self.assertEqual(root, expected_root)

    def test_transaction_root(self):
        def create_random_transactions():
            transactions = [
                Transaction(amount=random.randint(0, 99))
                for _ in range(0, 99)
            ]
            transactions = [
                bytes(str(serialization.json(transaction)), "utf-8")
                for transaction in transactions
            ]
            return transactions
        self.assertNotEqual(
            create_random_transactions(),
            create_random_transactions()
        )
