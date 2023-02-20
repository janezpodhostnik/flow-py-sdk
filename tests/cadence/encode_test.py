import json
import unittest
from dataclasses import dataclass
from flow_py_sdk import cadence


@dataclass
class _EncodeTestParams:
    name: str
    val: cadence.Value | cadence.Kind
    expected: str


class TestEncode(unittest.TestCase):
    """
    Cadence encoding/decoding tests were adapted from: https://github.com/onflow/cadence/blob/master/encoding/json/encoding_test.go
    """

    def _encodeAndDecodeAll(self, tests: list[_EncodeTestParams]):
        for test in tests:
            with self.subTest(msg=test.name):
                self._encodeAndDecode(test.val, test.expected)

    def _encodeAndDecode(self, val: cadence.Value, expected_json: str):
        actual_json = self._encode(val, expected_json)
        self._decode(actual_json, val)

    def _encode(self, val: cadence.Value, expected_json: str) -> str:
        actual_json = json.dumps(
            val,
            ensure_ascii=False,
            cls=cadence.CadenceJsonEncoder,
            separators=(",", ":"),
        )
        expected = json.loads(expected_json)
        actual = json.loads(actual_json)
        self.assertDictEqual(expected, actual)
        return actual_json

    def _decode(self, actual_json: str, expected_val: cadence.Value):
        cadence_val = json.loads(actual_json, object_hook=cadence.cadence_object_hook)
        self.assertEqual(expected_val, cadence_val)

    def testEncodeOptional(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Nil", cadence.Optional(None), '{"type": "Optional", "value": null}'
                ),
                _EncodeTestParams(
                    "Non-nil",
                    cadence.Optional(cadence.Int(42)),
                    '{"type": "Optional", "value": {"type": "Int", "value": "42"}}',
                ),
            ]
        )

    def testEncodeBool(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "True",
                    cadence.Bool(True),
                    '{"type":"Bool","value":true}',
                ),
                _EncodeTestParams(
                    "False",
                    cadence.Bool(False),
                    '{"type":"Bool","value":false}',
                ),
            ]
        )

    def testEncodeString(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Empty", cadence.String(""), '{"type":"String","value":""}'
                ),
                _EncodeTestParams(
                    "Non-empty",
                    cadence.String("foo"),
                    '{"type":"String","value":"foo"}',
                ),
            ]
        )

    def testEncodeAddress(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Address",
                    cadence.Address(bytes([1, 2, 3, 4, 5])),
                    '{"type":"Address","value":"0x0000000102030405"}',
                ),
            ]
        )

    def testEncodeInt(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Negative",
                    cadence.Int(-42),
                    '{"type": "Int", "value": "-42"}',
                ),
                _EncodeTestParams(
                    "Zero",
                    cadence.Int(0),
                    '{"type": "Int", "value": "0"}',
                ),
                _EncodeTestParams(
                    "Positive",
                    cadence.Int(42),
                    '{"type": "Int", "value": "42"}',
                ),
                _EncodeTestParams(
                    "SmallerThanMinInt256",
                    cadence.Int(
                        -57896044618658097711785492504343953926634992332820282019728792003956564819978
                    ),
                    """{"type": "Int", 
                "value": "-57896044618658097711785492504343953926634992332820282019728792003956564819978"}""",
                ),
                _EncodeTestParams(
                    "LargerThanMaxUInt256",
                    cadence.Int(
                        115792089237316195423570985008687907853269984665640564039457584007913129639945
                    ),
                    """{"type": "Int", 
                "value": "115792089237316195423570985008687907853269984665640564039457584007913129639945"}""",
                ),
            ]
        )

    def testEncodeInt8(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Min",
                    cadence.Int8(-128),
                    '{"type":"Int8","value":"-128"}',
                ),
                _EncodeTestParams(
                    "Zero",
                    cadence.Int8(0),
                    '{"type":"Int8","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Int8(127),
                    '{"type":"Int8","value":"127"}',
                ),
            ]
        )

    def testEncodeInt16(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Min",
                    cadence.Int16(-32768),
                    '{"type":"Int16","value":"-32768"}',
                ),
                _EncodeTestParams(
                    "Zero",
                    cadence.Int16(0),
                    '{"type":"Int16","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Int16(32767),
                    '{"type":"Int16","value":"32767"}',
                ),
            ]
        )

    def testEncodeInt32(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Min",
                    cadence.Int32(-2147483648),
                    '{"type":"Int32","value":"-2147483648"}',
                ),
                _EncodeTestParams(
                    "Zero",
                    cadence.Int32(0),
                    '{"type":"Int32","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Int32(2147483647),
                    '{"type":"Int32","value":"2147483647"}',
                ),
            ]
        )

    def testEncodeInt64(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Min",
                    cadence.Int64(-9223372036854775808),
                    '{"type":"Int64","value":"-9223372036854775808"}',
                ),
                _EncodeTestParams(
                    "Zero",
                    cadence.Int64(0),
                    '{"type":"Int64","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Int64(9223372036854775807),
                    '{"type":"Int64","value":"9223372036854775807"}',
                ),
            ]
        )

    def testEncodeInt128(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Min",
                    cadence.Int128(-170141183460469231731687303715884105728),
                    '{"type":"Int128","value":"-170141183460469231731687303715884105728"}',
                ),
                _EncodeTestParams(
                    "Zero",
                    cadence.Int128(0),
                    '{"type":"Int128","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Int128(170141183460469231731687303715884105727),
                    '{"type":"Int128","value":"170141183460469231731687303715884105727"}',
                ),
            ]
        )

    def testEncodeInt256(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Min",
                    cadence.Int256(
                        -57896044618658097711785492504343953926634992332820282019728792003956564819968
                    ),
                    """{"type":"Int256",
                        "value":"-57896044618658097711785492504343953926634992332820282019728792003956564819968"}""",
                ),
                _EncodeTestParams(
                    "Zero",
                    cadence.Int256(0),
                    '{"type":"Int256","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Int256(
                        57896044618658097711785492504343953926634992332820282019728792003956564819967
                    ),
                    """{"type":"Int256",
                        "value":"57896044618658097711785492504343953926634992332820282019728792003956564819967"}""",
                ),
            ]
        )

    def testEncodeUInt(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.UInt(0),
                    '{"type":"UInt","value":"0"}',
                ),
                _EncodeTestParams(
                    "Positive",
                    cadence.UInt(42),
                    '{"type":"UInt","value":"42"}',
                ),
                _EncodeTestParams(
                    "LargerThanMaxUInt256",
                    cadence.UInt(
                        115792089237316195423570985008687907853269984665640564039457584007913129639945
                    ),
                    """{"type":"UInt",
                        "value":"115792089237316195423570985008687907853269984665640564039457584007913129639945"}""",
                ),
            ]
        )

    def testEncodeUInt8(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.UInt8(0),
                    '{"type":"UInt8","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.UInt8(255),
                    '{"type":"UInt8","value":"255"}',
                ),
            ]
        )

    def testEncodeUInt16(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.UInt16(0),
                    '{"type":"UInt16","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.UInt16(65535),
                    '{"type":"UInt16","value":"65535"}',
                ),
            ]
        )

    def testEncodeUInt32(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.UInt32(0),
                    '{"type":"UInt32","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.UInt32(4294967295),
                    '{"type":"UInt32","value":"4294967295"}',
                ),
            ]
        )

    def testEncodeUInt64(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.UInt64(0),
                    '{"type":"UInt64","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.UInt64(18446744073709551615),
                    '{"type":"UInt64","value":"18446744073709551615"}',
                ),
            ]
        )

    def testEncodeUInt128(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.UInt128(0),
                    '{"type":"UInt128","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.UInt128(340282366920938463463374607431768211455),
                    '{"type":"UInt128","value":"340282366920938463463374607431768211455"}',
                ),
            ]
        )

    def testEncodeUInt256(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.UInt256(0),
                    '{"type":"UInt256","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.UInt256(
                        115792089237316195423570985008687907853269984665640564039457584007913129639935
                    ),
                    """{"type":"UInt256",
                        "value":"115792089237316195423570985008687907853269984665640564039457584007913129639935"}""",
                ),
            ]
        )

    def testEncodeWord8(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.Word8(0),
                    '{"type":"Word8","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Word8(255),
                    '{"type":"Word8","value":"255"}',
                ),
            ]
        )

    def testEncodeWord16(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.Word16(0),
                    '{"type":"Word16","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Word16(65535),
                    '{"type":"Word16","value":"65535"}',
                ),
            ]
        )

    def testEncodeWord32(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.Word32(0),
                    '{"type":"Word32","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Word32(4294967295),
                    '{"type":"Word32","value":"4294967295"}',
                ),
            ]
        )

    def testEncodeWord64(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.Word64(0),
                    '{"type":"Word64","value":"0"}',
                ),
                _EncodeTestParams(
                    "Max",
                    cadence.Word64(18446744073709551615),
                    '{"type":"Word64","value":"18446744073709551615"}',
                ),
            ]
        )

    def testEncodeFix64(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.Fix64(0),
                    '{"type":"Fix64","value":"0.00000000"}',
                ),
                _EncodeTestParams(
                    "789.00123010",
                    cadence.Fix64(78_900_123_010),
                    '{"type":"Fix64","value":"789.00123010"}',
                ),
                _EncodeTestParams(
                    "1234.056",
                    cadence.Fix64(123_405_600_000),
                    '{"type":"Fix64","value":"1234.05600000"}',
                ),
                _EncodeTestParams(
                    "-12345.006789",
                    cadence.Fix64(-1_234_500_678_900),
                    '{"type":"Fix64","value":"-12345.00678900"}',
                ),
            ]
        )

    def testEncodeUFix64(self):
        self._encodeAndDecodeAll(
            [
                _EncodeTestParams(
                    "Zero",
                    cadence.UFix64(0),
                    '{"type":"UFix64","value":"0.00000000"}',
                ),
                _EncodeTestParams(
                    "789.00123010",
                    cadence.UFix64(78_900_123_010),
                    '{"type":"UFix64","value":"789.00123010"}',
                ),
                _EncodeTestParams(
                    "1234.056",
                    cadence.UFix64(123_405_600_000),
                    '{"type":"UFix64","value":"1234.05600000"}',
                ),
            ]
        )

    def testEncodeArray(self):
        empty_array = _EncodeTestParams(
            "Empty",
            cadence.Array([]),
            '{"type":"Array","value":[]}',
        )
        int_array = _EncodeTestParams(
            "Integers",
            cadence.Array(
                [
                    cadence.Int(1),
                    cadence.Int(2),
                    cadence.Int(3),
                ]
            ),
            """{"type":"Array",
                "value":[{"type":"Int","value":"1"},{"type":"Int","value":"2"},{"type":"Int","value":"3"}]}""",
        )
        resource_array = _EncodeTestParams(
            "Resources",
            cadence.Array(
                [
                    cadence.Resource("S.test.Foo", [("bar", cadence.Int(1))]),
                    cadence.Resource("S.test.Foo", [("bar", cadence.Int(2))]),
                    cadence.Resource("S.test.Foo", [("bar", cadence.Int(3))]),
                ]
            ),
            """{"type":"Array","value":[
                {"type":"Resource","value":{"id":"S.test.Foo",
                    "fields":[{"name":"bar","value":{"type":"Int","value":"1"}}]}},
                {"type":"Resource","value":{"id":"S.test.Foo",
                    "fields":[{"name":"bar","value":{"type":"Int","value":"2"}}]}},
                {"type":"Resource","value":{"id":"S.test.Foo",
                    "fields":[{"name":"bar","value":{"type":"Int","value":"3"}}]}}
            ]}""",
        )
        self._encodeAndDecodeAll(
            [
                empty_array,
                int_array,
                resource_array,
            ]
        )

    def testEncodeDictionary(self):
        simple_dict = _EncodeTestParams(
            "Simple",
            cadence.Dictionary(
                [
                    cadence.KeyValuePair(
                        cadence.String("a"),
                        cadence.Int(1),
                    ),
                    cadence.KeyValuePair(
                        cadence.String("b"),
                        cadence.Int(2),
                    ),
                    cadence.KeyValuePair(
                        cadence.String("c"),
                        cadence.Int(3),
                    ),
                ]
            ),
            """{"type":"Dictionary","value":[
                {"key":{"type":"String","value":"a"},"value":{"type":"Int","value":"1"}},
                {"key":{"type":"String","value":"b"},"value":{"type":"Int","value":"2"}},
                {"key":{"type":"String","value":"c"},"value":{"type":"Int","value":"3"}}
            ]}""",
        )
        nested_dict = _EncodeTestParams(
            "Nested",
            cadence.Dictionary(
                [
                    cadence.KeyValuePair(
                        cadence.String("a"),
                        cadence.Dictionary(
                            [
                                cadence.KeyValuePair(
                                    cadence.String("1"),
                                    cadence.Int(1),
                                ),
                            ]
                        ),
                    ),
                    cadence.KeyValuePair(
                        cadence.String("b"),
                        cadence.Dictionary(
                            [
                                cadence.KeyValuePair(
                                    cadence.String("2"),
                                    cadence.Int(2),
                                ),
                            ]
                        ),
                    ),
                    cadence.KeyValuePair(
                        cadence.String("c"),
                        cadence.Dictionary(
                            [
                                cadence.KeyValuePair(
                                    cadence.String("3"),
                                    cadence.Int(3),
                                ),
                            ]
                        ),
                    ),
                ]
            ),
            """
            {
                "type": "Dictionary",
                "value": [
                {
                  "key": { "type": "String", "value": "a" },
                  "value": {
                    "type": "Dictionary",
                    "value": [
                      {
                        "key": { "type": "String", "value": "1" },
                        "value": { "type": "Int", "value": "1" }
                      }
                    ]
                  }
                },
                {
                  "key": { "type": "String", "value": "b" },
                  "value": {
                    "type": "Dictionary",
                    "value": [
                      {
                        "key": { "type": "String", "value": "2" },
                        "value": { "type": "Int", "value": "2" }
                      }
                    ]
                  }
                },
                {
                  "key": { "type": "String", "value": "c" },
                  "value": {
                    "type": "Dictionary",
                    "value": [
                      {
                        "key": { "type": "String", "value": "3" },
                        "value": { "type": "Int", "value": "3" }
                      }
                    ]
                  }
                }
                ]
            }
            """,
        )
        resource_dict = _EncodeTestParams(
            "Resources",
            cadence.Dictionary(
                [
                    cadence.KeyValuePair(
                        cadence.String("a"),
                        cadence.Resource("S.test.Foo", [("bar", cadence.Int(1))]),
                    ),
                    cadence.KeyValuePair(
                        cadence.String("b"),
                        cadence.Resource("S.test.Foo", [("bar", cadence.Int(2))]),
                    ),
                    cadence.KeyValuePair(
                        cadence.String("c"),
                        cadence.Resource("S.test.Foo", [("bar", cadence.Int(3))]),
                    ),
                ]
            ),
            """
                {
                  "type": "Dictionary",
                  "value": [
                    {
                      "key": { "type": "String", "value": "a" },
                      "value": {
                        "type": "Resource",
                        "value": {
                          "id": "S.test.Foo",
                          "fields": [
                            { "name": "bar", "value": { "type": "Int", "value": "1" } }
                          ]
                        }
                      }
                    },
                    {
                      "key": { "type": "String", "value": "b" },
                      "value": {
                        "type": "Resource",
                        "value": {
                          "id": "S.test.Foo",
                          "fields": [
                            { "name": "bar", "value": { "type": "Int", "value": "2" } }
                          ]
                        }
                      }
                    },
                    {
                      "key": { "type": "String", "value": "c" },
                      "value": {
                        "type": "Resource",
                        "value": {
                          "id": "S.test.Foo",
                          "fields": [
                            { "name": "bar", "value": { "type": "Int", "value": "3" } }
                          ]
                        }
                      }
                    }
                  ]
                }
            """,
        )
        self._encodeAndDecodeAll(
            [
                simple_dict,
                nested_dict,
                resource_dict,
            ]
        )

    def testEncodeResource(self):
        simple_resource = _EncodeTestParams(
            "Simple",
            cadence.Resource(
                "S.test.Foo",
                [
                    ("uuid", cadence.UInt64(0)),
                    ("bar", cadence.Int(42)),
                ],
            ),
            """
            {
              "type": "Resource",
              "value": {
                "id": "S.test.Foo",
                "fields": [
                  { "name": "uuid", "value": { "type": "UInt64", "value": "0" } },
                  { "name": "bar", "value": { "type": "Int", "value": "42" } }
                ]
              }
            }
            """,
        )
        nested_resource = _EncodeTestParams(
            "Nested resource",
            cadence.Resource(
                "S.test.Foo",
                [
                    ("uuid", cadence.UInt64(0)),
                    (
                        "bar",
                        cadence.Resource(
                            "S.test.Bar",
                            [("uuid", cadence.UInt64(0)), ("x", cadence.Int(42))],
                        ),
                    ),
                ],
            ),
            """
            {
              "type": "Resource",
              "value": {
                "id": "S.test.Foo",
                "fields": [
                  { "name": "uuid", "value": { "type": "UInt64", "value": "0" } },
                  {
                    "name": "bar",
                    "value": {
                      "type": "Resource",
                      "value": {
                        "id": "S.test.Bar",
                        "fields": [
                          { "name": "uuid", "value": { "type": "UInt64", "value": "0" } },
                          { "name": "x", "value": { "type": "Int", "value": "42" } }
                        ]
                      }
                    }
                  }
                ]
              }
            }
            """,
        )
        self._encodeAndDecodeAll([simple_resource, nested_resource])

    def testEncodeStruct(self):
        simple_struct = _EncodeTestParams(
            "Simple",
            cadence.Struct(
                "S.test.FooStruct",
                [("a", cadence.Int(1)), ("b", cadence.String("foo"))],
            ),
            """
            {
              "type": "Struct",
              "value": {
                "id": "S.test.FooStruct",
                "fields": [
                  { "name": "a", "value": { "type": "Int", "value": "1" } },
                  { "name": "b", "value": { "type": "String", "value": "foo" } }
                ]
              }
            }
            """,
        )
        resource_struct = _EncodeTestParams(
            "Resources",
            cadence.Struct(
                "S.test.FooStruct",
                [
                    ("a", cadence.String("foo")),
                    ("b", cadence.Resource("S.test.Foo", [("bar", cadence.Int(42))])),
                ],
            ),
            """
            {
              "type": "Struct",
              "value": {
                "id": "S.test.FooStruct",
                "fields": [
                  { "name": "a", "value": { "type": "String", "value": "foo" } },
                  {
                    "name": "b",
                    "value": {
                      "type": "Resource",
                      "value": {
                        "id": "S.test.Foo",
                        "fields": [
                          { "name": "bar", "value": { "type": "Int", "value": "42" } }
                        ]
                      }
                    }
                  }
                ]
              }
            }
            """,
        )
        self._encodeAndDecodeAll([simple_struct, resource_struct])

    def testEncodeEvent(self):
        simple_event = _EncodeTestParams(
            "Simple",
            cadence.Event(
                "S.test.FooEvent", [("a", cadence.Int(1)), ("b", cadence.String("foo"))]
            ),
            """
            {
              "type": "Event",
              "value": {
                "id": "S.test.FooEvent",
                "fields": [
                  { "name": "a", "value": { "type": "Int", "value": "1" } },
                  { "name": "b", "value": { "type": "String", "value": "foo" } }
                ]
              }
            }
            """,
        )
        resource_event = _EncodeTestParams(
            "Resources",
            cadence.Event(
                "S.test.FooEvent",
                [
                    ("a", cadence.String("foo")),
                    ("b", cadence.Resource("S.test.Foo", [("bar", cadence.Int(42))])),
                ],
            ),
            """
            {
              "type": "Event",
              "value": {
                "id": "S.test.FooEvent",
                "fields": [
                  { "name": "a", "value": { "type": "String", "value": "foo" } },
                  {
                    "name": "b",
                    "value": {
                      "type": "Resource",
                      "value": {
                        "id": "S.test.Foo",
                        "fields": [
                          { "name": "bar", "value": { "type": "Int", "value": "42" } }
                        ]
                      }
                    }
                  }
                ]
              }
            }
            """,
        )
        self._encodeAndDecodeAll([simple_event, resource_event])

    def testEncodeContract(self):
        simple_contract = _EncodeTestParams(
            "Simple",
            cadence.Contract(
                "S.test.FooContract",
                [
                    ("a", cadence.Int(1)),
                    ("b", cadence.String("foo")),
                ],
            ),
            """
            {
              "type": "Contract",
              "value": {
                "id": "S.test.FooContract",
                "fields": [
                  { "name": "a", "value": { "type": "Int", "value": "1" } },
                  { "name": "b", "value": { "type": "String", "value": "foo" } }
                ]
              }
            }
            """,
        )
        resource_contract = _EncodeTestParams(
            "Resources",
            cadence.Contract(
                "S.test.FooContract",
                [
                    ("a", cadence.String("foo")),
                    ("b", cadence.Resource("S.test.Foo", [("bar", cadence.Int(42))])),
                ],
            ),
            """
            {
              "type": "Contract",
              "value": {
                "id": "S.test.FooContract",
                "fields": [
                  { "name": "a", "value": { "type": "String", "value": "foo" } },
                  {
                    "name": "b",
                    "value": {
                      "type": "Resource",
                      "value": {
                        "id": "S.test.Foo",
                        "fields": [
                          { "name": "bar", "value": { "type": "Int", "value": "42" } }
                        ]
                      }
                    }
                  }
                ]
              }
            }
            """,
        )
        self._encodeAndDecodeAll([simple_contract, resource_contract])

    def testEncodeType(self):
        static_type = _EncodeTestParams(
            "Static Type",
            cadence.TypeValue(
                cadence.IntKind(),
            ),
            """
            {
              "type": "Type",
              "value": {
                "staticType": {
                  "kind": "Int"
                }
              }
            }
            """,
        )
        self._encodeAndDecodeAll([static_type])

    def testEncodeCapability(self):
        capability = _EncodeTestParams(
            "Capability",
            cadence.Capability(
                cadence.Path("public", "someInteger"),
                cadence.Address.from_hex("0x0000000000000001"),
                cadence.IntKind(),
            ),
            """
            {
              "type": "Capability",
              "value": {
                "path": {
                  "type": "Path",
                  "value": {
                    "domain": "public",
                    "identifier": "someInteger"
                  }
                },
                "address": "0x0000000000000001",
                "borrowType": {
                  "kind": "Int"
                }
              }
            }
            """,
        )
        self._encodeAndDecodeAll([capability])

    def testEncodeFunction(self):
        capability = _EncodeTestParams(
            "Function",
            cadence.Function(
                cadence.FunctionKind(
                    "fun():Void",
                    [],
                    cadence.VoidKind(),
                ),
            ),
            """
            {
              "type": "Function",
              "value": {
                "functionType": {
                  "kind": "Function",
                  "typeID": "fun():Void",
                  "parameters": [],
                  "return": {
                    "kind": "Void"
                  }
                }
              }
            }
            """,
        )
        self._encodeAndDecodeAll([capability])

    def testEncodeSimpleKind(self):
        simple_kind = _EncodeTestParams(
            "Simple Kind",
            cadence.UInt8Kind(),
            """
            {
              "kind": "UInt8"
            }
            """,
        )
        self._encodeAndDecodeAll([simple_kind])

    def testEncodeOptionalKind(self):
        optional_kind = _EncodeTestParams(
            "Optional Kind",
            cadence.OptionalKind(cadence.StringKind()),
            """
            {
              "kind": "Optional",
              "type": {
                "kind": "String"
              }
            }
            """,
        )
        self._encodeAndDecodeAll([optional_kind])

    def testVariableSizedArrayKind(self):
        kind = _EncodeTestParams(
            "VariableSizedArray Kind",
            cadence.VariableSizedArrayKind(cadence.StringKind()),
            """
            {
              "kind": "VariableSizedArray",
              "type": {
                "kind": "String"
              }
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testConstSizedArrayKind(self):
        kind = _EncodeTestParams(
            "ConstantSizedArray Kind",
            cadence.ConstantSizedArrayKind(cadence.StringKind(), 3),
            """
            {
              "kind": "ConstantSizedArray",
              "type": {
                "kind": "String"
              },
              "size":3
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testDictionaryKind(self):
        kind = _EncodeTestParams(
            "Dictionary Kind",
            cadence.DictionaryKind(cadence.StringKind(), cadence.UInt16Kind()),
            """
            {
              "kind": "Dictionary",
              "key": {
                "kind": "String"
              }, 
              "value": {
                "kind": "UInt16"
              }
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testCompositeKind(self):
        kind = _EncodeTestParams(
            "Resource Kind",
            cadence.ResourceKind(
                "0x3.GreatContract.GreatNFT",
                [
                    [
                        cadence.ParameterKind(
                            "foo",
                            "bar",
                            cadence.StringKind(),
                        )
                    ]
                ],
                [
                    cadence.FieldKind(
                        "foo",
                        cadence.StringKind(),
                    ),
                ],
            ),
            """
            {
              "kind": "Resource",
              "type": "",
              "typeID": "0x3.GreatContract.GreatNFT",
              "initializers":[
                [
                  {
                    "label": "foo",
                    "id": "bar",
                    "type": {
                      "kind": "String"
                    }
                  }
                ]
              ],
              "fields": [
                {
                  "id": "foo",
                  "type": {
                    "kind": "String"
                  }
                }
              ]
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testFunctionKind(self):
        kind = _EncodeTestParams(
            "Function Kind",
            cadence.FunctionKind(
                "foo",
                [
                    cadence.ParameterKind(
                        "foo",
                        "bar",
                        cadence.StringKind(),
                    )
                ],
                cadence.StringKind(),
            ),
            """
            {
              "kind": "Function",
              "typeID": "foo",
              "parameters": [
                {
                  "label": "foo",
                  "id": "bar",
                  "type": {
                    "kind": "String"
                  }
                } 
              ], 
              "return": {
                "kind": "String"
              }
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testReferenceKind(self):
        kind = _EncodeTestParams(
            "Reference Kind",
            cadence.ReferenceKind(
                True,
                cadence.StringKind(),
            ),
            """
            {
              "kind": "Reference",
              "authorized": true,
              "type": {
                "kind": "String"
              }
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testRestrictedKind(self):
        kind = _EncodeTestParams(
            "Restricted Kind",
            cadence.RestrictedKind(
                "0x3.GreatContract.GreatNFT",
                cadence.AnyResourceKind(),
                [
                    cadence.ResourceInterfaceKind(
                        "0x1.FungibleToken.Receiver",
                        [],
                        [
                            cadence.FieldKind(
                                "uuid",
                                cadence.UInt64Kind(),
                            )
                        ],
                    )
                ],
            ),
            """
            {
              "kind": "Restriction",
              "typeID": "0x3.GreatContract.GreatNFT",
              "type": {
                "kind": "AnyResource"
              },
              "restrictions": [
                {
                  "kind": "ResourceInterface",
                  "typeID": "0x1.FungibleToken.Receiver",
                  "initializers": [],
                  "fields": [
                    {
                      "id": "uuid",
                      "type": {
                        "kind": "UInt64"
                      }
                    }
                  ],
                  "type": ""
                }
              ]
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testCapabilityKind(self):
        kind = _EncodeTestParams(
            "Capability Kind",
            cadence.CapabilityKind(
                cadence.ReferenceKind(
                    True,
                    cadence.StringKind(),
                )
            ),
            """
            {
              "kind": "Capability",
              "type": {
                "kind": "Reference",
                "authorized": true,
                "type": {
                  "kind": "String"
                }
              }
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testEnumKind(self):
        kind = _EncodeTestParams(
            "Enum Kind",
            cadence.EnumKind(
                "0x3.GreatContract.GreatEnum",
                cadence.StringKind(),
                [
                    cadence.FieldKind(
                        "rawValue",
                        cadence.StringKind(),
                    )
                ],
            ),
            """
            {
              "kind": "Enum",
              "type": {
                "kind": "String"
              },
              "typeID": "0x3.GreatContract.GreatEnum",
              "initializers":[],
              "fields": [
                {
                  "id": "rawValue",
                  "type": {
                    "kind": "String"
                  }
                }
              ]
            }
            """,
        )
        self._encodeAndDecodeAll([kind])

    def testStorefrontEvent(self):
        self.maxDiff = None
        event = _EncodeTestParams(
            "StorefrontEvent",
            cadence.Event(
                "A.4eb8a10cb9f87357.NFTStorefrontV2.ListingAvailable",
                [
                    (
                        "storefrontAddress",
                        cadence.Address.from_hex("0xe037c7e7cd998a9c"),
                    ),
                    ("listingResourceID", cadence.UInt64(897392501)),
                    (
                        "nftType",
                        cadence.TypeValue(
                            cadence.ResourceKind(
                                "A.87ca73a41bb50ad5.Golazos.NFT",
                                [],
                                [
                                    cadence.FieldKind("uuid", cadence.UInt64Kind()),
                                    cadence.FieldKind("id", cadence.UInt64Kind()),
                                    cadence.FieldKind(
                                        "editionID", cadence.UInt64Kind()
                                    ),
                                    cadence.FieldKind(
                                        "serialNumber", cadence.UInt64Kind()
                                    ),
                                    cadence.FieldKind(
                                        "mintingDate", cadence.UFix64Kind()
                                    ),
                                ],
                            )
                        ),
                    ),
                    ("nftUUID", cadence.UInt64(885861011)),
                    ("nftID", cadence.UInt64(885861011)),
                    (
                        "salePaymentVaultType",
                        cadence.TypeValue(
                            cadence.ResourceKind(
                                "A.ead892083b3e2c6c.DapperUtilityCoin.Vault",
                                [],
                                [
                                    cadence.FieldKind("uuid", cadence.UInt64Kind()),
                                    cadence.FieldKind("balance", cadence.UFix64Kind()),
                                ],
                            )
                        ),
                    ),
                    ("salePrice", cadence.UFix64(200000000)),
                    (
                        "customID",
                        cadence.Optional(cadence.String("DAPPER_MARKETPLACE")),
                    ),
                    ("commissionAmount", cadence.UFix64(0)),
                    (
                        "commissionReceivers",
                        cadence.Optional(
                            cadence.Array(
                                [
                                    cadence.Address.from_hex("0x87ca73a41bb50ad5"),
                                ]
                            )
                        ),
                    ),
                    ("expiry", cadence.UInt64(33233716780)),
                ],
            ),
            """
            {
              "value": {
                "id": "A.4eb8a10cb9f87357.NFTStorefrontV2.ListingAvailable",
                "fields": [
                  {
                    "value": {
                      "value": "0xe037c7e7cd998a9c",
                      "type": "Address"
                    },
                    "name": "storefrontAddress"
                  },
                  {
                    "value": {
                      "value": "897392501",
                      "type": "UInt64"
                    },
                    "name": "listingResourceID"
                  },
                  {
                    "value": {
                      "value": {
                        "staticType": {
                          "type": "",
                          "kind": "Resource",
                          "typeID": "A.87ca73a41bb50ad5.Golazos.NFT",
                          "fields": [
                            {
                              "type": {
                                "kind": "UInt64"
                              },
                              "id": "uuid"
                            },
                            {
                              "type": {
                                "kind": "UInt64"
                              },
                              "id": "id"
                            },
                            {
                              "type": {
                                "kind": "UInt64"
                              },
                              "id": "editionID"
                            },
                            {
                              "type": {
                                "kind": "UInt64"
                              },
                              "id": "serialNumber"
                            },
                            {
                              "type": {
                                "kind": "UFix64"
                              },
                              "id": "mintingDate"
                            }
                          ],
                          "initializers": []
                        }
                      },
                      "type": "Type"
                    },
                    "name": "nftType"
                  },
                  {
                    "value": {
                      "value": "885861011",
                      "type": "UInt64"
                    },
                    "name": "nftUUID"
                  },
                  {
                    "value": {
                      "value": "885861011",
                      "type": "UInt64"
                    },
                    "name": "nftID"
                  },
                  {
                    "value": {
                      "value": {
                        "staticType": {
                          "type": "",
                          "kind": "Resource",
                          "typeID": "A.ead892083b3e2c6c.DapperUtilityCoin.Vault",
                          "fields": [
                            {
                              "type": {
                                "kind": "UInt64"
                              },
                              "id": "uuid"
                            },
                            {
                              "type": {
                                "kind": "UFix64"
                              },
                              "id": "balance"
                            }
                          ],
                          "initializers": []
                        }
                      },
                      "type": "Type"
                    },
                    "name": "salePaymentVaultType"
                  },
                  {
                    "value": {
                      "value": "2.00000000",
                      "type": "UFix64"
                    },
                    "name": "salePrice"
                  },
                  {
                    "value": {
                      "value": {
                        "value": "DAPPER_MARKETPLACE",
                        "type": "String"
                      },
                      "type": "Optional"
                    },
                    "name": "customID"
                  },
                  {
                    "value": {
                      "value": "0.00000000",
                      "type": "UFix64"
                    },
                    "name": "commissionAmount"
                  },
                  {
                    "value": {
                      "value": {
                        "value": [
                          {
                            "value": "0x87ca73a41bb50ad5",
                            "type": "Address"
                          }
                        ],
                        "type": "Array"
                      },
                      "type": "Optional"
                    },
                    "name": "commissionReceivers"
                  },
                  {
                    "value": {
                      "value": "33233716780",
                      "type": "UInt64"
                    },
                    "name": "expiry"
                  }
                ]
              },
              "type": "Event"
            }
            """,
        )
        self._encodeAndDecodeAll([event])
