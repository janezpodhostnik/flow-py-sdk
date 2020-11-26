import json
from typing import Optional, List

from flow_py_sdk.cadence.encode import CadenceJsonEncoder
from flow_py_sdk.cadence.types import Value


class Tx(object):
    def __init__(self) -> None:
        super().__init__()
        self.script: Optional[str] = None
        self.arguments: List[bytes] = []

    def with_script(self, script: str) -> 'Tx':
        self.script = script
        return self

    def add_arguments(self, *args: Value):
        self.arguments.extend((json.dumps(v, ensure_ascii=False, cls=CadenceJsonEncoder).encode('utf-8') for v in args))
