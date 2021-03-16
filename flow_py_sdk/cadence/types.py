from __future__ import annotations
from distutils.util import strtobool
from typing import (
    List,
    Any,
    Callable,
    Optional as pyOptional,
    Tuple,
    Annotated,
    TypeVar,
)

import flow_py_sdk.cadence.constants as c
from flow_py_sdk.cadence.address import Address
from flow_py_sdk.cadence.location import decode_location, Location
from flow_py_sdk.cadence.value import Value
from flow_py_sdk.exceptions import CadenceEncodingError


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
    def decode(cls, value) -> "Value":
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
    def decode(cls, value) -> "Value":
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
    def decode(cls, value) -> "Value":
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
    def decode(cls, value) -> "Value":
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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
    def decode(cls, value) -> "Value":
        return Int(int(value[c.valueKey]))

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
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

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
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

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
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

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
        raise NotImplementedError()

    @classmethod
    def decode(cls, value) -> "Value":
        raise NotImplementedError()

    @classmethod
    def type_str(cls) -> str:
        return c.word64TypeStr


class Fix64(Value):
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
    def decode(cls, value) -> "Value":
        str_values = str(value[c.valueKey]).split(".")
        return Fix64(int(str_values[0]) * c.fix64_factor + int(str_values[1]))

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
    def decode(cls, value) -> "Value":
        str_values = str(value[c.valueKey]).split(".")
        return Fix64(int(str_values[0]) * c.fix64_factor + int(str_values[1]))

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
    def decode(cls, value) -> "Value":
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
            c.valueKey: [
                {
                    c.keyKey: i.key.encode(),
                    c.valueKey: i.value.encode(),
                }
                for i in self.value
            ]
            if self.value is not None
            else None
        }

    @classmethod
    def decode(cls, value) -> "Value":
        obj = value[c.valueKey]
        items = [
            KeyValuePair(decode(item[c.keyKey]), decode(item[c.valueKey]))
            for item in obj
        ]
        return Dictionary(items)

    @classmethod
    def type_str(cls) -> str:
        return c.dictionaryTypeStr


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
        return c.structTypeStr


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
        return c.resourceTypeStr


class Field(object):
    def __init__(self, identifier: str, _type: type) -> None:
        super().__init__()
        self.identifier: str = identifier
        self.type: type = _type


class _Composite(object):
    def __init__(
        self,
        location: Location,
        qualified_identifier: str,
        field_values: list[Value],
        field_types: list[Field],
    ) -> None:
        super().__init__()
        self.location: Location = location
        self.qualified_identifier: str = qualified_identifier
        self.field_values: list[Value] = field_values
        self.field_types: list[Field] = field_types

    @classmethod
    def encode_composite(
        cls, kind: str, _id: str, fields: list[Field], values: list[Value]
    ) -> dict:
        return {
            c.typeKey: kind,
            c.valueKey: {
                c.idKey: _id,
                c.fieldsKey: [
                    {c.nameKey: f.identifier, c.valueKey: v.encode()}
                    for f, v in zip(fields, values)
                ],
            },
        }

    @classmethod
    def decode(cls, value) -> "_Composite":
        type_id = value[c.idKey]
        location, qualified_identifier = decode_location(type_id)
        fields = value[c.fieldsKey]

        field_values = []
        field_types = []

        for field in fields:
            field_value, field_type = _Composite._decode_composite_field(field)
            field_values.append(field_value)
            field_types.append(field_type)

        return _Composite(location, qualified_identifier, field_values, field_types)

    @classmethod
    def _decode_composite_field(cls, value) -> Tuple[Value, Field]:
        name = value[c.nameKey]
        field_value = decode(value[c.valueKey])

        field = Field(name, type(field_value))

        return field_value, field

    @classmethod
    def format_composite(
        cls, type_id: str, fields: list[Field], values: list[Value]
    ) -> str:
        prepared_fields: list[Tuple[str, str]] = []
        for v, f in zip(values, fields):
            prepared_fields.append((f.identifier, str(v)))

        return f"{type_id}({str.join(', ', [f'{n}: {v}' for n, v in prepared_fields])})"

    @classmethod
    def type_str(cls) -> str:
        return c.eventTypeStr


class Type(object):
    pass


class Parameter(object):
    def __init__(self) -> None:
        super().__init__()
        self.label: str
        self.identifier: str
        self.type: Type


class EventType(object):
    def __init__(
        self,
        location: Location,
        qualified_identifier: str,
        fields: list[Field],
        initializer: list[Parameter] = None,
    ) -> None:
        super().__init__()
        self.location: Location = location
        self.qualified_identifier: str = qualified_identifier
        self.fields: list[Field] = fields
        self.initializer: list[Parameter] = [] if initializer is None else initializer

    def id(self) -> str:
        return self.location.type_id(self.qualified_identifier)


class Event(Value):
    _event_types: dict = {}  # TODO find out how to type this correctly

    def __init__(self, fields: list[Value], event_type: EventType) -> None:
        super().__init__()
        self.event_type: EventType = event_type
        self.fields: list[Value] = fields

    def __str__(self):
        return _Composite.format_composite(
            self.event_type.id(),
            self.event_type.fields,
            self.fields,
        )

    def encode_value(self) -> dict:
        return _Composite.encode_composite(
            c.eventTypeStr,
            self.event_type.id(),
            self.event_type.fields,
            self.fields,
        )

    @classmethod
    def decode(cls, value) -> "Value":
        composite = _Composite.decode(value[c.valueKey])

        event = Event(
            composite.field_values,
            EventType(
                composite.location,
                composite.qualified_identifier,
                composite.field_types,
            ),
        )

        if event.event_type.id() in event._event_types:
            return event._event_types[event.event_type.id()].from_event(event)
        return event

    @classmethod
    def type_str(cls) -> str:
        return c.eventTypeStr

    @classmethod
    def from_event(cls, event: "Event") -> "Event":
        return Event(
            event.fields,
            event.event_type,
        )

    @classmethod
    def add_event_type(cls, event_type):  # TODO find out how to type this correctly
        Event._event_types[event_type.event_id_constraint()] = event_type

    @classmethod
    def event_id_constraint(cls) -> str:
        return ""


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
        return c.contractTypeStr


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
        return c.linkTypeStr


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
        return c.pathTypeStr


class TypeValue(Value):
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
        return c.typeTypeStr


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
        return c.capabilityTypeStr


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
    # json decoder starts from bottom up, so its possible that this is already decoded or is part of a composite
    if isinstance(obj, Value):
        return obj
    if c.valueKey in obj and isinstance(obj[c.valueKey], Value):
        return obj
    if c.fieldsKey in obj:
        return obj

    type_ = obj[c.typeKey]
    if type_ in all_cadence_decoders:
        decoder = all_cadence_decoders[type_]
        return decoder(obj)

    raise NotImplementedError()
