from __future__ import annotations

from abc import ABC
from typing import Tuple, Type as pyType

from flow_py_sdk.cadence.decode import decode, add_cadence_decoder
from flow_py_sdk.cadence.location import Location, decode_location
from flow_py_sdk.cadence.value import Value

import flow_py_sdk.cadence.constants as c


class CompositeType(ABC):
    def __init__(
        self,
        location: Location,
        qualified_identifier: str,
        fields: list[Field],
        initializer: list[list[Parameter]] = None,
    ):
        self.location: Location = location
        self.qualified_identifier: str = qualified_identifier
        self.fields: list[Field] = fields
        self.initializers: list[list[Parameter]] = initializer

    def id(self) -> str:
        return self.location.type_id(self.qualified_identifier)


class StructType(CompositeType):
    pass


class Struct(Value):
    def __init__(self, fields: list[Value], struct_type: StructType) -> None:
        super().__init__()
        self.struct_type: StructType = struct_type
        self.fields: list[Value] = fields

    def __str__(self):
        return Composite.format_composite(
            self.struct_type.id(),
            self.struct_type.fields,
            self.fields,
        )

    def encode_value(self) -> dict:
        return Composite.encode_composite(
            c.structTypeStr,
            self.struct_type.id(),
            self.struct_type.fields,
            self.fields,
        )

    @classmethod
    def decode(cls, value) -> Struct:
        composite = Composite.decode(value[c.valueKey])

        struct_type = StructType(
            composite.location,
            composite.qualified_identifier,
            composite.field_types,
        )

        return Struct(composite.field_values, struct_type)

    @classmethod
    def type_str(cls) -> str:
        return c.structTypeStr


class ResourceType(CompositeType):
    pass


class Resource(Value):
    def __init__(self, fields: list[Value], resource_type: ResourceType) -> None:
        super().__init__()
        self.resource_type: ResourceType = resource_type
        self.fields: list[Value] = fields

    def __str__(self):
        return Composite.format_composite(
            self.resource_type.id(),
            self.resource_type.fields,
            self.fields,
        )

    def encode_value(self) -> dict:
        return Composite.encode_composite(
            c.resourceTypeStr,
            self.resource_type.id(),
            self.resource_type.fields,
            self.fields,
        )

    @classmethod
    def decode(cls, value) -> Resource:
        composite = Composite.decode(value[c.valueKey])

        resource_type = ResourceType(
            composite.location,
            composite.qualified_identifier,
            composite.field_types,
        )

        return Resource(composite.field_values, resource_type)

    @classmethod
    def type_str(cls) -> str:
        return c.resourceTypeStr


class ContractType(CompositeType):
    pass


class Contract(Value):
    def __init__(self, fields: list[Value], resource_type: ContractType) -> None:
        super().__init__()
        self.resource_type: ContractType = resource_type
        self.fields: list[Value] = fields

    def __str__(self):
        return Composite.format_composite(
            self.resource_type.id(),
            self.resource_type.fields,
            self.fields,
        )

    def encode_value(self) -> dict:
        return Composite.encode_composite(
            c.contractTypeStr,
            self.resource_type.id(),
            self.resource_type.fields,
            self.fields,
        )

    @classmethod
    def decode(cls, value) -> Contract:
        composite = Composite.decode(value[c.valueKey])

        contract_type = ContractType(
            composite.location,
            composite.qualified_identifier,
            composite.field_types,
        )

        return Contract(composite.field_values, contract_type)

    @classmethod
    def type_str(cls) -> str:
        return c.contractTypeStr


class Field(object):
    def __init__(self, identifier: str, _type) -> None:
        super().__init__()
        self.identifier: str = identifier
        # not used anywhere yet! not typed
        self.type = _type


class Composite(object):
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
    def decode(cls, value) -> "Composite":
        type_id = value[c.idKey]
        location, qualified_identifier = decode_location(type_id)
        fields = value[c.fieldsKey]

        field_values = []
        field_types = []

        for field in fields:
            field_value, field_type = Composite._decode_composite_field(field)
            field_values.append(field_value)
            field_types.append(field_type)

        return Composite(location, qualified_identifier, field_values, field_types)

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


cadence_types: list[pyType[Value]] = [
    Struct,
    Resource,
    Contract,
]

for t in cadence_types:
    add_cadence_decoder(t)
