import random
import unittest

from adamnite import serialization
from adamnite.tree import hash_sha512, merkle_tree, radix_tree
from adamnite.transactions import Transaction


class TestTree(unittest.TestCase):
    def test_merkle_root(self):
        expected_root = hash_sha512(
            hash_sha512(
                hash_sha512(
                    hash_sha512(bytes(1)) + hash_sha512(bytes(2))
                )
                +
                hash_sha512(
                    hash_sha512(bytes(3)) + hash_sha512(bytes(4))
                )
            )
            +
            hash_sha512(
                hash_sha512(
                    hash_sha512(bytes(5)) + hash_sha512(bytes(5))
                )
                +
                hash_sha512(
                    hash_sha512(bytes(5)) + hash_sha512(bytes(5))
                )
            )
        )
        custom_list = [1, 2, 3, 4, 5]
        custom_list = [bytes(item) for item in custom_list]
        root = merkle_tree(custom_list)
        self.assertEqual(root, expected_root)

    def test_merkle_transaction_root(self):
        def create_random_transactions():
            transactions = [
                Transaction(amount=random.randint(0, 99))
                for _ in range(0, 99)
            ]
            transactions = [
                serialization.serialize(transaction)
                for transaction in transactions
            ]
            return transactions
        self.assertNotEqual(
            merkle_tree(create_random_transactions()),
            merkle_tree(create_random_transactions()),
        )

    def test_radix_tree(self):
        expected_values = {
            'romane': 1,
            'romanus': 2,
            'romulus': 3,
            'rubens': 4,
            'ruber': 5,
            'rubicon': 6,
            'rubicundus': 7,
        }
        expected_tree = {
            "r": {
                "om": {
                    "ulus": 3,
                    "an": {
                        "e": 1,
                        "us": 2,
                    }
                },
                "ub": {
                    "e": {
                        "ns": 4,
                        "r": 5,
                    },
                    "ic": {
                        "on": 6,
                        "undus": 7,
                    }
                }
            }
        }
        print(expected_tree["r"]["ub"]["ic"]["on"])
