import logging
from typing import Optional

from flow_py_sdk.cadence.types import Value
from flow_py_sdk.exceptions import NotCadenceValueError

log = logging.getLogger(__name__)


class Script(object):
    def __init__(self, *, code: str, arguments: list[Value] = None) -> None:
        super().__init__()
        self.code: Optional[str] = code
        self.arguments: list[Value] = arguments if arguments else []

    def add_arguments(self, *args: Value) -> "Script":
        for arg in args:
            if not isinstance(arg, Value):
                raise NotCadenceValueError.from_value(arg)
        self.arguments.extend(args)
        return self
