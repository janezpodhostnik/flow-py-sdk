import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from flow_py_sdk.account_key import AccountKey
from flow_py_sdk.cadence import cadence_object_hook
from flow_py_sdk.proto.flow import entities, access


class Account(object):
    def __init__(
        self,
        address: bytes,
        balance: int,
        code: bytes,
        keys: List[AccountKey],
        contracts: Dict[str, bytes],
    ) -> None:
        super().__init__()
        self.address: bytes = address
        self.balance: int = balance
        self.code: bytes = code
        self.keys: List[AccountKey] = keys
        self.contracts: Dict[str, bytes] = contracts

    @classmethod
    def from_proto(cls, proto: entities.Account) -> "Account":
        return Account(
            address=proto.address,
            balance=proto.balance,
            code=proto.code,
            keys=[AccountKey.from_proto(k) for k in proto.keys],
            contracts=proto.contracts,
        )


class BlockHeader(object):
    def __init__(
        self,
        id: bytes,
        parent_id: bytes,
        height: int,
        timestamp: datetime,
    ) -> None:
        self.id: bytes = id
        self.parent_id: bytes = parent_id
        self.height: int = height
        self.timestamp: datetime = timestamp

    @classmethod
    def from_proto(cls, proto: entities.BlockHeader) -> "BlockHeader":
        return BlockHeader(
            id=proto.id,
            parent_id=proto.parent_id,
            height=proto.height,
            timestamp=proto.timestamp,
        )


class Collection(object):
    def __init__(self, id: bytes, transaction_ids: List[bytes]) -> None:
        self.id: bytes = id
        self.transaction_ids: List[bytes] = transaction_ids

    @classmethod
    def from_proto(cls, proto: entities.Collection) -> "Collection":
        return Collection(id=proto.id, transaction_ids=proto.transaction_ids)


class CollectionGuarantee(object):
    def __init__(self, collection_id: bytes, signatures: List[bytes]) -> None:
        self.collection_id: bytes = collection_id
        self.signatures: List[bytes] = signatures

    @classmethod
    def from_proto(cls, proto: entities.CollectionGuarantee) -> "CollectionGuarantee":
        return CollectionGuarantee(
            collection_id=proto.collection_id, signatures=proto.signatures
        )


class BlockSeal(object):
    def __init__(
        self,
        block_id: bytes,
        execution_receipt_id: bytes,
        execution_receipt_signatures: List[bytes],
        result_approval_signatures: List[bytes],
    ) -> None:
        self.block_id: bytes = block_id
        self.execution_receipt_id: bytes = execution_receipt_id
        self.execution_receipt_signatures: List[bytes] = execution_receipt_signatures
        self.result_approval_signatures: List[bytes] = result_approval_signatures

    @classmethod
    def from_proto(cls, proto: entities.BlockSeal) -> "BlockSeal":
        return BlockSeal(
            block_id=proto.block_id,
            execution_receipt_id=proto.execution_receipt_id,
            execution_receipt_signatures=proto.execution_receipt_signatures,
            result_approval_signatures=proto.result_approval_signatures,
        )


@dataclass
class Block(object):
    def __init__(
        self,
        id: bytes,
        parent_id: bytes,
        height: int,
        timestamp: datetime,
        collection_guarantees: List[CollectionGuarantee],
        block_seals: List[BlockSeal],
        signatures: List[bytes],
    ) -> None:
        self.id: bytes = id
        self.parent_id: bytes = parent_id
        self.height: int = height
        self.timestamp: datetime = timestamp
        self.collection_guarantees: List[CollectionGuarantee] = collection_guarantees
        self.block_seals: List[BlockSeal] = block_seals
        self.signatures: List[bytes] = signatures

    @classmethod
    def from_proto(cls, proto: entities.Block) -> "Block":
        return Block(
            id=proto.id,
            parent_id=proto.parent_id,
            height=proto.height,
            timestamp=proto.timestamp,
            collection_guarantees=proto.collection_guarantees,
            block_seals=proto.block_seals,
            signatures=proto.signatures,
        )


class Event(object):
    def __init__(
        self,
        _type: str,
        transaction_id: bytes,
        transaction_index: int,
        event_index: int,
        payload: bytes,
    ) -> None:
        self.type: str = _type
        self.transaction_id: bytes = transaction_id
        self.transaction_index: int = transaction_index
        self.event_index: int = event_index
        self.payload: bytes = payload
        self.value: cadence.Event = json.loads(payload, object_hook=cadence_object_hook)

    @classmethod
    def from_proto(cls, proto: entities.Event) -> "Event":
        return Event(
            _type=proto.type,
            transaction_id=proto.transaction_id,
            transaction_index=proto.transaction_index,
            event_index=proto.event_index,
            payload=proto.payload,
        )


