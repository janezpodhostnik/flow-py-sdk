from abc import ABC, abstractmethod
from typing import Optional


class Signer(ABC):
    """The Signer class

    This is an abstract base class that is used for signing transactions and messages.
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def sign(self, message: bytes, tag: Optional[bytes] = None) -> bytes:
        """The signe method signs a message with a tag and returns the signature

        Parameters
        ----------
        message : int
            The message to sign.
        tag : str
            The tag to sign with.

        Returns
        -------
        bytes
            The signe message and tag.

        """
        pass
