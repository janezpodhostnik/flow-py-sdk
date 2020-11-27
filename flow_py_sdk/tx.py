import json
import logging
from typing import Optional

import rlp

from flow_py_sdk.cadence.encode import CadenceJsonEncoder
from flow_py_sdk.cadence.types import Value, Address
from flow_py_sdk.proto.flow import entities
from flow_py_sdk.signer import Signer

log = logging.getLogger(__name__)


class TxSignature(object):

    def __init__(self, address: Address, key_id: int, signer_index: int, signature: bytes) -> None:
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


class Tx(object):
    def __init__(self, code: str) -> None:
        super().__init__()
        self.code: Optional[str] = code
        self.arguments: list[Value] = []
        self.reference_block_id: Optional[bytes] = None
        self.gas_limit: int = 100
        self.payer: Optional[Address] = None
        self.authorizers: list[Address] = []
        self.proposal_key: Optional[(Address, int, int)] = None
        self.payload_signatures: list[TxSignature] = []
        self.envelope_signatures: list[TxSignature] = []

    def with_payer(self, payer: Address) -> 'Tx':
        self.payer = payer
        return self

    def with_gas_limit(self, gas_limit) -> 'Tx':
        self.gas_limit = gas_limit
        return self

    def with_code(self, code: Optional[str]) -> 'Tx':
        self.code = code
        return self

    def with_reference_block_id(self, reference_block_id: bytes) -> 'Tx':
        self.reference_block_id = reference_block_id
        return self

    def with_proposal_key(self, proposer: Address, key_id: int, sequence_number: int) -> 'Tx':
        self.proposal_key = (proposer, key_id, sequence_number)
        return self

    def _payload_form(self):
        return [
            self.code.encode('utf-8') if self.code is not None else ''.encode('utf-8'),
            self._encoded_arguments() if self._encoded_arguments() is not None else [],
            self.reference_block_id,
            self.gas_limit.to_bytes(8, 'big', signed=False).lstrip(b'\0'),
            self.proposal_key[0].bytes,
            self.proposal_key[1].to_bytes(8, 'big', signed=False).lstrip(b'\0'),
            self.proposal_key[2].to_bytes(8, 'big', signed=False).lstrip(b'\0'),
            self.payer.bytes,
            [a.bytes for a in self.authorizers]
        ]

    def payload_message(self) -> bytes:
        return rlp.encode(self._payload_form())

    def envelope_message(self) -> bytes:
        return rlp.encode([
            self._payload_form(),
            [[
                s.signer_index.to_bytes(8, 'big', signed=False).lstrip(b'\0'),
                s.key_id.to_bytes(8, 'big', signed=False).lstrip(b'\0'),
                s.signature
            ] for s in self.payload_signatures]
        ])

    def _signer_list(self) -> list[Address]:
        signers = []
        seen = {}

        def add_signer(address: Address):
            if address in seen:
                return

            signers.append(address)
            seen[address] = True

        if self.proposal_key is not None:
            add_signer(self.proposal_key[0])

        if self.payer is not None:
            add_signer(self.payer)

        for authorizer in self.authorizers:
            add_signer(authorizer)

        return signers

    def with_payload_signature(self, address: Address, key_id: int, signer: Signer) -> 'Tx':
        signature = signer.sign(self.payload_message())
        signer_index = self._signer_list().index(address)
        ts = TxSignature(address, key_id, signer_index, signature)
        self.payload_signatures.append(ts)
        return self

    def with_envelope_signature(self, address: Address, key_id: int, signer: Signer) -> 'Tx':
        signature = signer.sign(self.envelope_message())
        signer_index = self._signer_list().index(address)
        ts = TxSignature(address, key_id, signer_index, signature)
        self.envelope_signatures.append(ts)
        return self

    def add_authorizers(self, *args: Address) -> 'Tx':
        self.authorizers.extend(args)
        return self

    def add_arguments(self, *args: Value) -> 'Tx':
        self.arguments.extend(args)
        return self

    def to_grpc(self) -> entities.Transaction:
        tx = entities.Transaction()
        tx.script = self.code.encode('utf-8')
        tx.arguments = self._encoded_arguments()
        tx.reference_block_id = self.reference_block_id
        tx.gas_limit = self.gas_limit
        tx.payer = self.payer.bytes
        tx.authorizers = [a.bytes for a in self.authorizers]

        proposal_key = entities.TransactionProposalKey()
        proposal_key.address = self.proposal_key[0].bytes if self.proposal_key is not None else None
        proposal_key.key_id = self.proposal_key[1] if self.proposal_key is not None else None
        proposal_key.sequence_number = self.proposal_key[2] if self.proposal_key is not None else None

        tx.proposal_key = proposal_key
        tx.payload_signatures = [s.rpc_form() for s in self.payload_signatures]
        tx.envelope_signatures = [s.rpc_form() for s in self.envelope_signatures]

        return tx

    def _encoded_arguments(self) -> Optional[list[bytes]]:
        if len(self.arguments) == 0:
            return None
        return [
            (json.dumps(a, ensure_ascii=False, cls=CadenceJsonEncoder, separators=(',', ':')) + '\n').encode('utf-8')
            for a in self.arguments]
