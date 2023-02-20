from abc import ABCMeta

from flow_py_sdk.cadence import Kind
import flow_py_sdk.cadence.constants as c
from flow_py_sdk.cadence.decode import decode, add_cadence_kind_decoder


class OptionalKind(Kind):
    def __init__(self, value: Kind) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return f"{self.value}?"

    def encode_kind(self) -> dict:
        return {c.typeKey: self.value.encode()}

    @classmethod
    def kind_str(cls) -> str:
        return "Optional"

    @classmethod
    def decode(cls, value) -> "Kind":
        v = value[c.typeKey]
        return OptionalKind(decode(v))


class VariableSizedArrayKind(Kind):
    def __init__(self, value: Kind) -> None:
        super().__init__()
        self.value = value

    def __str__(self):
        return f"[{self.value}]"

    def encode_kind(self) -> dict:
        return {c.typeKey: self.value.encode()}

    @classmethod
    def kind_str(cls) -> str:
        return "VariableSizedArray"

    @classmethod
    def decode(cls, value) -> "Kind":
        v = value[c.typeKey]
        return VariableSizedArrayKind(decode(v))


class ConstantSizedArrayKind(Kind):
    def __init__(self, value: Kind, size: int) -> None:
        super().__init__()
        self.value = value
        self.size = size

    def __str__(self):
        return f"[{self.value};{self.size}]"

    def encode_kind(self) -> dict:
        return {
            c.typeKey: self.value.encode(),
            c.sizeKey: self.size,
        }

    @classmethod
    def kind_str(cls) -> str:
        return "ConstantSizedArray"

    @classmethod
    def decode(cls, value) -> "Kind":
        v = value[c.typeKey]
        size = value[c.sizeKey]
        return ConstantSizedArrayKind(decode(v), int(size))


class DictionaryKind(Kind):
    def __init__(self, key: Kind, value: Kind) -> None:
        super().__init__()
        self.key = key
        self.value = value

    def __str__(self):
        return f"{{{self.key};{self.value}}}"

    def encode_kind(self) -> dict:
        return {
            c.keyKey: self.key.encode(),
            c.valueKey: self.value.encode(),
        }

    @classmethod
    def kind_str(cls) -> str:
        return "Dictionary"

    @classmethod
    def decode(cls, value) -> "Kind":
        v = value[c.valueKey]
        key = value[c.keyKey]
        return DictionaryKind(decode(key), decode(v))


class ParameterKind:
    def __init__(self, label: str, id_: str, value: Kind) -> None:
        super().__init__()
        self.label = label
        self.id = id_
        self.value = value

    def encode(self):
        return {
            c.labelKey: self.label,
            c.idKey: self.id,
            c.typeKey: self.value.encode(),
        }

    @classmethod
    def decode(cls, value) -> "ParameterKind":
        label = str(value[c.labelKey])
        id_ = str(value[c.idKey])
        v = value[c.typeKey]

        return ParameterKind(label, id_, decode(v))

    def __str__(self):
        return f"{self.label} {self.id}: {self.value}"


class FieldKind:
    def __init__(self, id_: str, value: Kind) -> None:
        super().__init__()
        self.id = id_
        self.value = value

    def encode(self):
        return {
            c.idKey: self.id,
            c.typeKey: self.value.encode(),
        }

    @classmethod
    def decode(cls, value) -> "FieldKind":
        id_ = str(value[c.idKey])
        v = value[c.typeKey]

        return FieldKind(id_, decode(v))

    def __str__(self):
        return f"{self.id}: {self.value}"


class CompositeKind(Kind, metaclass=ABCMeta):
    def __init__(
        self,
        type_id: str,
        initializers: list[list[ParameterKind]],
        fields: list[FieldKind],
    ) -> None:
        super().__init__()
        self.type_id = type_id
        self.initializers = initializers
        self.fields = fields

    @classmethod
    def decode(cls, value) -> "Kind":
        type_id = str(value[c.typeIdKey])
        initializers = value[c.initializersKey]
        fields = value[c.fieldsKey]
        return cls(
            str(type_id),
            [[ParameterKind.decode(j) for j in i] for i in initializers],
            [FieldKind.decode(i) for i in fields],
        )

    def encode_kind(self) -> dict:
        return {
            c.typeKey: "",
            c.typeIdKey: self.type_id,
            c.initializersKey: [[i.encode() for i in j] for j in self.initializers],
            c.fieldsKey: [i.encode() for i in self.fields],
        }

    def __str__(self):
        return f"{self.type_id}({', '.join([str(i) for i in self.fields])})"


