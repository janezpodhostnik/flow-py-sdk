from __future__ import annotations
import logging

from flow_py_sdk.cadence.types import Value
from flow_py_sdk.exceptions import NotCadenceValueError

log = logging.getLogger(__name__)


class Script(object):
    """The Script object used for sending scripts to the Flow blockchain

    This is mainly just a wrapper around a script code and the code arguments.

    Attributes
    ----------
    code : str
        The code of the script.

    arguments : list[Value]
        arguments will be passed to the script when it is being executed. The order of the arguments is important.
        Arguments are verified to be cadence.Value(s).
    """

    def __init__(self, *, code: str, arguments: list[Value] = None) -> None:
        super().__init__()
        self.code: str = code
        self.arguments: list[Value] = []
        if arguments:
            self.add_arguments(*arguments)

    def add_arguments(self, *args: Value) -> Script:
        for arg in args:
            if not isinstance(arg, Value):
                raise NotCadenceValueError.from_value(arg)
        self.arguments.extend(args)
        return self
