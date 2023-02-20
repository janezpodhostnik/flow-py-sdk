from __future__ import annotations

from abc import ABCMeta

import flow_py_sdk.cadence.constants as c
from flow_py_sdk.cadence.decode import add_cadence_kind_decoder
from flow_py_sdk.cadence.kind import Kind


class SimpleKind(Kind, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()

    def encode_kind(self) -> dict:
        return {}

    def __str__(self):
        return self.kind_str()

    @classmethod
    def decode(cls, value) -> "Kind":
        v = value[c.kindKey]
        return cls()


class AnyKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Any"


class AnyStructKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "AnyStruct"


class AnyResourceKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "AnyResource"


class TypeKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Type"


class VoidKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Void"


class NeverKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Never"


class BoolKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Bool"


class StringKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "String"


class CharacterKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Character"


class BytesKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Bytes"


class AddressKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Address"


class NumberKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Number"


class SignedNumberKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "SignedNumber"


class IntegerKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Integer"


class SignedIntegerKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "SignedInteger"


class FixedPointKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "FixedPoint"


class SignedFixedPointKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "SignedFixedPoint"


class IntKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Int"


class Int8Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Int8"


class Int16Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Int16"


class Int32Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Int32"


class Int64Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Int64"


class Int128Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Int128"


class Int256Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Int256"


class UIntKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "UInt"


class UInt8Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "UInt8"


class UInt16Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "UInt16"


class UInt32Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "UInt32"


class UInt64Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "UInt64"


class UInt128Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "UInt128"


class UInt256Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "UInt256"


class Word8Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Word8"


class Word16Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Word16"


class Word32Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Word32"


class Word64Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Word64"


class Fix64Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Fix64"


class UFix64Kind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "UFix64"


class PathKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Path"


class CapabilityPathKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "CapabilityPath"


class StoragePathKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "StoragePath"


class PublicPathKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "PublicPath"


class PrivatePathKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "PrivatePath"


class AuthAccountKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "AuthAccount"


class PublicAccountKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "PublicAccount"


class AuthAccountKeysKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "AuthAccount.Keys"


class PublicAccountKeysKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "PublicAccount.Keys"


class AuthAccountContractsKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "AuthAccount.Contracts"


class PublicAccountContractsKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "PublicAccount.Contracts"


class DeployedContractKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "DeployedContract"


class AccountKeyKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "AccountKey"


class BlockKind(SimpleKind):
    @classmethod
    def kind_str(cls) -> str:
        return "Block"


cadence_kinds = [
    AnyKind,
    AnyStructKind,
    AnyResourceKind,
    TypeKind,
    VoidKind,
    NeverKind,
    BoolKind,
    StringKind,
    CharacterKind,
    BytesKind,
    AddressKind,
    NumberKind,
    SignedNumberKind,
    IntegerKind,
    SignedIntegerKind,
    FixedPointKind,
    SignedFixedPointKind,
    IntKind,
    Int8Kind,
    Int16Kind,
    Int32Kind,
    Int64Kind,
    Int128Kind,
    Int256Kind,
    UIntKind,
    UInt8Kind,
    UInt16Kind,
    UInt32Kind,
    UInt64Kind,
    UInt128Kind,
    UInt256Kind,
    Word8Kind,
    Word16Kind,
    Word32Kind,
    Word64Kind,
    Fix64Kind,
    UFix64Kind,
    PathKind,
    CapabilityPathKind,
    StoragePathKind,
    PublicPathKind,
    PrivatePathKind,
    AuthAccountKind,
    PublicAccountKind,
    AuthAccountKeysKind,
    PublicAccountKeysKind,
    AuthAccountContractsKind,
    PublicAccountContractsKind,
    DeployedContractKind,
    AccountKeyKind,
    BlockKind,
]

for t in cadence_kinds:
    add_cadence_kind_decoder(t)
