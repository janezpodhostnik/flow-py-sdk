from __future__ import annotations

import ecdsa
from enum import IntEnum


class SignAlgo(IntEnum):
    ECDSA_P256 = 2
    ECDSA_secp256k1 = 3

    @classmethod
    def from_string(cls, s: str) -> SignAlgo:
        return {
            "ECDSA_P256": SignAlgo.ECDSA_P256,
            "ECDSA_secp256k1": SignAlgo.ECDSA_secp256k1,
        }[s]

    def get_signing_curve(self) -> ecdsa.curves.Curve:
        if self == SignAlgo.ECDSA_P256:
            return ecdsa.NIST256p
        if self == SignAlgo.ECDSA_secp256k1:
            return ecdsa.SECP256k1
        raise NotImplementedError()
