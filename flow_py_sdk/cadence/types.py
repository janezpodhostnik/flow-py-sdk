from abc import ABC, abstractmethod
from distutils.util import strtobool
from typing import List, Any, Callable, Optional as pyOptional

typeKey = "type"
_valueKey = "value"
_keyKey = "key"
_nameKey = "name"
_fieldsKey = "fields"
_idKey = "id"
_targetPathKey = "targetPath"
_borrowTypeKey = "borrowType"
_domainKey = "domain"
_identifierKey = "identifier"
_staticTypeKey = "staticType"
_addressKey = "address"
_pathKey = "path"

_voidTypeStr = "Void"
_optionalTypeStr = "Optional"
_boolTypeStr = "Bool"
_stringTypeStr = "String"
_addressTypeStr = "Address"
_intTypeStr = "Int"
_int8TypeStr = "Int8"
_int16TypeStr = "Int16"
_int32TypeStr = "Int32"
_int64TypeStr = "Int64"
_int128TypeStr = "Int128"
_int256TypeStr = "Int256"
_uintTypeStr = "UInt"
_uint8TypeStr = "UInt8"
_uint16TypeStr = "UInt16"
_uint32TypeStr = "UInt32"
_uint64TypeStr = "UInt64"
_uint128TypeStr = "UInt128"
_uint256TypeStr = "UInt256"
_word8TypeStr = "Word8"
_word16TypeStr = "Word16"
_word32TypeStr = "Word32"
_word64TypeStr = "Word64"
_fix64TypeStr = "Fix64"
_ufix64TypeStr = "UFix64"
_arrayTypeStr = "Array"
_dictionaryTypeStr = "Dictionary"
_structTypeStr = "Struct"
_resourceTypeStr = "Resource"
_eventTypeStr = "Event"
_contractTypeStr = "Contract"
_linkTypeStr = "Link"
_pathTypeStr = "Path"
_typeTypeStr = "Type"
_capabilityTypeStr = "Capability"

fix64_scale = int(8)
fix64_factor = int(100_000_000)


