from typing import Any, Callable, Type, Union

from flow_py_sdk.cadence.value import Value
from flow_py_sdk.cadence.kind import Kind
import logging
import flow_py_sdk.cadence.constants as c

_cadence_decoders: dict[str, Callable[[Any], Value]] = {}
_cadence_kind_decoders: dict[str, Callable[[Any], Kind]] = {}


def add_cadence_decoder(t: Type[Value]):
    _cadence_decoders[t.type_str()] = t.decode


def add_cadence_kind_decoder(t: Type[Kind]):
    _cadence_kind_decoders[t.kind_str()] = t.decode


def decode(obj: dict[Any, Any]) -> Union[Value, Kind, dict]:
    try:
        # Check if already decoded
        if isinstance(obj, Value) or isinstance(obj, Kind):
            return obj

        # If obj has an idKey, treat as already decoded field or parameter
        if c.idKey in obj:
            return obj

        # Check for kindKey or typeKey to determine appropriate decoder
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

        return obj  # Return the object if no decoder applies

    except KeyError as e:
        logging.error(
            f"Unhandled key '{e}' during decode of {type(obj).__name__}. "
            + f"Value: {obj}"
        )
        raise

    except NotImplementedError:
        logging.error(
            f"Decoding not implemented for type {type(obj).__name__}. "
            + f"Value: {obj}"
        )
        raise


def cadence_object_hook(obj: [dict[Any, Any]]) -> Any:
    return decode(obj)
