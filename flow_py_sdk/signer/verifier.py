from abc import ABC, abstractmethod

from flow_py_sdk.signer import TransactionDomainTag, UserDomainTag


class Verifier(ABC):
    """The Verifier class

    This is an abstract base class that is used for transaction and message signature verification.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def verify(self, signature: bytes, message: bytes, tag: bytes) -> bool:
        """The verify method signs a message with a tag and returns the signature

        Parameters
        ----------
        signature : bytes
            The signature to verify.
        message : bytes
            The message to verify.
        tag : str
            The tag to verify.

        Returns
        -------
        bool
            Is the signature valid.

        """
        pass

    def verify_transaction(self, signature: bytes, message: bytes) -> bool:
        """The verify method signs a message with a transaction domain tag and returns the signature

        Parameters
        ----------
        signature : bytes
            The signature to verify.
        message : bytes
            The message to verify.

        Returns
        -------
        bool
            Is the signature valid.

        """
        return self.verify(signature, message, TransactionDomainTag)

    def verify_user_message(self, signature: bytes, message: bytes) -> bool:
        """The verify method signs a message with a user domain tag and returns the signature

        Parameters
        ----------
        signature : bytes
            The signature to verify.
        message : bytes
            The message to verify.
        Returns
        -------
        bool
            Is the signature valid.

        """
        return self.verify(signature, message, UserDomainTag)
