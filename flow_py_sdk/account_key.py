from __future__ import annotations
from typing import Optional

import rlp

from flow_py_sdk.frlp import rlp_encode_uint64
from flow_py_sdk.proto.flow import entities
from flow_py_sdk.signer import SignAlgo, HashAlgo


class AccountKey(object):
    weight_threshold: int = 1000

    def __init__(
        self,
        *,
        public_key: bytes,
        sign_algo: SignAlgo,
        hash_algo: HashAlgo,
        weight: Optional[int] = None
    ) -> None:
        super().__init__()
        self.index: Optional[int] = None
        self.public_key: bytes = public_key
        self.sign_algo: SignAlgo = sign_algo
        self.hash_algo: HashAlgo = hash_algo
        self.weight: int = weight if weight is not None else self.weight_threshold
        self.sequence_number: Optional[int] = None
        self.revoked: Optional[bool] = None

    def rlp(self) -> bytes:
        return rlp.encode(
            [
                self.public_key,
                rlp_encode_uint64(self.sign_algo.value),
                rlp_encode_uint64(self.hash_algo.value),
                rlp_encode_uint64(self.weight),
            ]
        )

    def hex(self):
        return self.rlp().hex()

    @classmethod
    def from_proto(cls, k: entities.AccountKey) -> AccountKey:
        ak = AccountKey(
            public_key=k.public_key,
            hash_algo=HashAlgo(k.hash_algo),
            sign_algo=SignAlgo(k.sign_algo),
            weight=k.weight,
        )
        ak.index = k.index
        ak.revoked = k.revoked
        ak.sequence_number = k.sequence_number

        return ak
