from typing import Optional

import ecdsa

from flow_py_sdk.signer.hash_algo import HashAlgo
from flow_py_sdk.signer.sign_algo import SignAlgo
from flow_py_sdk.signer.signer import Signer


class InMemorySigner(Signer):
    """The InMemorySigner used for signing transaction and messaged given a private key hex."""

    def __init__(
        self, *, hash_algo: HashAlgo, sign_algo: SignAlgo, private_key_hex: str
    ) -> None:
        super().__init__()
        self.hash_algo = hash_algo
        self.key = ecdsa.SigningKey.from_string(
            bytes.fromhex(private_key_hex), curve=sign_algo.get_signing_curve()
        )

    def sign(self, message: bytes, tag: Optional[bytes] = None) -> bytes:
        m = self.hash_algo.create_hasher()
        if tag:
            m.update(tag + message)
        else:
            m.update(message)
        hash_ = m.digest()
        return self.key.sign_digest_deterministic(hash_)
