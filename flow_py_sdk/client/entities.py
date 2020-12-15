# from dataclasses import dataclass
# from datetime import datetime
# from typing import Dict, List
#
# from flow_py_sdk.proto.flow import entities
#
#
# class AccountKey(object):
#     def __init__(self,
#                  index: int,
#                  public_key: bytes,
#                  sign_algo: int,
#                  hash_algo: int,
#                  weight: int,
#                  sequence_number: int,
#                  revoked: bool) -> None:
#         super().__init__()
#         self.index: int = index
#         self.public_key: bytes = public_key
#         self.sign_algo: int = sign_algo
#         self.hash_algo: int = hash_algo
#         self.weight: int = weight
#         self.sequence_number: int = sequence_number
#         self.revoked: bool = revoked
#
#     @classmethod
#     def from_proto(cls, proto: entities.AccountKey) -> 'AccountKey':
#         return AccountKey(index=proto.index,
#                           public_key=proto.public_key,
#                           sign_algo=proto.sign_algo,
#                           hash_algo=proto.hash_algo,
#                           weight=proto.weight,
#                           sequence_number=proto.sequence_number,
#                           revoked=proto.revoked)
#
#
# class Account(object):
#     def __init__(self, address: bytes,
#                  balance: int,
#                  code: bytes,
#                  keys: List[AccountKey],
#                  contracts: Dict[str, bytes]) -> None:
#         super().__init__()
#         self.address: bytes = address
#         self.balance: int = balance
#         self.code: bytes = code
#         self.keys: List[AccountKey] = keys
#         self.contracts: Dict[str, bytes] = contracts
#
#     @classmethod
#     def from_proto(cls, proto: entities.Account) -> 'Account':
#         return Account(address=proto.address,
#                        balance=proto.balance,
#                        code=proto.code,
#                        keys=[AccountKey.from_proto(k) for k in proto.keys],
#                        contracts=proto.contracts)
#
#
# class BlockHeader(object):
#     def __init__(self,
#                  id: bytes,
#                  parent_id: bytes,
#                  height: int,
#                  timestamp: datetime,
#                  ) -> None:
#         self.id: bytes = id
#         self.parent_id: bytes = parent_id
#         self.height: int = height
#         self.timestamp: datetime = timestamp
#
#     @classmethod
#     def from_proto(cls, proto: entities.BlockHeader) -> 'BlockHeader':
#         return BlockHeader(id=proto.id,
#                            parent_id=proto.parent_id,
#                            height=proto.height,
#                            timestamp=proto.timestamp)
#
#
# class Collection(object):
#     def __init__(self,
#                  id: bytes,
#                  transaction_ids: List[bytes]) -> None:
#         self.id: bytes = id
#         self.transaction_ids: List[bytes] = transaction_ids
#
#     @classmethod
#     def from_proto(cls, proto: entities.Collection) -> 'Collection':
#         return Collection(id=proto.id,
#                           transaction_ids=proto.transaction_ids)
#
#
# class CollectionGuarantee(object):
#     def __init__(self,
#                  collection_id: bytes,
#                  signatures: List[bytes]) -> None:
#         self.collection_id: bytes = collection_id
#         self.signatures: List[bytes] = signatures
#
#     @classmethod
#     def from_proto(cls, proto: entities.CollectionGuarantee) -> 'CollectionGuarantee':
#         return CollectionGuarantee(collection_id=proto.collection_id,
#                                    signatures=proto.signatures)
#
#
# class BlockSeal(object):
#     def __init__(self,
#                  block_id: bytes,
#                  execution_receipt_id: bytes,
#                  execution_receipt_signatures: List[bytes],
#                  result_approval_signatures: List[bytes]) -> None:
#         self.block_id: bytes = block_id
#         self.execution_receipt_id: bytes = execution_receipt_id
#         self.execution_receipt_signatures: List[bytes] = execution_receipt_signatures
#         self.result_approval_signatures: List[bytes] = result_approval_signatures
#
#     @classmethod
#     def from_proto(cls, proto: entities.BlockSeal) -> 'BlockSeal':
#         return BlockSeal(block_id=proto.block_id,
#                          execution_receipt_id=proto.execution_receipt_id,
#                          execution_receipt_signatures=proto.execution_receipt_signatures,
#                          result_approval_signatures=proto.result_approval_signatures)
#
#
# @dataclass
# class Block(object):
#     def __init__(self,
#                  id: bytes,
#                  parent_id: bytes,
#                  height: int,
#                  timestamp: datetime,
#                  collection_guarantees: List[CollectionGuarantee],
#                  block_seals: List[BlockSeal],
#                  signatures: List[bytes],
#                  ) -> None:
#         self.id: bytes = id
#         self.parent_id: bytes = parent_id
#         self.height: int = height
#         self.timestamp: datetime = timestamp
#         self.collection_guarantees: List[CollectionGuarantee] = collection_guarantees
#         self.block_seals: List[BlockSeal] = block_seals
#         self.signatures: List[bytes] = signatures
#
#     @classmethod
#     def from_proto(cls, proto: entities.Block) -> 'Block':
#         return Block(id=proto.id,
#                      parent_id=proto.parent_id,
#                      height=proto.height,
#                      timestamp=proto.timestamp,
#                      collection_guarantees=proto.collection_guarantees,
#                      block_seals=proto.block_seals,
#                      signatures=proto.signatures)
#
#
# class Event(object):
#     def __init__(self,
#                  id: bytes,
#                  parent_id: bytes,
#                  height: int,
#                  timestamp: datetime,
#                  collection_guarantees: List[CollectionGuarantee],
#                  block_seals: List[BlockSeal],
#                  signatures: List[bytes],
#                  ) -> None:
#     type: str = betterproto.string_field(1)
#     transaction_id: bytes = betterproto.bytes_field(2)
#     transaction_index: int = betterproto.uint32_field(3)
#     event_index: int = betterproto.uint32_field(4)
#     payload: bytes = betterproto.bytes_field(5)
#
#
# @dataclass
# class Transaction(betterproto.Message):
#     script: bytes = betterproto.bytes_field(1)
#     arguments: List[bytes] = betterproto.bytes_field(2)
#     reference_block_id: bytes = betterproto.bytes_field(3)
#     gas_limit: int = betterproto.uint64_field(4)
#     proposal_key: "TransactionProposalKey" = betterproto.message_field(5)
#     payer: bytes = betterproto.bytes_field(6)
#     authorizers: List[bytes] = betterproto.bytes_field(7)
#     payload_signatures: List["TransactionSignature"] = betterproto.message_field(8)
#     envelope_signatures: List["TransactionSignature"] = betterproto.message_field(9)
#
#
# @dataclass
# class TransactionProposalKey(betterproto.Message):
#     address: bytes = betterproto.bytes_field(1)
#     key_id: int = betterproto.uint32_field(2)
#     sequence_number: int = betterproto.uint64_field(3)
#
#
# @dataclass
# class TransactionSignature(betterproto.Message):
#     address: bytes = betterproto.bytes_field(1)
#     key_id: int = betterproto.uint32_field(2)
#     signature: bytes = betterproto.bytes_field(3)
