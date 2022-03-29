import time
import unittest
from typing import List

from adamnite import serialization
from adamnite.block import Block
from adamnite.transactions import Transaction


class TestSerializationJSON(unittest.TestCase):
    class CustomClass:
        string = "string"
        number = 123
        list = ["string", "string", "string2"]
        # tuple = ("string", "string", "string2")
        timestamp = int(time.time())
        bytes = b"123"
        string2 = "string2"

    def test_json_class(self):
        json = serialization.json(self.CustomClass)
        self.assertEqual(json['string'], 'string')

    def test_json_block(self):
        block = Block(height=1)

        json = serialization.json(block)
        self.assertEqual(json['height'], 1)

    def test_json_transaction(self):
        transaction = Transaction(amount=1)

        json = serialization.json(transaction)
        self.assertEqual(json['amount'], 1)

    def test_byte_class(self):
        bytes_class = serialization.to_bytes_object(self.CustomClass)
        len_string = int.from_bytes(bytes_class[0:8], "big")
        self.assertEqual(len_string, len(self.CustomClass.string))
        self.assertEqual(bytes_class[8:8+len_string].decode('utf-8'), "string")

    def test_struct_class(self):
        bytes_class = serialization.to_bytes_object(self.CustomClass)
        restored_class, read = serialization.from_bytes_object(
            bytes_class,
            to=self.CustomClass
        )
        self.assertEqual(self.CustomClass.string, restored_class.string)
        self.assertEqual(self.CustomClass.number, restored_class.number)
        self.assertEqual(self.CustomClass.list, restored_class.list)
        self.assertEqual(self.CustomClass.timestamp, restored_class.timestamp)
        self.assertEqual(self.CustomClass.bytes, restored_class.bytes)
        self.assertEqual(self.CustomClass.string2, restored_class.string2)

    def test_list_class(self):
        transactions = [
            Transaction(), Transaction(), Transaction()
        ]
        bytes_class = serialization.to_bytes_object(transactions)
        restored_class, read = serialization.from_bytes_object(
            bytes_class,
            to=transactions
        )
        self.assertEqual(restored_class[0].sender, Transaction().sender)
        self.assertEqual(len(restored_class), 3)

    def test_nested_list_class(self):
        class CustomList:
            not_nested = "not_nested"
            nested: List[Transaction] = [
                Transaction(), Transaction(), Transaction()
            ]
        bytes_class = serialization.to_bytes_object(CustomList)
        restored_class, read = serialization.from_bytes_object(
            bytes_class,
            to=CustomList
        )
        self.assertEqual(restored_class.nested[0].sender, Transaction().sender)
        self.assertEqual(len(restored_class.nested), 3)
