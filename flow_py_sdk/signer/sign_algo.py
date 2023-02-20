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

    def get_cadence_enum_value(self) -> int:
        """
        get_cadence_enum_value provide a way for user to get cadence enum value for signature algorithm.
        For some reason this is 1 less than the enum value in the go sdk code: https://github.com/onflow/flow-go-sdk/blob/9f5d7409940a99d663b214a3ba66d477c1761409/templates/accounts.go#L60
        Returns
        -------

        """
        return self.value - 1
