from unittest import TestCase

from flow_py_sdk.cadence import Address
from flow_py_sdk.exceptions import NotAddressError


class TestAddress(TestCase):
    def test_convert_to_bytes(self):
        with self.subTest(msg="Pass address as bytes"):
            address = Address.from_hex("0x01")
            self.assertEqual(address.bytes, Address.convert_to_bytes(address.bytes))

        with self.subTest(msg="Pass address as Address"):
            address = Address.from_hex("0x01")
            self.assertEqual(address.bytes, Address.convert_to_bytes(address))

        with self.subTest(msg="Pass address as hex string"):
            address = Address.from_hex("0x01")
            self.assertEqual(address.bytes, Address.convert_to_bytes(address.hex()))

        with self.subTest(msg="Pass address as unknown"):
            with self.assertRaises(NotAddressError):
                Address.convert_to_bytes(1)
