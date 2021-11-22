from typing import Optional

import ecdsa

from flow_py_sdk.signer.hash_algo import HashAlgo
from flow_py_sdk.signer.in_memory_verifier import InMemoryVerifier
from flow_py_sdk.signer.sign_algo import SignAlgo
from flow_py_sdk.signer.signer import Signer
from flow_py_sdk.signer.verifier import Verifier


class InMemorySigner(Signer, Verifier):
    def __init__(
        self, *, hash_algo: HashAlgo, sign_algo: SignAlgo, private_key_hex: str
    ) -> None:
        super().__init__()
        self.hash_algo = hash_algo
        self.key = ecdsa.SigningKey.from_string(
            bytes.fromhex(private_key_hex), curve=sign_algo.get_signing_curve()
        )
        self.verifier = InMemoryVerifier(
            hash_algo=hash_algo,
            sign_algo=sign_algo,
            public_key_hex=self.key.get_verifying_key().to_string().hex(),
        )

    def sign(self, message: bytes, tag: Optional[bytes] = None) -> bytes:
        hash_ = self._hash_message(message, tag)
        return self.key.sign_digest_deterministic(hash_)

    def verify(self, signature: bytes, message: bytes, tag: bytes) -> bool:
        return self.verifier.verify(signature, message, tag)

    def _hash_message(self, message: bytes, tag: Optional[bytes] = None) -> bytes:
        m = self.hash_algo.create_hasher()
        if tag:
            m.update(tag + message)
        else:
            m.update(message)
        return m.digest()
