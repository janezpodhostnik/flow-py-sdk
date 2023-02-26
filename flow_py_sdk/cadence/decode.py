from typing import Any, Callable, Type, Union

from flow_py_sdk.cadence.value import Value
from flow_py_sdk.cadence.kind import Kind

import flow_py_sdk.cadence.constants as c

_cadence_decoders: dict[str, Callable[[Any], Value]] = {}
_cadence_kind_decoders: dict[str, Callable[[Any], Kind]] = {}


def add_cadence_decoder(t: Type[Value]):
    _cadence_decoders[t.type_str()] = t.decode


def add_cadence_kind_decoder(t: Type[Kind]):
    _cadence_kind_decoders[t.kind_str()] = t.decode


def decode(obj: [dict[Any, Any]]) -> Union[Value, Kind]:
    # json decoder starts from bottom up, so it's possible that this is already decoded
    if isinstance(obj, Value) or isinstance(obj, Kind):
        return obj

    # if there is an id key, it's already decoded and it is either a field or a parameter
    if c.idKey in obj:
        return obj

    # if there is no type key we cant decode it directly, but it could be part of a dictionary or composite or path
    if c.kindKey not in obj and c.typeKey not in obj:
        return obj

    if c.kindKey in obj:
        kind = obj[c.kindKey]
        if kind in _cadence_kind_decoders:
            decoder = _cadence_kind_decoders[kind]
            return decoder(obj)

    if c.typeKey in obj:
        type_ = obj[c.typeKey]
        if type_ in _cadence_decoders:
            decoder = _cadence_decoders[type_]
            return decoder(obj)

    raise NotImplementedError()


def cadence_object_hook(obj: [dict[Any, Any]]) -> Any:
    return decode(obj)
