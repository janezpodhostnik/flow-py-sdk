from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional

import flow_py_sdk.cadence.constants as c
from flow_py_sdk.exceptions import CadenceIncorrectTypeError


class Value(ABC, object):
    def __init__(self) -> None:
        super().__init__()

    def encode(self) -> dict:
        return {c.typeKey: self.type_str()} | self.encode_value()

    def as_type(self, t: Type[TValue]) -> Optional[TValue]:
        if isinstance(self, t):
            return self
        raise CadenceIncorrectTypeError(f"Value {self} is not of type {t}")

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


TValue = TypeVar("TValue", bound=Value)
