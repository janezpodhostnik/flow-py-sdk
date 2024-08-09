from __future__ import annotations

from distutils.util import strtobool
from typing import (
    List,
    Optional as pyOptional,
    Type as pyType,
)

import flow_py_sdk.cadence.constants as c
from flow_py_sdk.cadence.kind import Kind
from flow_py_sdk.cadence.address import Address
from flow_py_sdk.cadence.decode import decode, add_cadence_decoder
from flow_py_sdk.cadence.value import Value


class Void(Value):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return f"Void"

    def encode_value(self) -> dict:
        return {}

    @classmethod
    def decode(cls, value) -> Void:
        return Void()

    @classmethod
    def type_str(cls) -> str:
        return c.voidTypeStr


class Optional(Value):
    def __init__(self, value: pyOptional[Value]) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Optional[{str(self.value)}]"

    def encode_value(self) -> dict:
        return {c.valueKey: self.value.encode() if self.value is not None else None}

    @classmethod
    def decode(cls, value) -> Optional:
        if c.valueKey not in value or value[c.valueKey] is None:
            return Optional(None)
        return Optional(decode(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.optionalTypeStr


class Bool(Value):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: self.value}

    @classmethod
    def decode(cls, value) -> Bool:
        if isinstance(value[c.valueKey], bool):
            return Bool(value[c.valueKey])
        return Bool(bool(strtobool(value[c.valueKey])))

    @classmethod
    def type_str(cls) -> str:
        return c.boolTypeStr


class String(Value):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

    def encode_value(self) -> dict:
        return {c.valueKey: self.value}

    @classmethod
    def decode(cls, value) -> String:
        return String(str(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.stringTypeStr


class Int(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Int:
        return Int(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.intTypeStr


class Int8(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Int8:
        return Int8(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.int8TypeStr


class Int16(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Int16:
        return Int16(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.int16TypeStr


class Int32(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Int32:
        return Int32(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.int32TypeStr


class Int64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Int64:
        return Int64(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.int64TypeStr


class Int128(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Int128:
        return Int128(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.int128TypeStr


class Int256(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Int256:
        return Int256(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.int256TypeStr


class UInt(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> UInt:
        return UInt(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.uintTypeStr


class UInt8(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> UInt8:
        return UInt8(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.uint8TypeStr


class UInt16(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> UInt16:
        return UInt16(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.uint16TypeStr


class UInt32(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> UInt32:
        return UInt32(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.uint32TypeStr


class UInt64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> UInt64:
        return UInt64(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.uint64TypeStr


class UInt128(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> UInt128:
        return UInt128(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.uint128TypeStr


class UInt256(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> UInt256:
        return UInt256(int(value[c.valueKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.uint256TypeStr


class Word8(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Word8:
        return Word8(value[c.valueKey])

    @classmethod
    def type_str(cls) -> str:
        return c.word8TypeStr


class Word16(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Word16:
        return Word16(value[c.valueKey])

    @classmethod
    def type_str(cls) -> str:
        return c.word16TypeStr


class Word32(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Word32:
        return Word32(value[c.valueKey])

    @classmethod
    def type_str(cls) -> str:
        return c.word32TypeStr


class Word64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def encode_value(self) -> dict:
        return {c.valueKey: str(self.value)}

    @classmethod
    def decode(cls, value) -> Word64:
        return Word64(value[c.valueKey])

    @classmethod
    def type_str(cls) -> str:
        return c.word64TypeStr


class Fix64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value: int = value

    def __str__(self):
        integer = int(self.value / c.fix64_factor)
        fraction = int(abs(self.value) % c.fix64_factor)
        return f"{integer}.{fraction:08d}"

    def encode_value(self) -> dict:
        return {c.valueKey: str(self)}

    @classmethod
    def decode(cls, value) -> Fix64:
        str_values = str(value[c.valueKey]).split(".")
        sign: int = -1 if int(str_values[0]) < 0 else 1
        return Fix64(
            sign * (abs(int(str_values[0])) * c.fix64_factor + int(str_values[1]))
        )

    @classmethod
    def type_str(cls) -> str:
        return c.fix64TypeStr


class UFix64(Value):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value: int = value

    def __str__(self):
        integer = int(self.value / c.fix64_factor)
        fraction = int(self.value % c.fix64_factor)
        return f"{integer}.{fraction:08d}"

    def encode_value(self) -> dict:
        return {c.valueKey: str(self)}

    @classmethod
    def decode(cls, value) -> UFix64:
        str_values = str(value[c.valueKey]).split(".")
        return UFix64(int(str_values[0]) * c.fix64_factor + int(str_values[1]))

    @classmethod
    def type_str(cls) -> str:
        return c.ufix64TypeStr


class Array(Value):
    def __init__(self, value: List[Value]) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return f'[{",".join([str(item) for item in self.value])}]'

    def encode_value(self) -> dict:
        return {c.valueKey: [i.encode() for i in self.value]}

    @classmethod
    def decode(cls, value) -> Array:
        obj = value[c.valueKey]
        return Array([decode(i) for i in obj])

    @classmethod
    def type_str(cls) -> str:
        return c.arrayTypeStr


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
            c.valueKey: (
                [
                    {
                        c.keyKey: i.key.encode(),
                        c.valueKey: i.value.encode(),
                    }
                    for i in self.value
                ]
                if self.value is not None
                else None
            )
        }

    @classmethod
    def decode(cls, value) -> Dictionary:
        obj = value[c.valueKey]
        items = [
            KeyValuePair(decode(item[c.keyKey]), decode(item[c.valueKey]))
            for item in obj
        ]
        return Dictionary(items)

    @classmethod
    def type_str(cls) -> str:
        return c.dictionaryTypeStr


class Path(Value):
    def __init__(self, domain: str, identifier: str) -> None:
        super().__init__()
        self.domain: str = domain
        self.identifier: str = identifier

    def __str__(self):
        return f"/{self.domain}/{self.identifier}"

    def encode_value(self) -> dict:
        return {
            c.valueKey: {c.domainKey: self.domain, c.identifierKey: self.identifier}
        }

    @classmethod
    def decode(cls, value) -> Path:
        v = value[c.valueKey]
        return Path(
            v[c.domainKey],
            v[c.identifierKey],
        )

    @classmethod
    def type_str(cls) -> str:
        return c.pathTypeStr


class TypeValue(Value):
    def __init__(self, type_: Kind = None) -> None:
        super().__init__()
        self.type_ = type_

    def __str__(self):
        return f"Type<{str(self.type_) if self.type_ else ''}>()"

    def encode_value(self) -> dict:
        return {
            c.valueKey: {
                c.staticTypeKey: self.type_.encode() if self.type_ else "",
            }
        }

    @classmethod
    def decode(cls, value) -> TypeValue:
        v = value[c.valueKey]
        return TypeValue(
            decode(v[c.staticTypeKey]) if v[c.staticTypeKey] else None,
        )

    @classmethod
    def type_str(cls) -> str:
        return c.typeTypeStr


class InclusiveRange(Value):
    def __init__(self, start: Value, end: Value, step: Value) -> None:
        super().__init__()
        self.start = start
        self.end = end
        self.step = step

    def __str__(self):
        fields = {}

        if self.start is not None:
            fields["start"] = self.start
        if self.end is not None:
            fields["end"] = self.end
        if self.step is not None:
            fields["step"] = self.step

        return f"{self.type_str()}({','.join([f'{k}:{v}' for k, v in fields.items()])})"

    def encode_value(self) -> dict:
        return {
            c.valueKey: {
                c.startKey: self.start.encode(),
                c.endKey: self.end.encode(),
                c.stepKey: self.step.encode(),
            }
        }

    @classmethod
    def decode(cls, value) -> InclusiveRange:
        v = value[c.valueKey]
        return InclusiveRange(
            decode(v[c.startKey]),
            decode(v[c.endKey]),
            decode(v[c.stepKey]),
        )

    @classmethod
    def type_str(cls) -> str:
        return c.inclusiveRangeTypeStr


class Capability(Value):
    def __init__(self, id_: int, address: Address, borrow_type: Kind) -> None:
        super().__init__()
        self.id_ = id_
        self.address = address
        self.borrow_type = borrow_type

    def __str__(self):
        type_arg = "" if self.borrow_type is None else f"<{self.borrow_type}>"
        return f"Capability{type_arg}(address: {self.address}, id: {self.id_})"

    def encode_value(self) -> dict:
        return {
            c.valueKey: {
                c.idKey: self.id_,
                c.addressKey: self.address.encode_value()[c.valueKey],
                c.borrowTypeKey: self.borrow_type.encode(),
            }
        }

    @classmethod
    def decode(cls, value) -> Capability:
        v = value[c.valueKey]
        id_ = v[c.idKey]
        address = Address.decode({c.valueKey: v[c.addressKey]})
        return Capability(id_, address, decode(v[c.borrowTypeKey]))

    @classmethod
    def type_str(cls) -> str:
        return c.capabilityTypeStr


class Function(Value):
    def __init__(self, function_type: Kind) -> None:
        super().__init__()
        self.function_type = function_type

    def __str__(self):
        return f"Function{self.function_type}"

    def encode_value(self) -> dict:
        return {
            c.valueKey: {
                c.functionTypeKey: self.function_type.encode(),
            }
        }

    @classmethod
    def decode(cls, value) -> Function:
        v = value[c.valueKey]
        type_ = v[c.functionTypeKey]
        return Function(decode(type_))

    @classmethod
    def type_str(cls) -> str:
        return c.functionTypeStr


cadence_types: list[pyType[Value]] = [
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
    TypeValue,
    InclusiveRange,
    Path,
    Capability,
    Function,
]

for t in cadence_types:
    add_cadence_decoder(t)