class StructKind(CompositeKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Struct"


class ResourceKind(CompositeKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Resource"


class EventKind(CompositeKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Event"


class ContractKind(CompositeKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Contract"


class StructInterfaceKind(CompositeKind):
    @classmethod
    def kind_str(cls) -> str:
        return "StructInterface"


class ResourceInterfaceKind(CompositeKind):
    @classmethod
    def kind_str(cls) -> str:
        return "ResourceInterface"


class ContractInterfaceKind(CompositeKind):
    @classmethod
    def kind_str(cls) -> str:
        return "ContractInterface"


class FunctionKind(Kind):
    def __init__(
        self, type_id: str, parameters: list[ParameterKind], return_: Kind
    ) -> None:
        super().__init__()
        self.type_id = type_id
        self.parameters = parameters
        self.return_ = return_

    @classmethod
    def decode(cls, value) -> "Kind":
        type_id = str(value[c.typeIdKey])
        parameters = value[c.parametersKey]
        return_ = value[c.returnKey]
        return FunctionKind(
            type_id,
            [ParameterKind.decode(i) for i in parameters],
            decode(return_),
        )

    def encode_kind(self) -> dict:
        return {
            c.typeIdKey: self.type_id,
            c.parametersKey: [i.encode() for i in self.parameters],
            c.returnKey: self.return_.encode(),
        }

    def __str__(self):
        return f"(({', '.join([str(p) for p in self.parameters])}): {self.return_})"

    @classmethod
    def kind_str(cls) -> str:
        return "Function"


class ReferenceKind(Kind):
    def __init__(self, authorized: bool, type_: Kind) -> None:
        super().__init__()
        self.authorized = authorized
        self.type = type_

    @classmethod
    def decode(cls, value) -> "Kind":
        authorized = bool(value[c.authorizedKey])
        type_ = value[c.typeKey]
        return ReferenceKind(
            authorized,
            decode(type_),
        )

    def encode_kind(self) -> dict:
        return {
            c.authorizedKey: self.authorized,
            c.typeKey: self.type.encode(),
        }

    def __str__(self):
        return f"&{'auth' if self.authorized else ''}{self.type}"

    @classmethod
    def kind_str(cls) -> str:
        return "Reference"


class RestrictedKind(Kind):
    def __init__(self, type_id: str, type_: Kind, restrictions: list[Kind]) -> None:
        super().__init__()
        self.type_id = type_id
        self.type = type_
        self.restrictions = restrictions

    @classmethod
    def decode(cls, value) -> "Kind":
        type_id = str(value[c.typeIdKey])
        type_ = value[c.typeKey]
        restrictions = value[c.restrictionsKey]
        return RestrictedKind(
            type_id,
            decode(type_),
            [decode(i) for i in restrictions],
        )

    def encode_kind(self) -> dict:
        return {
            c.typeIdKey: self.type_id,
            c.typeKey: self.type.encode(),
            c.restrictionsKey: [i.encode() for i in self.restrictions],
        }

    def __str__(self):
        return f"{self.type}{{{', '.join([str(r) for r in self.restrictions])}}}"

    @classmethod
    def kind_str(cls) -> str:
        return "Restriction"


class CapabilityKind(Kind):
    def __init__(self, type_: Kind) -> None:
        super().__init__()
        self.type = type_

    @classmethod
    def decode(cls, value) -> "Kind":
        type_ = value[c.typeKey]
        return CapabilityKind(
            decode(type_),
        )

    def encode_kind(self) -> dict:
        return {
            c.typeKey: self.type.encode(),
        }

    def __str__(self):
        return f"Capability<{self.type}>"

    @classmethod
    def kind_str(cls) -> str:
        return "Capability"


class EnumKind(Kind):
    def __init__(self, type_id: str, type_: Kind, fields: list[FieldKind]) -> None:
        super().__init__()
        self.type_id = type_id
        self.fields = fields
        self.type_ = type_

    @classmethod
    def decode(cls, value) -> "Kind":
        type_id = str(value[c.typeIdKey])
        type_ = value[c.typeKey]
        fields = value[c.fieldsKey]
        return cls(
            str(type_id),
            decode(type_),
            [FieldKind.decode(i) for i in fields],
        )

    def encode_kind(self) -> dict:
        return {
            c.typeKey: self.type_.encode(),
            c.typeIdKey: self.type_id,
            c.initializersKey: [],
            c.fieldsKey: [i.encode() for i in self.fields],
        }

    def __str__(self):
        return f"{self.type_id}({', '.join([str(i) for i in self.fields])})"

    @classmethod
    def kind_str(cls) -> str:
        return "Enum"


cadence_kinds = [
    OptionalKind,
    VariableSizedArrayKind,
    ConstantSizedArrayKind,
    DictionaryKind,
    StructKind,
    ResourceKind,
    EventKind,
    ContractKind,
    StructInterfaceKind,
    ResourceInterfaceKind,
    ContractInterfaceKind,
    FunctionKind,
    ReferenceKind,
    RestrictedKind,
    CapabilityKind,
    EnumKind,
]

for t in cadence_kinds:
    add_cadence_kind_decoder(t)
