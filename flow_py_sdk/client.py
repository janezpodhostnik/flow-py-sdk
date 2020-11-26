import asyncio
import json
import logging
from types import TracebackType
from typing import Optional, Type

from grpclib.client import Channel
from grpclib.config import Configuration
from grpclib.encoding.base import CodecBase, StatusDetailsCodecBase
from grpclib.metadata import Deadline

from .cadence.decode import cadence_object_hook
from .cadence.types import Value
from .proto.flow.access import AccessAPIStub, TransactionResultResponse
from .script import Script
from .tx import Tx

log = logging.getLogger(__name__)


class AccessAPI(AccessAPIStub):
    def __init__(self, channel: "Channel", *, timeout: Optional[float] = None, deadline: Optional["Deadline"] = None,
                 metadata=None) -> None:
        super().__init__(channel=channel, timeout=timeout, deadline=deadline, metadata=metadata)

    async def __aenter__(self) -> 'AccessAPI':
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        self.channel.close()

    async def execute_script(self, script: Script,
                             at_block_id: Optional[bytes] = None,
                             at_block_height: Optional[int] = None) -> Optional[Value]:
        if at_block_id is not None:
            log.debug(f'Executing script at block id {at_block_id.hex()}', script.code, script.arguments)
            result = await self.execute_script_at_block_i_d(script=script.code.encode("utf-8"),
                                                            arguments=script.encoded_arguments(),
                                                            block_id=at_block_id)
        elif at_block_height is not None:
            log.debug(f'Executing script at block height {at_block_height}', script.code, script.arguments)
            result = await self.execute_script_at_block_height(script=script.code.encode("utf-8"),
                                                               arguments=script.encoded_arguments(),
                                                               block_height=at_block_height)
        else:
            log.debug(f'Executing script at latest block', script.code, script.arguments)
            result = await self.execute_script_at_latest_block(script=script.code.encode("utf-8"),
                                                               arguments=script.encoded_arguments())

        if result is None or result.value is None:
            return None
        cadence_value = json.loads(result.value, object_hook=cadence_object_hook)
        return cadence_value

    async def execute_transaction(self, tx: Tx) -> TransactionResultResponse:
        log.debug(f'Executing transaction', tx.code, tx.arguments)
        result = await self.send_transaction(transaction=tx.to_grpc())

        return await self.get_transaction_result(id=result.id)


def flow_client(
        host: Optional[str] = None,
        port: Optional[int] = None,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        path: Optional[str] = None,
        codec: Optional[CodecBase] = None,
        status_details_codec: Optional[StatusDetailsCodecBase] = None,
        ssl=None,
        config: Optional[Configuration] = None,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None, metadata=None) -> AccessAPI:
    channel = Channel(host=host, port=port, loop=loop, path=path, codec=codec,
                      status_details_codec=status_details_codec, ssl=ssl, config=config)

    return AccessAPI(channel=channel, timeout=timeout, deadline=deadline, metadata=metadata)
