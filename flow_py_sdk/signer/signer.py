from abc import ABC, abstractmethod
from typing import Optional

from flow_py_sdk.exceptions import PySDKError

DomainTagLength = 32


def _padded_domain_tag(s: str) -> bytes:
    encoded = s.encode("utf-8")
    if len(encoded) > DomainTagLength:
        raise PySDKError(
            f"domain tag {s} cannot be longer than {DomainTagLength} bytes"
        )
    return encoded + bytearray(DomainTagLength - len(s))


TransactionDomainTag = _padded_domain_tag("FLOW-V0.0-transaction")
UserDomainTag = _padded_domain_tag("FLOW-V0.0-user")


class Signer(ABC):
    """The Signer class

    This is an abstract base class that is used for signing transactions and messages.
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def sign(self, message: bytes, tag: Optional[bytes] = None) -> bytes:
        """The sign method signs a message with a tag and returns the signature

        Parameters
        ----------
        message : bytes
            The message to sign.
        tag : str
            The tag to sign with.

        Returns
        -------
        bytes
            The signed message.

        """
        pass

    def sign_transaction(self, message: bytes) -> bytes:
        """The sign_user_message method signs a message with the transaction tag and returns the signature

        Used to sign user messages

        Parameters
        ----------
        message : bytes
            The message to sign.

        Returns
        -------
        bytes
            The signed message.

        """
        return self.sign(message, TransactionDomainTag)

    def sign_user_message(self, message: bytes) -> bytes:
        """The sign_user_message method signs a message with the user tag and returns the signature

        Used to sign user messages

        Parameters
        ----------
        message : int
            The message to sign.

        Returns
        -------
        bytes
            The signed message.

        """
        return self.sign(message, UserDomainTag)
