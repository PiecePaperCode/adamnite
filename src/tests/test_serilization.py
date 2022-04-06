import time
import unittest

from adamnite import serialization


class TestSerializationJSON(unittest.TestCase):
    class CustomClass:
        class NestedClass:
            list = [1, 2, 3, 4]
        string = "string"
        number = 123
        list = ["list0", "list1", "list2"]
        tuple = ("string", "string", "string2")
        timestamp = int(time.time())
        bytes = b"12345"
        string2 = "string2"
        nested = [NestedClass(), NestedClass()]

    def test_serialize_primitive(self):
        bytes_string = serialization.serialize(b"12345")
        restored_class, read = serialization.deserialize(
            bytes_string,
            to=bytes()
        )
        self.assertEqual(restored_class, b"12345")

    def test_serialize_custom_class(self):
        bytes_class = serialization.serialize(self.CustomClass)
        restored_class, read = serialization.deserialize(
            bytes_class,
            to=self.CustomClass
        )
        self.assertEqual(self.CustomClass.string, restored_class.string)
        self.assertEqual(self.CustomClass.number, restored_class.number)
        self.assertEqual(self.CustomClass.list, restored_class.list)
        self.assertEqual(self.CustomClass.tuple, restored_class.tuple)
        self.assertEqual(self.CustomClass.timestamp, restored_class.timestamp)
        self.assertEqual(self.CustomClass.bytes, restored_class.bytes)
        self.assertEqual(self.CustomClass.string2, restored_class.string2)
        self.assertEqual(
            self.CustomClass.nested[0].list[3],
            restored_class.nested[0].list[3]
        )
