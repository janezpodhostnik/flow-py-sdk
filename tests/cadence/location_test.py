import unittest
from dataclasses import dataclass

from flow_py_sdk import cadence
from flow_py_sdk.exceptions import CadenceEncodingError


class TestLocation(unittest.TestCase):
    def testLocationId(self):
        location_str = "0102"
        type_id_str = "something"

        @dataclass
        class TestCase:
            location: cadence.Location
            expected_id: str
            expected_type_id: str

            def __init__(self, loc, expected_id, expected_type_id) -> None:
                super().__init__()
                self.location = loc
                self.expected_id = expected_id
                self.expected_type_id = expected_type_id

        cases: list[TestCase] = [
            TestCase(
                cadence.ScriptLocation(location_str),
                f"s.{location_str}",
                f"s.{location_str}.{type_id_str}",
            ),
            TestCase(
                cadence.AddressLocation(cadence.Address.from_hex("0x01"), location_str),
                f"A.0000000000000001.{location_str}",
                f"A.0000000000000001.{type_id_str}",
            ),
            TestCase(
                cadence.StringLocation(location_str),
                f"S.{location_str}",
                f"S.{location_str}.{type_id_str}",
            ),
            TestCase(cadence.FlowLocation(), "flow", f"flow.{type_id_str}"),
        ]

        for case in cases:
            with self.subTest(msg=f"{case} id"):
                location_id = case.location.id()
                self.assertEqual(case.expected_id, location_id)

            with self.subTest(msg=f"{case} type_id"):
                location_id = case.location.type_id(type_id_str)
                self.assertEqual(case.expected_type_id, location_id)

    def testDecodeAddressLocation(self):
        with self.subTest(msg=f"missing prefix"):
            with self.assertRaises(CadenceEncodingError):
                cadence.AddressLocation.decode("")

        with self.subTest(msg=f"missing location"):
            with self.assertRaises(CadenceEncodingError):
                cadence.AddressLocation.decode("A")

        with self.subTest(msg=f"missing qualified identifier"):
            with self.assertRaises(CadenceEncodingError):
                cadence.AddressLocation.decode("A.0000000000000001")

        with self.subTest(msg=f"invalid prefix"):
            with self.assertRaises(CadenceEncodingError):
                cadence.AddressLocation.decode("s.0000000000000001.t")

        with self.subTest(msg=f"decode"):
            location, identifier = cadence.AddressLocation.decode(
                "A.0000000000000001.test"
            )
            self.assertEqual(
                cadence.AddressLocation(
                    cadence.Address.from_hex("0x0000000000000001"), "test"
                ),
                location,
            )
            self.assertEqual(
                "test",
                identifier,
            )

    def testDecodeScriptLocation(self):
        with self.subTest(msg=f"missing prefix"):
            with self.assertRaises(CadenceEncodingError):
                cadence.ScriptLocation.decode("")

        with self.subTest(msg=f"missing location"):
            with self.assertRaises(CadenceEncodingError):
                cadence.ScriptLocation.decode("s")

        with self.subTest(msg=f"missing qualified identifier"):
            with self.assertRaises(CadenceEncodingError):
                cadence.ScriptLocation.decode("s.test")

        with self.subTest(msg=f"invalid prefix"):
            with self.assertRaises(CadenceEncodingError):
                cadence.ScriptLocation.decode("A.test.t")

        with self.subTest(msg=f"decode"):
            location, identifier = cadence.ScriptLocation.decode("s.test.T")
            self.assertEqual(
                cadence.ScriptLocation("test"),
                location,
            )
            self.assertEqual(
                "T",
                identifier,
            )

    def testDecodeStringLocation(self):
        with self.subTest(msg=f"missing prefix"):
            with self.assertRaises(CadenceEncodingError):
                cadence.StringLocation.decode("")

        with self.subTest(msg=f"missing location"):
            with self.assertRaises(CadenceEncodingError):
                cadence.StringLocation.decode("S")

        with self.subTest(msg=f"missing qualified identifier"):
            with self.assertRaises(CadenceEncodingError):
                cadence.StringLocation.decode("S.test")

        with self.subTest(msg=f"invalid prefix"):
            with self.assertRaises(CadenceEncodingError):
                cadence.StringLocation.decode("A.test.t")

        with self.subTest(msg=f"decode"):
            location, identifier = cadence.StringLocation.decode("S.test.T")
            self.assertEqual(
                cadence.StringLocation("test"),
                location,
            )
            self.assertEqual(
                "T",
                identifier,
            )

    def testDecodeFlowLocation(self):
        with self.subTest(msg=f"missing prefix"):
            with self.assertRaises(CadenceEncodingError):
                cadence.FlowLocation.decode("")

        with self.subTest(msg=f"missing location"):
            with self.assertRaises(CadenceEncodingError):
                cadence.FlowLocation.decode("flow")

        with self.subTest(msg=f"invalid prefix"):
            with self.assertRaises(CadenceEncodingError):
                cadence.FlowLocation.decode("A.test")

        with self.subTest(msg=f"decode"):
            location, identifier = cadence.FlowLocation.decode("flow.test")
            self.assertEqual(
                cadence.FlowLocation(),
                location,
            )
            self.assertEqual(
                "test",
                identifier,
            )
