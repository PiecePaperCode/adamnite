from typing import Literal, Union


SUPPORTED_TYPES = (bytes, str, int, list, tuple, type, object)


def serialize(to: Union[SUPPORTED_TYPES]) -> bytes:
    types_conversion: {object: object} = {
        bytes: to_bytes,
        str: to_string,
        int: to_number,
        list: to_list,
        tuple: to_list,
        type: to_class,
    }
    if type(to) not in types_conversion:
        return to_class(to)
    return types_conversion[type(to)](to)


INT_SIZE = 4


def to_bytes(to: bytes) -> bytes:
    b = bytes()
    b += to_number(len(to))
    b += to
    assert len(b) == len(to) + INT_SIZE
    return b


BYTE_ORDER: Literal["little", "big"] = "big"
ENCODING = "utf-8"


def to_string(to: str) -> bytes:
    b = len(to).to_bytes(INT_SIZE, BYTE_ORDER)
    b += to.encode(ENCODING)
    assert len(to) + INT_SIZE == len(b)
    return b


def to_number(to: int) -> bytes:
    return to.to_bytes(INT_SIZE, BYTE_ORDER)


def to_list(to: Union[list, tuple]) -> bytes:
    b = to_number(len(to))
    for item in to:
        b += serialize(item)
    return b


def to_class(to: object):
    b: bytes = bytes()
    assert hasattr(to, "__dict__"), TypeError(f"{to} Not Supported Type")
    for name, value in vars(to).items():
        if name.startswith('__'):
            continue
        elif isinstance(value, SUPPORTED_TYPES):
            b += serialize(value)
    return b


def deserialize(
        from_: bytes,
        to: Union[str, int, list, type, object],
) -> (object, int):
    types_conversion: {type: object} = {
        bytes: from_bytes,
        str: from_string,
        int: from_number,
        list: from_list,
        tuple: from_list,
        type: from_class,
    }
    if type(to) not in types_conversion:
        return from_class(from_, to)
    return types_conversion[type(to)](from_, to)


def from_bytes(from_: bytes, to: bytes) -> (str, int):
    assert isinstance(to, bytes)
    len_bytes, read = from_number(from_, int())
    bytes_array = from_[read: read + len_bytes]
    assert len_bytes == len(bytes_array)
    size = read + len_bytes
    return bytes_array, size


def from_string(from_: bytes, to: str) -> (str, int):
    assert isinstance(to, str)
    len_string, read = from_number(from_, int())
    string = from_[read: read + len_string].decode(ENCODING)
    assert len_string == len(string)
    size = read + len(string)
    return string, size


def from_number(from_: bytes, to: int) -> (str, int):
    assert isinstance(to, int)
    return int.from_bytes(from_[0:INT_SIZE], BYTE_ORDER), INT_SIZE


def from_list(from_: bytes, to: Union[list, tuple]):
    list_array = []
    len_list, read = from_number(from_, int())
    item_type = to[0]
    pointer = read
    for i in range(len_list):
        list_item, read = deserialize(from_[pointer:], item_type)
        list_array.append(list_item)
        pointer += read
    assert len_list == len(list_array)
    return list_array, pointer


def from_class(from_: bytes, to: object) -> (object, int):
    pointer = 0
    assert hasattr(to, "__dict__"), TypeError(f"{to} Not Supported Type")
    for name, value in vars(to).items():
        if name.startswith('__'):
            continue
        obj, read = deserialize(from_[pointer:], value)
        setattr(to, name, obj)
        pointer += read
    return to, pointer


class Serializable:
    def serialize(self):
        class Serialize:
            pass

        for name, value in vars(self).items():
            setattr(Serialize, name, value)
        return serialize(Serialize)

    def deserialize(self, b: bytes):
        class Deserialize:
            pass

        for name, value in vars(self).items():
            setattr(Deserialize, name, value)
        restored_class, read = deserialize(b, Deserialize)
        for name, value in vars(restored_class).items():
            if name.startswith('__'):
                continue
            setattr(self, name, value)
