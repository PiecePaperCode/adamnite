import datetime
import unittest

from src.adamnite import serialization
from src.adamnite.block import Block
from src.adamnite.transactions import Transaction


class TestSerialization(unittest.TestCase):
    class CustomClass:
        string = "string"
        number = 123
        float = 123.123
        list = [123, 123]
        dict = {"123": 123}
        time = datetime.datetime.now()

        def function(self):
            return self.number

    def test_serialize_primitive(self):
        json = serialization.json(123)
        print(json)

    def test_serialize_class(self):
        json = serialization.json(self.CustomClass)
        self.assertEqual(json['string'], 'string')

    def test_serialize_nested_class(self):
        class CustomClass2:
            custom_class = self.CustomClass()

        json = serialization.json(CustomClass2)
        self.assertEqual(json['CustomClass']['string'], 'string')

    def test_serialize_block(self):
        block = Block(height=1)

        json = serialization.json(block)
        self.assertEqual(json['height'], 1)

    def test_serialize_transaction(self):
        transaction = Transaction(amount=1)

        json = serialization.json(transaction)
        self.assertEqual(json['amount'], 1)
