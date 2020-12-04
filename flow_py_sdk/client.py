import asyncio
import json
import logging
import time
from types import TracebackType
from typing import Optional, Type, Annotated

from grpclib.client import Channel
from grpclib.config import Configuration
from grpclib.encoding.base import CodecBase, StatusDetailsCodecBase
from grpclib.metadata import Deadline

from flow_py_sdk.cadence import Value, cadence_object_hook, encode_arguments
from flow_py_sdk.proto.flow.access import AccessAPIStub, TransactionResultResponse
from flow_py_sdk.script import Script
from flow_py_sdk.tx import Tx, TransactionStatus

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
        s = script.code.encode("utf-8")
        a = encode_arguments(script.arguments)

        if at_block_id is not None:
            log.debug(f'Executing script at block id {at_block_id.hex()}')
            result = await self.execute_script_at_block_i_d(script=s, arguments=a, block_id=at_block_id)
        elif at_block_height is not None:
            log.debug(f'Executing script at block height {at_block_height}')
            result = await self.execute_script_at_block_height(script=s, arguments=a, block_height=at_block_height)
        else:
            log.debug(f'Executing script at latest block', )
            result = await self.execute_script_at_latest_block(script=s, arguments=a)

        log.debug(f'Script Executed')

        if result is None or result.value is None:
            return None
        cadence_value = json.loads(result.value, object_hook=cadence_object_hook)
        return cadence_value

    async def execute_transaction(self, tx: Tx, *, wait_for_seal=True,
                                  timeout: Annotated[float, 'seconds'] = 30.0) -> TransactionResultResponse:
        log.debug(f'Sending transaction')
        result = await self.send_transaction(transaction=tx.to_grpc())
        log.info(f'Sent transaction {result.id.hex()}')
        tx_result = await self.get_transaction_result(id=result.id)
        if tx_result.error_message:
            raise Exception(tx_result.error_message)  # TODO wrap error

        if not wait_for_seal:
            return tx_result

        log.info(f'Waiting for transaction to seal')

        end_time = time.monotonic() + timeout
        while TransactionStatus(tx_result.status) is not TransactionStatus.TransactionStatusSealed \
                and time.monotonic() < end_time:
            await asyncio.sleep(1)
            tx_result = await self.get_transaction_result(id=result.id)

        if TransactionStatus(tx_result.status) is not TransactionStatus.TransactionStatusSealed:
            raise TimeoutError(f"Waiting for transaction {result.id.hex()} to seal")

        if tx_result.error_message:
            raise Exception(tx_result.error_message)  # TODO wrap error

        log.info(f'Got transaction seal')
        return tx_result


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
