import time
import unittest
from typing import List

from adamnite import serialization
from adamnite.block import Block
from adamnite.serialization import INT_SIZE
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

    def test_serialize_primitive(self):
        bytes_string = serialization.serialize(b"12")
        restored_class, read = serialization.deserialize(
            bytes_string,
            to=bytes()
        )
        self.assertEqual(restored_class, "123")

    def test_serialize_custom_class(self):
        bytes_class = serialization.serialize(self.CustomClass)
        restored_class, read = serialization.deserialize(
            bytes_class,
            to=self.CustomClass
        )
        self.assertEqual(self.CustomClass.string, restored_class.string)
        self.assertEqual(self.CustomClass.number, restored_class.number)
        self.assertEqual(self.CustomClass.list, restored_class.list)
        self.assertEqual(self.CustomClass.timestamp, restored_class.timestamp)
        self.assertEqual(self.CustomClass.bytes, restored_class.bytes)
        self.assertEqual(self.CustomClass.string2, restored_class.string2)

    def test_serialize_list_transactions(self):
        transactions = [
            Transaction(), Transaction(), Transaction()
        ]
        bytes_class = serialization.serialize(transactions)
        restored_class, read = serialization.deserialize(
            bytes_class,
            to=list([Transaction])
        )
        self.assertEqual(restored_class[0].sender, Transaction().sender)
        self.assertEqual(len(restored_class), 3)

    def test_serialize_nested_list_transactions(self):
        class CustomList:
            not_nested = "not_nested"
            nested: List[Transaction] = [
                Transaction(), Transaction(), Transaction()
            ]
        bytes_class = serialization.serialize(CustomList)
        restored_class, read = serialization.deserialize(
            bytes_class,
            to=CustomList
        )
        self.assertEqual(restored_class.nested[0].sender, Transaction().sender)
        self.assertEqual(len(restored_class.nested), 3)
