from typing import Any

from flow_py_sdk.cadence.types import decode


def cadence_object_hook(obj: [dict[Any, Any]]) -> Any:
    return decode(obj)
