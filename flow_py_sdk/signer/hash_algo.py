from __future__ import annotations

import hashlib

from enum import IntEnum


class HashAlgo(IntEnum):
    SHA2_256 = 1
    SHA2_384 = 2
    SHA3_256 = 3
    SHA3_384 = 4

    @classmethod
    def from_string(cls, s: str) -> HashAlgo:
        return {
            "SHA2_256": HashAlgo.SHA2_256,
            "SHA2_384": HashAlgo.SHA2_384,
            "SHA3_256": HashAlgo.SHA3_256,
            "SHA3_384": HashAlgo.SHA3_384,
        }[s]

    def create_hasher(self):
        if self is HashAlgo.SHA2_256:
            return hashlib.sha256()
        if self == HashAlgo.SHA2_384:
            return hashlib.sha384()
        if self == HashAlgo.SHA3_256:
            return hashlib.sha3_256()
        if self == HashAlgo.SHA3_384:
            return hashlib.sha3_384()
        raise NotImplementedError()
