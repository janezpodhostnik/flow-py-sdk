from typing import List


class Void(object):
    pass


class Optional(object):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value


class Bool(object):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value


class String(object):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class Address(object):
    def __init__(self, value: bytes) -> None:
        super().__init__()
        self.value = value


class Int(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Int8(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Int16(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Int32(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Int64(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Int128(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Int256(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class UInt(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class UInt8(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class UInt16(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class UInt32(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class UInt64(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class UInt128(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class UInt256(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Word8(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Word16(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Word32(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Word64(object):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


# def _parse_fixed_point(value: str):
#     parts = value.split('.')
#     if len(parts) != 2:
#         raise Exception()  # TODO
#
#     integerStr = parts[0]
#     fractionalStr = parts[1]
#
#     scale = len(fractionalStr)
#
#     if fractionalStr[0] != '+' and fractionalStr[0] !=  '-':
#         raise Exception()  # TODO
#
#     negative = False


class Fix64(object):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    @classmethod
    def parse_string(cls, value: str):
        return Fix64(float(value))  # TODO


class UFix64(object):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    @classmethod
    def parse_string(cls, value: str):
        return Fix64(float(value))  # TODO


class Array(object):
    def __init__(self, value: List) -> None:
        super().__init__()
        self.value = value


class KeyValuePair(object):
    def __init__(self, key, value) -> None:
        super().__init__()
        self.key = key
        self.value = value


class Dictionary(object):
    def __init__(self, value: List[KeyValuePair]) -> None:
        super().__init__()
        self.value = value
