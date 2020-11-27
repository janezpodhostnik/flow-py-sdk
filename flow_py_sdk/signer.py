import hashlib
from abc import ABC, abstractmethod

from ecdsa import SigningKey, NIST256p, SECP256k1


class Signer(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def sign(self, message: bytes) -> bytes:
        pass


class InMemorySigner(Signer):
    def __init__(self, hash_algo: int, sign_algo: int, key_hex: str) -> None:
        super().__init__()
        self.hash_algo = hash_algo
        self.key = SigningKey.from_string(bytes.fromhex(key_hex), curve=get_signing_curve(sign_algo))

    def sign(self, message: bytes) -> bytes:
        m = create_hasher(self.hash_algo)
        m.update(message)
        hash_ = m.digest()
        return self.key.sign_digest_deterministic(hash_)

    def public_key(self) -> bytes:
        return self.key.verifying_key.to_string()


def create_hasher(hash_id: int):
    if hash_id == 1:
        return hashlib.sha256()
    if hash_id == 2:
        return hashlib.sha384()
    if hash_id == 3:
        return hashlib.sha3_256()
    if hash_id == 4:
        return hashlib.sha3_384()
    raise NotImplementedError()


def get_signing_curve(sign_algo: int):
    if sign_algo == 2:
        return NIST256p
    if sign_algo == 3:
        return SECP256k1
    raise NotImplementedError()
