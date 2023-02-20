from __future__ import annotations

from abc import ABCMeta

import flow_py_sdk.cadence.constants as c
from flow_py_sdk.cadence.decode import decode, add_cadence_decoder
from flow_py_sdk.cadence.value import Value


class Composite(Value, metaclass=ABCMeta):
    def __init__(self, id_: str, field_pairs: list[(str, Value)]):
        super().__init__()

        self.fields: dict[str, Value] = {f[0]: f[1] for f in field_pairs}
        self.field_order = [f[0] for f in field_pairs]
        self.id = id_

    @classmethod
    def decode(cls, value) -> "Composite":
        v = value[c.valueKey]
        field_pairs = [(f[c.nameKey], decode(f[c.valueKey])) for f in v[c.fieldsKey]]
        id_ = v[c.idKey]
        return cls(id_, field_pairs)

    def encode_value(self):
        return {
            c.valueKey: {
                c.idKey: self.id,
                c.fieldsKey: [
                    {c.nameKey: f, c.valueKey: self.fields[f].encode()}
                    for f in self.field_order
                ],
            }
        }

    def __str__(self):
        return f"{self.type_str()}({','.join([f'{k}:{v}' for k, v in self.fields.items()])})"

    def __setattr__(self, key, value):
        if key != "fields" and key in self.fields:
            self.fields[key] = value
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        if key != "fields" and key in self.fields:
            return self.fields[key]
        else:
            super(Value, self).__getattribute__(key)


class Struct(Composite):
    @classmethod
    def type_str(cls) -> str:
        return "Struct"


class Resource(Composite):
    @classmethod
    def type_str(cls) -> str:
        return "Resource"


class Event(Composite):
    @classmethod
    def type_str(cls) -> str:
        return "Event"


class Contract(Composite):
    @classmethod
    def type_str(cls) -> str:
        return "Contract"


class Enum(Composite):
    @classmethod
    def type_str(cls) -> str:
        return "Enum"


cadence_types = [
    Struct,
    Resource,
    Event,
    Contract,
    Enum,
]

for t in cadence_types:
    add_cadence_decoder(t)
