from typing import Any, Callable, Type

from flow_py_sdk.cadence.value import Value

import flow_py_sdk.cadence.constants as c


_cadence_decoders: dict[str, Callable[[Any], Value]] = {}


def add_cadence_decoder(t: Type[Value]):
    _cadence_decoders[t.type_str()] = t.decode


def decode(obj: [dict[Any, Any]]) -> Value:
    # json decoder starts from bottom up, so its possible that this is already decoded or is part of a composite
    if isinstance(obj, Value):
        return obj
    if c.valueKey in obj and isinstance(obj[c.valueKey], Value):
        return obj
    if c.fieldsKey in obj:
        return obj

    type_ = obj[c.typeKey]
    if type_ in _cadence_decoders:
        decoder = _cadence_decoders[type_]
        return decoder(obj)

    raise NotImplementedError()


def cadence_object_hook(obj: [dict[Any, Any]]) -> Any:
    return decode(obj)
