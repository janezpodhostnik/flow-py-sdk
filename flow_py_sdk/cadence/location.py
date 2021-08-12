from abc import ABC, abstractmethod
from typing import Tuple, Annotated

from flow_py_sdk.cadence.address import Address
from flow_py_sdk.exceptions import CadenceEncodingError


class Location(ABC):
    """Location describes the origin of a Cadence script.

    This could be a file, a transaction, or a smart contract.
    """

    def __init__(self):
        super(Location, self).__init__()

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def id(self) -> str:
        """

        Returns
        -------
        returns the canonical ID for this import location
        """
        pass

    @abstractmethod
    def type_id(self, qualified_identifier: str) -> str:
        """

        Parameters
        ----------
        qualified_identifier

        Returns
        -------
        returns a type ID for the given qualified_identifier
        """
        pass

    @abstractmethod
    def qualified_identifier(self, type_id: str) -> str:
        """

        Parameters
        ----------
        type_id

        Returns
        -------
        returns the qualified identifier for the given type_id
        """
        pass

    @classmethod
    @abstractmethod
    def decode(
        cls, type_id: str
    ) -> Tuple["Location", Annotated[str, "qualified identifier"]]:
        pass

    @classmethod
    @abstractmethod
    def prefix(cls) -> str:
        pass

    def __eq__(self, other):
        if isinstance(other, Location):
            return str(self) == str(other)
        return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(str(self))


class AddressLocation(Location):
    def __init__(self, address: Address, name: str) -> None:
        super().__init__()
        self.address: Address = address
        self.name: str = name

    def __str__(self) -> str:
        if not self.name:
            return str(self.address)
        return f"{self.address}.{self.name}"

    def id(self) -> str:
        if not self.name:
            return f"{self.prefix()}.{self.address.hex()}"
        return f"{self.prefix()}.{self.address.hex()}.{self.name}"

    def type_id(self, qualified_identifier: str) -> str:
        return f"{self.prefix()}.{self.address.hex()}.{qualified_identifier}"

    def qualified_identifier(self, type_id: str) -> str:
        pieces = type_id.split(".")
        if len(pieces) < 3:
            return ""
        return pieces[2]

    @classmethod
    def decode(
        cls, type_id: str
    ) -> Tuple["AddressLocation", Annotated[str, "qualified identifier"]]:
        err_prefix = "Invalid address location type ID"
        if not type_id:
            raise CadenceEncodingError(f"{err_prefix}: missing prefix.")

        parts = type_id.split(".", 4)

        if len(parts) == 1:
            raise CadenceEncodingError(f"{err_prefix}: missing location.")
        elif len(parts) == 2:
            raise CadenceEncodingError(f"{err_prefix}: missing qualified identifier.")

        if parts[0] != cls.prefix():
            raise CadenceEncodingError(
                f"{err_prefix}: invalid prefix, expected {cls.prefix()} got {parts[0]}."
            )

        address = Address.from_hex(parts[1])

        if len(parts) == 3:
            name = parts[2]
            qualified_identifier = name
        else:
            name = parts[2]
            qualified_identifier = f"{name}.{parts[3]}"

        location = AddressLocation(address, name)

        return location, qualified_identifier

    @classmethod
    def prefix(cls) -> str:
        return "A"


class FlowLocation(Location):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"{self.prefix()}"

    def id(self) -> str:
        return f"{self.prefix()}"

    def type_id(self, qualified_identifier: str) -> str:
        return f"{self.prefix()}.{qualified_identifier}"

    def qualified_identifier(self, type_id: str) -> str:
        pieces = type_id.split(".", 2)
        if len(pieces) < 2:
            return ""
        return pieces[1]

    @classmethod
    def decode(
        cls, type_id: str
    ) -> Tuple["FlowLocation", Annotated[str, "qualified identifier"]]:
        err_prefix = "invalid Flow location type ID"
        if not type_id:
            raise CadenceEncodingError(f"{err_prefix}: missing prefix.")

        parts = type_id.split(".", 2)

        if len(parts) == 1:
            raise CadenceEncodingError(f"{err_prefix}: missing qualified identifier.")

        if parts[0] != cls.prefix():
            raise CadenceEncodingError(
                f"{err_prefix}: invalid prefix, expected {cls.prefix()} got {parts[0]}."
            )
        qualified_identifier = parts[1]

        location = FlowLocation()

        return location, qualified_identifier

    @classmethod
    def prefix(cls) -> str:
        return "flow"


