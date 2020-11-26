import json
import logging
from typing import Optional

from flow_py_sdk.cadence.decode import cadence_object_hook
from flow_py_sdk.cadence.encode import CadenceJsonEncoder
from flow_py_sdk.cadence.types import Value, Address
from flow_py_sdk.proto.flow import entities
from flow_py_sdk.proto.flow.access import AccessAPIStub

log = logging.getLogger(__name__)


class Signer(object):
    pass


class Tx(object):
    def __init__(self, code: str) -> None:
        super().__init__()
        self.code: str = code
        self.arguments: list[Value] = []
        self.reference_block_id: Optional[bytes] = None
        self.gas_limit: int = 100
        self.payer: Optional[Address] = None
        self.authorizers: list[Address] = []
        self.proposalKey: Optional[(Address, int, int)] = None
        self.payload_signatures: list[entities.TransactionSignature] = []
        self.envelope_signatures: list[entities.TransactionSignature] = []

    def with_payer(self, payer: Address) -> 'Tx':
        self.payer = payer
        return self

    def with_proposal_key(self, proposer: Address, key_id: int, sequence_number: int) -> 'Tx':
        self.proposalKey = (proposer, key_id, sequence_number)
        return self

    def with_payload_signature(self, address: Address, key_id: int, signer: Signer) -> 'Tx':
        # self.payload_signatures.append()
        return self

    def with_envelope_signature(self, address: Address, key_id: int, signer: Signer) -> 'Tx':
        # self.envelope_signatures.append()
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
        proposal_key.address = self.proposalKey[0].bytes
        proposal_key.key_id = self.proposalKey[1]
        proposal_key.sequence_number = self.proposalKey[2]

        tx.proposal_key = proposal_key
        tx.payload_signatures = self.payload_signatures
        tx.envelope_signatures = self.envelope_signatures

        return tx

    def _encoded_arguments(self) -> list[bytes]:
        return [json.dumps(a, ensure_ascii=False, cls=CadenceJsonEncoder).encode('utf-8') for a in self.arguments]
