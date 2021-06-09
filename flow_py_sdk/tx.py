import logging
from enum import Enum

import rlp

from flow_py_sdk.cadence import Value, Address, encode_arguments
from flow_py_sdk.exceptions import NotCadenceValueError, PySDKError
from flow_py_sdk.frlp import rlp_encode_uint64
from flow_py_sdk.proto.flow import entities
from flow_py_sdk.signer import Signer

log = logging.getLogger(__name__)


class TransactionStatus(Enum):
    # TransactionStatusUnknown indicates that the transaction status is not known.
    TransactionStatusUnknown = 0
    # TransactionStatusPending is the status of a pending transaction.
    TransactionStatusPending = 1
    # TransactionStatusFinalized is the status of a finalized transaction.
    TransactionStatusFinalized = 2
    # TransactionStatusExecuted is the status of an executed transaction.
    TransactionStatusExecuted = 3
    # TransactionStatusSealed is the status of a sealed transaction.
    TransactionStatusSealed = 4
    # TransactionStatusExpired is the status of an expired transaction.
    TransactionStatusExpired = 5


DomainTagLength = 32


def _padded_domain_tag(s: str) -> bytes:
    encoded = s.encode("utf-8")
    if len(encoded) > DomainTagLength:
        raise PySDKError(
            f"domain tag {s} cannot be longer than {DomainTagLength} bytes"
        )
    return encoded + bytearray(DomainTagLength - len(s))


TransactionDomainTag = _padded_domain_tag("FLOW-V0.0-transaction")


class TxSignature(object):
    def __init__(
        self, address: Address, key_id: int, signer_index: int, signature: bytes
    ) -> None:
        super().__init__()
        self.address: Address = address
        self.key_id: int = key_id
        self.signer_index: int = signer_index
        self.signature: bytes = signature

    def rpc_form(self) -> entities.TransactionSignature:
        s = entities.TransactionSignature()
        s.signature = self.signature
        s.key_id = self.key_id
        s.address = self.address.bytes
        return s


class ProposalKey(object):
    def __init__(
        self, *, key_address: Address, key_id: int, key_sequence_number: int
    ) -> None:
        super().__init__()
        self.key_address: Address = key_address
        self.key_id: int = key_id
        self.key_sequence_number: int = key_sequence_number


class Tx(object):
    def __init__(
        self,
        *,
        code: str,
        reference_block_id: bytes = None,
        payer: Address = None,
        proposal_key: ProposalKey = None,
    ) -> None:
        super().__init__()
        self.code: str = code
        self.reference_block_id: bytes = reference_block_id
        self.payer: Address = payer
        self.arguments: list[Value] = []
        self.gas_limit: int = 100
        self.authorizers: list[Address] = []
        self.proposal_key: ProposalKey = proposal_key
        self.payload_signatures: list[TxSignature] = []
        self.envelope_signatures: list[TxSignature] = []

    def with_gas_limit(self, gas_limit: int) -> "Tx":
        self.gas_limit = gas_limit
        return self

    def with_reference_block_id(self, reference_block_id: bytes) -> "Tx":
        self.reference_block_id = reference_block_id
        return self

    def with_payer(self, payer: Address) -> "Tx":
        self.payer = payer
        return self

    def with_proposal_key(self, proposal_key: ProposalKey) -> "Tx":
        self.proposal_key = proposal_key
        return self

    def _payload_form(self):
        return [
            self.code.encode("utf-8"),
            encode_arguments(self.arguments),
            self.reference_block_id,
            rlp_encode_uint64(self.gas_limit),
            self.proposal_key.key_address.bytes,
            rlp_encode_uint64(self.proposal_key.key_id),
            rlp_encode_uint64(self.proposal_key.key_sequence_number),
            self.payer.bytes,
            [a.bytes for a in self.authorizers],
        ]

    def payload_message(self) -> bytes:
        return rlp.encode(self._payload_form())

    def envelope_message(self) -> bytes:
        return rlp.encode(
            [
                self._payload_form(),
                [
                    [
                        rlp_encode_uint64(s.signer_index),
                        rlp_encode_uint64(s.key_id),
                        s.signature,
                    ]
                    for s in self.payload_signatures
                ],
            ]
        )

    def _signer_list(self) -> list[Address]:
        signers = []
        seen = {}

        def add_signer(address: Address):
            if address in seen:
                return

            signers.append(address)
            seen[address] = True

        add_signer(self.proposal_key.key_address)
        add_signer(self.payer)

        for authorizer in self.authorizers:
            add_signer(authorizer)

        return signers

    def with_payload_signature(
        self, address: Address, key_id: int, signer: Signer
    ) -> "Tx":
        if self._missing_fields_for_signing():
            raise Exception(
                f"The transaction needs [{', '.join(self._missing_fields_for_signing())}] before it can be signed"
            )
        signature = signer.sign(self.payload_message(), TransactionDomainTag)
        signer_index = self._signer_list().index(address)
        ts = TxSignature(address, key_id, signer_index, signature)
        self.payload_signatures.append(ts)
        return self

    def with_envelope_signature(
        self, address: Address, key_id: int, signer: Signer
    ) -> "Tx":
        if self._missing_fields_for_signing():
            raise Exception(
                f"The transaction needs [{', '.join(self._missing_fields_for_signing())}] before it can be signed"
            )
        signature = signer.sign(self.envelope_message(), TransactionDomainTag)
        signer_index = self._signer_list().index(address)
        ts = TxSignature(address, key_id, signer_index, signature)
        self.envelope_signatures.append(ts)
        return self

    def add_authorizers(self, *args: Address) -> "Tx":
        self.authorizers.extend(args)
        return self

    def add_arguments(self, *args: Value) -> "Tx":
        for arg in args:
            if not isinstance(arg, Value):
                raise NotCadenceValueError.from_value(arg)
        self.arguments.extend(args)
        return self

    def _missing_fields_for_signing(self) -> list[str]:
        mandatory_fields = {
            "code": self.code,
            "reference_block_id": self.reference_block_id,
            "payer": self.payer,
            "proposal_key": self.proposal_key,
        }
        return [k for (k, v) in mandatory_fields.items() if v is None]

    def to_grpc(self) -> entities.Transaction:
        tx = entities.Transaction()
        tx.script = self.code.encode("utf-8")
        tx.arguments = encode_arguments(self.arguments)
        tx.reference_block_id = self.reference_block_id
        tx.gas_limit = self.gas_limit
        tx.payer = self.payer.bytes
        tx.authorizers = [a.bytes for a in self.authorizers]

        proposal_key = entities.TransactionProposalKey()
        proposal_key.address = self.proposal_key.key_address.bytes
        proposal_key.key_id = self.proposal_key.key_id
        proposal_key.sequence_number = self.proposal_key.key_sequence_number

        tx.proposal_key = proposal_key
        tx.payload_signatures = [s.rpc_form() for s in self.payload_signatures]
        tx.envelope_signatures = [s.rpc_form() for s in self.envelope_signatures]

        return tx
