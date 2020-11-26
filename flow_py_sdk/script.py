import json
import logging
from typing import Optional

from flow_py_sdk.cadence.decode import cadence_object_hook
from flow_py_sdk.cadence.encode import CadenceJsonEncoder
from flow_py_sdk.cadence.types import Value
from flow_py_sdk.proto.flow.access import AccessAPIStub

log = logging.getLogger(__name__)


class Script(object):
    def __init__(self) -> None:
        super().__init__()
        self.code: Optional[str] = None
        self.arguments: list[Value] = []

    def with_cadence_code(self, code: str) -> 'Script':
        self.code = code
        return self

    def add_arguments(self, *args: Value) -> 'Script':
        self.arguments.extend(args)
        return self

    def _encoded_arguments(self) -> list[bytes]:
        return [json.dumps(a, ensure_ascii=False, cls=CadenceJsonEncoder).encode('utf-8') for a in self.arguments]

    async def execute(self, *,
                      client: AccessAPIStub,
                      at_block_id: Optional[bytes] = None,
                      at_block_height: Optional[int] = None) -> Optional[Value]:
        if at_block_id is not None:
            logging.debug(f'Executing script at block id {at_block_id.hex()}', self.code, self.arguments)
            result = await client.execute_script_at_block_i_d(script=self.code.encode("utf-8"),
                                                              arguments=self._encoded_arguments(),
                                                              block_id=at_block_id)
        elif at_block_height is not None:
            logging.debug(f'Executing script at block height {at_block_height}', self.code, self.arguments)
            result = await client.execute_script_at_block_height(script=self.code.encode("utf-8"),
                                                                 arguments=self._encoded_arguments(),
                                                                 block_height=at_block_height)
        else:
            logging.debug(f'Executing script at latest block', self.code, self.arguments)
            result = await client.execute_script_at_latest_block(script=self.code.encode("utf-8"),
                                                                 arguments=self._encoded_arguments())

        if result is None or result.value is None:
            return None
        cadence_value = json.loads(result.value, object_hook=cadence_object_hook)
        return cadence_value
