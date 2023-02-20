from __future__ import annotations

from flow_py_sdk.cadence.value import Value
import flow_py_sdk.cadence.constants as c

from flow_py_sdk.exceptions import NotAddressError


class Address(Value):
    address_length = 8
    address_prefix = "0x"

    def __init__(self, value: bytes) -> None:
        super().__init__()
        if len(value) > Address.address_length:
            raise Exception()  # TODO

        self.bytes = bytes(Address.address_length - len(value)) + value

    @classmethod
    def from_hex(cls, value: str) -> "Address":
        return Address(bytes.fromhex(value.removeprefix(Address.address_prefix)))

    def hex(self) -> str:
        return self.bytes.hex()

    def hex_with_prefix(self) -> str:
        return Address.address_prefix + self.bytes.hex()

    def __str__(self) -> str:
        return self.hex_with_prefix()

    def encode_value(self) -> dict:
        return {
            c.valueKey: self.hex_with_prefix(),
        }

    @classmethod
    def decode(cls, value) -> "Address":
        addr = str(value[c.valueKey])
        if addr[:2] != "0x":
            raise NotAddressError.from_value(addr)  # TODO
        return Address.from_hex(addr)

    @classmethod
    def type_str(cls) -> str:
        return c.addressTypeStr

    @classmethod
    def convert_to_bytes(cls, address: bytes | Address | str) -> bytes:
        """
        Converts an address to bytes if it is not already bytes.
        Parameters
        ----------
        address : bytes | Address | str
            The address to convert to bytes
            Can be bytes, Address, or hex string

        Returns
        -------
        bytes
            The address as bytes

        """
        if isinstance(address, bytes):
            return address
        elif isinstance(address, Address):
            return address.bytes
        elif isinstance(address, str):
            return Address.from_hex(address).bytes
        else:
            raise NotAddressError.from_value(address)