class StringLocation(Location):
    def __init__(
        self,
        location: str,
    ) -> None:
        super().__init__()
        self.location: str = location

    def __str__(self) -> str:
        return f"{self.location}"

    def id(self) -> str:
        return f"{self.prefix()}.{self.location}"

    def type_id(self, qualified_identifier: str) -> str:
        return f"{self.prefix()}.{self.location}.{qualified_identifier}"

    def qualified_identifier(self, type_id: str) -> str:
        pieces = type_id.split(".", 3)
        if len(pieces) < 3:
            return ""
        return pieces[2]

    @classmethod
    def decode(
        cls, type_id: str
    ) -> Tuple["StringLocation", Annotated[str, "qualified identifier"]]:
        err_prefix = "invalid string location type ID"
        if not type_id:
            raise CadenceEncodingError(f"{err_prefix}: missing prefix.")

        parts = type_id.split(".", 3)

        if len(parts) == 1:
            raise CadenceEncodingError(f"{err_prefix}: missing location.")
        if len(parts) == 2:
            raise CadenceEncodingError(f"{err_prefix}: missing qualified identifier.")

        if parts[0] != cls.prefix():
            raise CadenceEncodingError(
                f"{err_prefix}: invalid prefix, expected {cls.prefix()} got {parts[0]}."
            )
        qualified_identifier = parts[2]

        location = StringLocation(parts[1])

        return location, qualified_identifier

    @classmethod
    def prefix(cls) -> str:
        return "S"


class ScriptLocation(Location):
    def __init__(
        self,
        location: str,
    ) -> None:
        super().__init__()
        self.location: str = location

    def __str__(self) -> str:
        return f"{self.location}"

    def id(self) -> str:
        return f"{self.prefix()}.{self.location}"

    def type_id(self, qualified_identifier: str) -> str:
        return f"{self.prefix()}.{self.location}.{qualified_identifier}"

    def qualified_identifier(self, type_id: str) -> str:
        pieces = type_id.split(".", 3)
        if len(pieces) < 3:
            return ""
        return pieces[2]

    @classmethod
    def decode(
        cls, type_id: str
    ) -> Tuple["ScriptLocation", Annotated[str, "qualified identifier"]]:
        err_prefix = "invalid script location type ID"
        if not type_id:
            raise CadenceEncodingError(f"{err_prefix}: missing prefix.")

        parts = type_id.split(".", 3)

        if len(parts) == 1:
            raise CadenceEncodingError(f"{err_prefix}: missing location.")
        if len(parts) == 2:
            raise CadenceEncodingError(f"{err_prefix}: missing qualified identifier.")

        if parts[0] != cls.prefix():
            raise CadenceEncodingError(
                f"{err_prefix}: invalid prefix, expected {cls.prefix()} got {parts[0]}."
            )
        qualified_identifier = parts[2]

        location = ScriptLocation(parts[1])

        return location, qualified_identifier

    @classmethod
    def prefix(cls) -> str:
        return "s"


_location_types = [AddressLocation, FlowLocation, StringLocation, ScriptLocation]


def decode_location(
    type_id: str,
) -> Tuple["AddressLocation", Annotated[str, "qualified identifier"]]:
    parts = type_id.split(".")
    if len(parts) < 1:
        raise CadenceEncodingError("Invalid type ID: missing prefix.")

    prefix = parts[0]
    for loc in _location_types:
        if loc.prefix() == prefix:
            return loc.decode(type_id)

    raise CadenceEncodingError(f"Invalid type ID: cannot decode prefix {prefix}")