class Value(ABC):
    def __init__(self) -> None:
        super().__init__()

    def encode(self) -> dict:
        return {typeKey: self.type_str()} | self.encode_value()

    @abstractmethod
    def encode_value(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def decode(cls, value) -> "Value":
        pass

    @classmethod
    @abstractmethod
    def type_str(cls) -> str:
        pass

    def __eq__(self, other):
        if isinstance(other, Value):
            return str(self) == str(other)
        return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(str(self))


class Void(Value):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return f"Void"

    def encode_value(self) -> dict:
        return {}

    @classmethod
    def decode(cls, value) -> "Value":
        return Void()

    @classmethod
    def type_str(cls) -> str:
        return _voidTypeStr


class Optional(Value):
    def __init__(self, value: pyOptional[Value]) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Optional[{str(self.value)}]"

    def encode_value(self) -> dict:
        return {_valueKey: self.value.encode() if self.value is not None else None}

    @classmethod
    def decode(cls, value) -> "Value":
        if _valueKey not in value or value[_valueKey] is None:
            return Optional(None)
        return Optional(decode(value[_valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return _optionalTypeStr


class Bool(Value):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {_valueKey: self.value}

    @classmethod
    def decode(cls, value) -> "Value":
        return Bool(bool(strtobool(value[_valueKey])))

    @classmethod
    def type_str(cls) -> str:
        return _boolTypeStr


class String(Value):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

    def encode_value(self) -> dict:
        return {_valueKey: self.value}

    @classmethod
    def decode(cls, value) -> "Value":
        return String(str(value[_valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return _stringTypeStr


class Address(Value):
    address_length = 8
    address_prefix = "0x"

    def __init__(self, value: bytes) -> None:
        super().__init__()
        if len(value) > Address.address_length:
            raise Exception()  # TODO

        self.bytes = bytes(Address.address_length - len(value)) + value

    @classmethod
    def from_hex(cls, value: str) -> "Address":
        return Address(bytes.fromhex(value.removeprefix(Address.address_prefix)))

    def hex(self) -> str:
        return self.bytes.hex()

    def hex_with_prefix(self) -> str:
        return Address.address_prefix + self.bytes.hex()

    def __str__(self) -> str:
        return self.hex_with_prefix()

    def encode_value(self) -> dict:
        return {
            _valueKey: self.hex_with_prefix(),
        }

    @classmethod
    def decode(cls, value) -> "Value":
        addr = str(value[_valueKey])
        if addr[:2] != "0x":
            raise Exception()  # TODO
        return Address.from_hex(addr)

    @classmethod
    def type_str(cls) -> str:
        return _addressTypeStr


class Int(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {_valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> "Value":
        return Int(int(value[_valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return _intTypeStr


class Int8(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _int8TypeStr


class Int16(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _int16TypeStr


class Int32(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _int32TypeStr


class Int64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _int64TypeStr


class Int128(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _int128TypeStr


class Int256(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _int256TypeStr


class UInt(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _uintTypeStr


class UInt8(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _uint8TypeStr


class UInt16(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _uint16TypeStr


class UInt32(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _uint32TypeStr


class UInt64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _uint64TypeStr


class UInt128(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _uint128TypeStr


class UInt256(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _uint256TypeStr


class Word8(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _word8TypeStr


class Word16(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _word16TypeStr


class Word32(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _word32TypeStr


class Word64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _word64TypeStr


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


class Fix64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value: int = value

    def __str__(self):
        integer = int(self.value / fix64_factor)
        fraction = int(self.value % fix64_factor)
        return f"{integer}.{fraction:08d}"

    def encode_value(self) -> dict:
        return {_valueKey: str(self)}

    @classmethod
    def decode(cls, value) -> "Value":
        str_values = str(value[_valueKey]).split(".")
        return Fix64(int(str_values[0]) * fix64_factor + int(str_values[1]))

    @classmethod
    def type_str(cls) -> str:
        return _fix64TypeStr


class UFix64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value: int = value

    def __str__(self):
        integer = int(self.value / fix64_factor)
        fraction = int(self.value % fix64_factor)
        return f"{integer}.{fraction:08d}"

    def encode_value(self) -> dict:
        return {_valueKey: str(self)}

    @classmethod
    def decode(cls, value) -> "Value":
        str_values = str(value[_valueKey]).split(".")
        return Fix64(int(str_values[0]) * fix64_factor + int(str_values[1]))

    @classmethod
    def type_str(cls) -> str:
        return _ufix64TypeStr


class Array(Value):
    def __init__(self, value: List[Value]) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return f'[{",".join([str(item) for item in self.value])}]'

    def encode_value(self) -> dict:
        return {_valueKey: [i.encode() for i in self.value]}

    @classmethod
    def decode(cls, value) -> "Value":
        obj = value[_valueKey]
        return Array([decode(i) for i in obj])

    @classmethod
    def type_str(cls) -> str:
        return _arrayTypeStr


class KeyValuePair(object):
    def __init__(self, key: Value, value: Value) -> None:
        self.key = key
        self.value = value


class Dictionary(Value):
    def __init__(self, value: List[KeyValuePair] = None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return (
            f'{{{",".join([f"{{{item.key}:{item.value}}}" for item in self.value])}}}'
        )

    def encode_value(self) -> dict:
        return {
            _valueKey: [
                {
                    _keyKey: i.key.encode(),
                    _valueKey: i.value.encode(),
                }
                for i in self.value
            ]
            if self.value is not None
            else None
        }

    @classmethod
    def decode(cls, value) -> "Value":
        obj = value[_valueKey]
        items = [
            KeyValuePair(decode(item[_keyKey]), decode(item[_valueKey])) for item in obj
        ]
        return Dictionary(items)

    @classmethod
    def type_str(cls) -> str:
        return _dictionaryTypeStr


class Struct(Value):
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        raise NotImplementedError()

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _structTypeStr


class Resource(Value):
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        raise NotImplementedError()

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _resourceTypeStr


class Event(Value):
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        raise NotImplementedError()

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _eventTypeStr


class Contract(Value):
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        raise NotImplementedError()

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _contractTypeStr


class Link(Value):
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        raise NotImplementedError()

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _linkTypeStr


class Path(Value):
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        raise NotImplementedError()

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _pathTypeStr


class Type(Value):
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        raise NotImplementedError()

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _typeTypeStr


class Capability(Value):
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        raise NotImplementedError()

    def encode_value(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return _capabilityTypeStr


all_cadence_types: list = [
    Void,
    Optional,
    Bool,
    String,
    Address,
    Int,
    Int8,
    Int16,
    Int32,
    Int64,
    Int128,
    Int256,
    UInt,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UInt128,
    UInt256,
    Word8,
    Word16,
    Word32,
    Word64,
    Fix64,
    UFix64,
    Array,
    Dictionary,
    Struct,
    Resource,
    Event,
    Contract,
    Link,
    Path,
    Type,
    Capability,
]  # TODO try to constraint type to those that inherit Value

all_cadence_decoders: dict[str, Callable[[Any], Value]] = {
    t.type_str(): t.decode for t in all_cadence_types if issubclass(t, Value)
}


def decode(obj: [dict[Any, Any]]) -> Value:
    if isinstance(obj, Value):
        # json decoder starts from bottom up, so its possible that this is already decoded
        return obj

    type_ = obj[typeKey]
    if type_ in all_cadence_decoders:
        decoder = all_cadence_decoders[type_]
        return decoder(obj)

    raise NotImplementedError()