class Transaction(object):
    def __init__(
        self,
        script: bytes,
        arguments: List[bytes],
        reference_block_id: bytes,
        gas_limit: int,
        proposal_key: "TransactionProposalKey",
        payer: bytes,
        authorizers: List[bytes],
        payload_signatures: List["TransactionSignature"],
        envelope_signatures: List["TransactionSignature"],
    ) -> None:
        self.script: bytes = script
        self.arguments: List[bytes] = arguments
        self.reference_block_id: bytes = reference_block_id
        self.gas_limit: int = gas_limit
        self.proposal_key: "TransactionProposalKey" = proposal_key
        self.payer: bytes = payer
        self.authorizers: List[bytes] = authorizers
        self.payload_signatures: List["TransactionSignature"] = payload_signatures
        self.envelope_signatures: List["TransactionSignature"] = envelope_signatures

    @classmethod
    def from_proto(cls, proto: entities.Transaction) -> "Transaction":
        return Transaction(
            script=proto.script,
            arguments=proto.arguments,
            reference_block_id=proto.reference_block_id,
            gas_limit=proto.gas_limit,
            proposal_key=proto.proposal_key,
            payer=proto.payer,
            authorizers=proto.authorizers,
            payload_signatures=proto.payload_signatures,
            envelope_signatures=proto.envelope_signatures,
        )


class TransactionProposalKey(object):
    def __init__(self, address: bytes, key_id: int, sequence_number: int) -> None:
        self.address: bytes = address
        self.key_id: int = key_id
        self.sequence_number: int = sequence_number

    @classmethod
    def from_proto(
        cls, proto: entities.TransactionProposalKey
    ) -> "TransactionProposalKey":
        return TransactionProposalKey(
            address=proto.address,
            key_id=proto.key_id,
            sequence_number=proto.sequence_number,
        )


class TransactionSignature(object):
    def __init__(self, address: bytes, key_id: int, signature: bytes) -> None:
        self.address: bytes = address
        self.key_id: int = key_id
        self.signature: bytes = signature

    @classmethod
    def from_proto(cls, proto: entities.TransactionSignature) -> "TransactionSignature":
        return TransactionSignature(
            address=proto.address, key_id=proto.key_id, signature=proto.signature
        )


class EventsResponseResult(object):
    def __init__(
        self,
        block_id: bytes,
        block_height: int,
        events: List[Event],
        block_timestamp: datetime,
    ) -> None:
        self.block_id: bytes = block_id
        self.block_height: int = block_height
        self.events: List[Event] = events
        self.block_timestamp: datetime = block_timestamp

    @classmethod
    def from_proto(cls, proto: access.EventsResponseResult) -> "EventsResponseResult":
        return EventsResponseResult(
            block_id=proto.block_id,
            block_height=proto.block_height,
            events=[Event.from_proto(e) for e in proto.events],
            block_timestamp=proto.block_timestamp,
        )


class GetNetworkParametersResponse(object):
    def __init__(
        self,
        chain_id: str,
    ) -> None:
        self.chain_id: str = chain_id

    @classmethod
    def from_proto(
        cls, proto: access.GetNetworkParametersResponse
    ) -> "GetNetworkParametersResponse":
        return GetNetworkParametersResponse(chain_id=proto.chain_id)


class TransactionResultResponse(object):
    def __init__(
        self,
        status: entities.TransactionStatus,
        status_code: int,
        error_message: str,
        events: List[Event],
    ) -> None:
        self.status: entities.TransactionStatus = status
        self.status_code: int = status_code
        self.error_message: str = error_message
        self.events: List[Event] = events

    @classmethod
    def from_proto(
        cls, proto: access.TransactionResultResponse
    ) -> "TransactionResultResponse":
        return TransactionResultResponse(
            status=proto.status,
            status_code=proto.status_code,
            error_message=proto.error_message,
            events=[Event.from_proto(e) for e in proto.events],
        )


class SendTransactionResponse(object):
    def __init__(self, _id: bytes) -> None:
        self.id: bytes = _id

    @classmethod
    def from_proto(
        cls, proto: access.SendTransactionResponse
    ) -> "SendTransactionResponse":
        return SendTransactionResponse(_id=proto.id)
