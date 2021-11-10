from typing import Optional

import ecdsa

from flow_py_sdk.signer.hash_algo import HashAlgo
from flow_py_sdk.signer.sign_algo import SignAlgo
from flow_py_sdk.signer.verifier import Verifier


class InMemoryVerifier(Verifier):
    def __init__(
        self, *, hash_algo: HashAlgo, sign_algo: SignAlgo, public_key_hex: str
    ) -> None:
        super().__init__()
        self.hash_algo = hash_algo
        self.key = ecdsa.VerifyingKey.from_string(
            bytes.fromhex(public_key_hex), curve=sign_algo.get_signing_curve()
        )

    def verify(self, signature: bytes, message: bytes, tag: bytes) -> bool:
        hash_ = self._hash_message(message, tag)
        try:
            return self.key.verify_digest(signature, hash_)
        except ecdsa.keys.BadSignatureError:
            return False

    def _hash_message(self, message: bytes, tag: Optional[bytes] = None) -> bytes:
        m = self.hash_algo.create_hasher()
        if tag:
            m.update(tag + message)
        else:
            m.update(message)
        return m.digest()
