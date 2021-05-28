from abc import ABC, abstractmethod


class Signer(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def sign(self, message: bytes, tag: bytes) -> bytes:
        pass
