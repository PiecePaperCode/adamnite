import hashlib
import json
import jsonpickle


class Blockchain_Util:

    @staticmethod
    def hashing(item):
        hash_object = hashlib.sha512(item.encode())
        item = hash_object.hexdigest()
        return item

    @staticmethod
    def encode(object):
        return jsonpickle.encode(object)

    @staticmethod
    def decode(encoded):
        return jsonpickle.decode(encoded)
