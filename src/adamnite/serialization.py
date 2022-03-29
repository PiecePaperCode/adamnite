from typing import Literal, Union


class Serializable:
    def serialize(self):
        class Serialize:
            pass

        for name, value in vars(self).items():
            setattr(Serialize, name, value)
        return to_bytes_object(Serialize)

    def deserialize(self, b: bytes):
        class Deserialize:
            pass

        for name, value in vars(self).items():
            setattr(Deserialize, name, value)
        block, read = from_bytes_object(b, Deserialize)
        for name, value in vars(block).items():
            if name.startswith('__'):
                continue
            setattr(self, name, value)


def json(to_serialize) -> dict:
    dictionary = {}
    for name, value in vars(to_serialize).items():
        if name.startswith('__'):
            continue
        if isinstance(value, (str, int, float, list, dict)):
            dictionary.update({name: value})
    return dictionary


def to_bytes_object(to: Union[str, int, list, type]) -> bytes:
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
    return to


BYTE_ORDER: Literal["little", "big"] = "big"
ENCODING = "utf-8"


def to_string(to: str) -> bytes:
    b: bytes = bytes()
    b += len(to).to_bytes(INT_SIZE, BYTE_ORDER)
    b += to.encode(ENCODING)
    assert len(to) + INT_SIZE == len(b)
    return b


def to_number(to: int) -> bytes:
    return to.to_bytes(INT_SIZE, BYTE_ORDER)


def to_list(to: Union[list, tuple]) -> bytes:
    b = bytes()
    b += to_number(len(to))
    for item in to:
        size = len(to_bytes_object(item))
        b += to_number(size)
        b += to_bytes_object(item)
    return b


def to_class(to: object):
    b: bytes = bytes()
    for name, value in vars(to).items():
        if name.startswith('__'):
            continue
        if isinstance(value, (str, int, list, dict)):
            b += to_bytes_object(value)
    return b


def from_bytes_object(from_: bytes, to: Union[str, int, list, type]) -> (
object, int):
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
    from_ = from_[read:]
    bytes_array = from_[0: len_bytes]
    assert len_bytes == len(bytes_array)
    return bytes_array, read + len(bytes_array)


def from_string(from_: bytes, to: str) -> (str, int):
    assert isinstance(to, str)
    len_string, read = from_number(from_, int())
    from_ = from_[read:]
    string = from_[0: len_string].decode(ENCODING)
    assert len_string == len(string)
    return string, read + len(string)


def from_number(from_: bytes, to: int) -> (str, int):
    assert isinstance(to, int)
    return int.from_bytes(from_[0:INT_SIZE], BYTE_ORDER), INT_SIZE


def from_list(from_: bytes, to: Union[list, tuple]):
    list_array = []
    len_list, read = from_number(from_, int())
    pointer = read
    for i in range(len_list):
        len_list_item, read = from_number(from_[pointer:], int())
        pointer += read
        list_item, read = from_bytes_object(
            from_[pointer:pointer + len_list_item], to[0])
        pointer += read
        list_array.append(list_item)
    assert len_list == len(list_array)
    return list_array, pointer


def from_class(from_: bytes, to: object) -> (object, int):
    pointer = 0
    for name, value in vars(to).items():
        if name.startswith('__'):
            continue
        print(name, value, type(value))
        obj, read = from_bytes_object(from_[pointer:], value)
        setattr(to, name, obj)
        pointer += read
    return to, pointer
