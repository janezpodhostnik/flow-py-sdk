import asyncio
import json
import logging
from types import TracebackType
from typing import Optional, Type, Annotated, List

import time
from grpclib.client import Channel
from grpclib.config import Configuration
from grpclib.encoding.base import CodecBase, StatusDetailsCodecBase
from grpclib.metadata import Deadline

from flow_py_sdk.cadence import Value, cadence_object_hook, encode_arguments
from flow_py_sdk.client import entities
from flow_py_sdk.proto.flow.access import (
    AccessAPIStub,
    PingResponse,
)
from flow_py_sdk.script import Script
from flow_py_sdk.tx import Tx, TransactionStatus

log = logging.getLogger(__name__)


class AccessAPI(AccessAPIStub):
    def __init__(
        self,
        channel: "Channel",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata=None,
    ) -> None:
        super().__init__(
            channel=channel, timeout=timeout, deadline=deadline, metadata=metadata
        )

    async def __aenter__(self) -> "AccessAPI":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.channel.close()

    async def get_latest_block_header(
        self, *, is_sealed: bool = False
    ) -> entities.BlockHeader:
        """
        Get the full payload of the latest sealed or unsealed block header.

        Parameters
        ----------
        is_sealed : bool
            Determine the requested block header should be sealed or not.

        Returns
        -------
        entities.BlockHeader
            Return requested block header.

        """
        response = await super().get_latest_block_header(is_sealed=is_sealed)
        return entities.BlockHeader.from_proto(response.block)

    async def get_block_header_by_i_d(self, *, id: bytes = b"") -> entities.BlockHeader:
        """
        Get a block header using its ID.

        Parameters
        ----------
        id : bytes
            ID of requested block header.

        Returns
        -------
        entities.BlockHeader
            Return requested block header.

        """
        response = await super().get_block_header_by_i_d(id=id)
        return entities.BlockHeader.from_proto(response.block)

    async def get_block_header_by_height(
        self, *, height: int = 0
    ) -> entities.BlockHeader:
        """
        Get a block header using its height.

        Parameters
        ----------
        id : bytes
            ID of requested block header.

        Returns
        -------
        entities.BlockHeader
            Return requested block header.

        """
        response = await super().get_block_header_by_height(height=height)
        return entities.BlockHeader.from_proto(response.block)

    async def get_latest_block(self, *, is_sealed: bool = False) -> entities.Block:
        """
        Get the full payload of the latest sealed or unsealed block.

        Parameters
        ----------
        is_sealed : bool
            Determine the requested block should be sealed or not.

        Returns
        -------
        entities.Block
            Return requested block.

        """
        response = await super(AccessAPI, self).get_latest_block(is_sealed=is_sealed)
        return entities.Block.from_proto(response.block)

    async def get_block_by_i_d(self, *, id: bytes = b"") -> entities.Block:
        """
        Get a block using its ID.

        Parameters
        ----------
        id : bytes
            ID of requested block.

        Returns
        -------
        entities.Block
            Return requested block.

        """
        response = await super().get_block_by_i_d(id=id)
        return entities.Block.from_proto(response.block)

    async def get_block_by_height(self, *, height: int = 0) -> entities.Block:
        """
        Get a block using its height.

        Parameters
        ----------
        height : int
            Height of requested block.

        Returns
        -------
        entities.Block
            Return requested block.

        """
        response = await super().get_block_by_height(height=height)
        return entities.Block.from_proto(response.block)

    async def get_collection_by_i_d(self, *, id: bytes = b"") -> entities.Collection:
        """
        Get a collection using its ID.

        Parameters
        ----------
        ID : bytes
            ID of requested collection.

        Returns
        -------
        entities.Collection
            Return requested collection.

        """
        response = await super().get_collection_by_i_d(id=id)
        return entities.Collection.from_proto(response.collection)

    async def get_transaction(self, *, id: bytes = b"") -> entities.Transaction:
        """
        Get a transaction using its ID.

        Parameters
        ----------
        ID : bytes
            ID of requested transaction.

        Returns
        -------
        entities.Transaction
            Return requested transaction.

        """
        response = await super().get_transaction(id=id)
        return entities.Transaction.from_proto(response.transaction)

    async def get_account(self, *, address: bytes = b"") -> entities.Account:
        """
        Get an account using its address.

        Parameters
        ----------
        address : bytes
            Address of requested account.

        Returns
        -------
        entities.Account
            Return requested account.

        """
        response = await super().get_account(address=address)
        return entities.Account.from_proto(response.account)

    async def get_account_at_latest_block(
        self, *, address: bytes = b""
    ) -> entities.Account:
        """
        Get an account by address at the latest sealed block.

        Parameters
        ----------
        address : bytes
            Address of requested account.

        Returns
        -------
        entities.Account
            Return requested account.

        """
        response = await super().get_account_at_latest_block(address=address)
        return entities.Account.from_proto(response.account)

    async def get_account_at_block_height(
        self, *, address: bytes = b"", block_height: int = 0
    ) -> entities.Account:
        """
        Get an account by address at the given block height.

        Parameters
        ----------
        address : bytes
            Address of requested account.
        block_height : int
            Desired block height.

        Returns
        -------
        entities.Account
            Return requested account.

        """
        response = await super().get_account_at_block_height(
            address=address, block_height=block_height
        )
        return entities.Account.from_proto(response.account)

    async def execute_script_at_latest_block(
        self, *, script: bytes = b"", arguments: List[bytes] = []
    ) -> bytes:
        """
        Execute a read-only Cadence script against the latest sealed block.
        The script is executed on an execution node and the return value is encoded using the JSON-Cadence data interchange format.

        Parameters
        ----------
        script : bytes
            Cadence script which is wanted to perform.
        argument : List[bytes]
            List of argument which is need for performing script.

        Returns
        -------
        bytes
            Return value is encoded using the JSON-Cadence data interchange format.

        """
        response = await super().execute_script_at_latest_block(
            script=script, arguments=arguments
        )
        return response.value

    async def execute_script_at_block_i_d(
        self, *, block_id: bytes = b"", script: bytes = b"", arguments: List[bytes] = []
    ) -> bytes:
        """
        Execute a read-only Cadence script against the desired block with specific ID.
        The script is executed on an execution node and the return value is encoded using the JSON-Cadence data interchange format.

        Parameters
        ----------
        block_id: bytes
            ID of desired block.
        script : bytes
            Cadence script which is wanted to perform.
        argument : List[bytes]
            List of argument which is need for performing script.

        Returns
        -------
        bytes
            Return value is encoded using the JSON-Cadence data interchange format.

        """
        response = await super().execute_script_at_block_i_d(
            block_id=block_id, script=script, arguments=arguments
        )
        return response.value

    async def execute_script_at_block_height(
        self, *, block_height: int = 0, script: bytes = b"", arguments: List[bytes] = []
    ) -> bytes:
        """
        Execute a read-only Cadence script against the desired block with specific height.
        The script is executed on an execution node and the return value is encoded using the JSON-Cadence data interchange format.

        Parameters
        ----------
        block_height: int
            Height of desired block.
        script : bytes
            Cadence script which is wanted to perform.
        argument : List[bytes]
            List of argument which is need for performing script.

        Returns
        -------
        bytes
            Return value is encoded using the JSON-Cadence data interchange format.

        """
        response = await super().execute_script_at_block_height(
            block_height=block_height, script=script, arguments=arguments
        )
        return response.value

    async def get_events_for_height_range(
        self, *, type: str = "", start_height: int = 0, end_height: int = 0
    ) -> list[entities.EventsResponseResult]:
        """
        Query on blocks in specific height.
        The script is executed on an execution node and the return value is encoded using the JSON-Cadence data interchange format.

        Parameters
        ----------
        type : str
            Type of requested type.
        start_height: int
            Start of desired range.
        end_height : int
            End of desired range.

        Returns
        -------
        List[entities.EventsResponseResult]
            Return the event results that are grouped by block, with each group specifying a block ID, height and block timestamp.

        """
        response = await super().get_events_for_height_range(
            type=type, start_height=start_height, end_height=end_height
        )
        return [entities.EventsResponseResult.from_proto(er) for er in response.results]

    async def get_events_for_block_i_ds(
        self, *, type: str = "", block_ids: List[bytes] = []
    ) -> list[entities.EventsResponseResult]:
        """
        Query on blocks with specific IDs.
        The script is executed on an execution node and the return value is encoded using the JSON-Cadence data interchange format.

        Parameters
        ----------
        type : str
            Type of requested type.
        block_ids: List[bytes]
            List of desired blocks.

        Returns
        -------
        list[entities.EventsResponseResult]
            Return the event results that are grouped by block, with each group specifying a block ID, height and block timestamp.

        """
        response = await super().get_events_for_block_i_ds(
            type=type, block_ids=block_ids
        )
        return [entities.EventsResponseResult.from_proto(er) for er in response.results]

    async def get_network_parameters(self) -> entities.GetNetworkParametersResponse:
        """
        Retrieve the network parameters.

        Parameters
        ----------

        Returns
        -------
        entities.GetNetworkParametersResponse

        """
        response = await super().get_network_parameters()
        return entities.GetNetworkParametersResponse.from_proto(response)

    async def execute_script(
        self,
        script: Script,
        at_block_id: Optional[bytes] = None,
        at_block_height: Optional[int] = None,
    ) -> Optional[Value]:
        """
        Execute a read-only Cadence script against the desired block with specific height or ID.
        The script is executed on an execution node and the return value is encoded using the JSON-Cadence data interchange format.

        Parameters
        ----------
        script : bytes
            Cadence script which is wanted to perform.
        block_id: int
            ID of desired block.
        block_height: int
            Height of desired block.

        Returns
        -------
        Optional[Value]
            Return value is encoded using the JSON-Cadence data interchange format.

        """
        s = script.code.encode("utf-8")
        a = encode_arguments(script.arguments)

        if at_block_id is not None:
            log.debug(f"Executing script at block id {at_block_id.hex()}")
            result = await self.execute_script_at_block_i_d(
                script=s, arguments=a, block_id=at_block_id
            )
        elif at_block_height is not None:
            log.debug(f"Executing script at block height {at_block_height}")
            result = await self.execute_script_at_block_height(
                script=s, arguments=a, block_height=at_block_height
            )
        else:
            log.debug(
                f"Executing script at latest block",
            )
            result = await self.execute_script_at_latest_block(script=s, arguments=a)

        log.debug(f"Script Executed")

        if result is None or result is None:
            return None
        cadence_value = json.loads(result, object_hook=cadence_object_hook)
        return cadence_value

    async def ping(self) -> PingResponse:
        """
        will return a successful response if the Access API is ready and available.

        Parameters
        ----------

        Returns
        -------

        """
        return await super().ping()

    async def send_transaction(
        self, *, transaction: Optional[entities.Transaction] = None
    ) -> entities.SendTransactionResponse:
        """
        Submit a transaction to the network.

        Parameters
        ----------
        transaction: Optional[entities.Transaction]
            A transaction object contains parameters like script, arguments, proposal_key, reference_block_id ...

        Returns
        -------
        entities.SendTransactionResponse
            Returns id of block

        """
        response = await super().send_transaction(transaction=transaction)
        return entities.SendTransactionResponse.from_proto(response)

    async def get_transaction_result(
        self, *, id: bytes = b""
    ) -> entities.TransactionResultResponse:
        """
        Get a transaction response.

        Parameters
        ----------
        id: byte
            Id of requested transaction.

        Returns
        -------
        entities.TransactionResultResponse
            Returns id of block

        """
        response = await super().get_transaction_result(id=id)
        return entities.TransactionResultResponse.from_proto(response)

    async def execute_transaction(
        self, tx: Tx, *, wait_for_seal=True, timeout: Annotated[float, "seconds"] = 30.0
    ) -> entities.TransactionResultResponse:
        """
        Submit a transaction to the network and wait to return its response.

        Parameters
        ----------
        tx: entities.Transaction
            A transaction object contains parameters like script, arguments, proposal_key, reference_block_id ...
        wait_for_seal: bool
            Return response when the block is sealed.
        timeout: float
            Time the function should wait for response

        Returns
        -------
        entities.TransactionResultResponse
            Returns id of block

        """
        log.debug(f"Sending transaction")
        result = await self.send_transaction(transaction=tx.to_signed_grpc())
        log.info(f"Sent transaction {result.id.hex()}")
        tx_result = await self.get_transaction_result(id=result.id)
        if tx_result.error_message:
            raise Exception(tx_result.error_message)  # TODO wrap error

        if not wait_for_seal:
            return tx_result

        log.info(f"Waiting for transaction to seal")

        end_time = time.monotonic() + timeout
        while (
            TransactionStatus(tx_result.status)
            is not TransactionStatus.TransactionStatusSealed
            and time.monotonic() < end_time
        ):
            await asyncio.sleep(1)
            tx_result = await self.get_transaction_result(id=result.id)

        if (
            TransactionStatus(tx_result.status)
            is not TransactionStatus.TransactionStatusSealed
        ):
            raise TimeoutError(f"Waiting for transaction {result.id.hex()} to seal")

        if tx_result.error_message:
            raise Exception(tx_result.error_message)  # TODO wrap error

        log.info(f"Got transaction seal")
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
    deadline: Optional["Deadline"] = None,
    metadata=None,
) -> AccessAPI:
    channel = Channel(
        host=host,
        port=port,
        loop=loop,
        path=path,
        codec=codec,
        status_details_codec=status_details_codec,
        ssl=ssl,
        config=config,
    )

    return AccessAPI(
        channel=channel, timeout=timeout, deadline=deadline, metadata=metadata
    )
