import json
import unittest
from dataclasses import dataclass

from flow_py_sdk import cadence


@dataclass
class _EncodeTestParams:
    name: str
    val: cadence.Value
    expected: str


class TestTx(unittest.TestCase):
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
        self.skipTest("not implemented yet")

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
        self.skipTest("not implemented yet")

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
        self.skipTest("not implemented yet")

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
        self.skipTest("not implemented yet")

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

        resourceArray = _EncodeTestParams(
            "Resources",
            cadence.Array(
                [
                    cadence.Resource([cadence.Int(1)], _foo_resource_type),
                    cadence.Resource([cadence.Int(2)], _foo_resource_type),
                    cadence.Resource([cadence.Int(3)], _foo_resource_type),
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
                resourceArray,
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
                        cadence.Resource([cadence.Int(1)], _foo_resource_type),
                    ),
                    cadence.KeyValuePair(
                        cadence.String("b"),
                        cadence.Resource([cadence.Int(2)], _foo_resource_type),
                    ),
                    cadence.KeyValuePair(
                        cadence.String("c"),
                        cadence.Resource([cadence.Int(3)], _foo_resource_type),
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
        foo_resource_type = cadence.ResourceType(
            _test_location,
            "Foo",
            [
                cadence.Field(
                    "uuid",
                    type(cadence.UInt64),
                ),
                cadence.Field(
                    "bar",
                    type(cadence.Int),
                ),
            ],
        )

        simple_resource = _EncodeTestParams(
            "Simple",
            cadence.Resource([cadence.UInt64(0), cadence.Int(42)], foo_resource_type),
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

        bar_resource_type = cadence.ResourceType(
            _test_location,
            "Bar",
            [
                cadence.Field(
                    "uuid",
                    type(cadence.UInt64),
                ),
                cadence.Field(
                    "x",
                    type(cadence.Int),
                ),
            ],
        )

        foo_resource_type = cadence.ResourceType(
            _test_location,
            "Foo",
            [
                cadence.Field(
                    "uuid",
                    type(cadence.UInt64),
                ),
                cadence.Field(
                    "bar",
                    bar_resource_type,
                ),
            ],
        )

        nested_resource = _EncodeTestParams(
            "Nested resource",
            cadence.Resource(
                [
                    cadence.UInt64(0),
                    cadence.Resource(
                        [cadence.UInt64(0), cadence.Int(42)], bar_resource_type
                    ),
                ],
                foo_resource_type,
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
        simple_struct_type = cadence.StructType(
            _test_location,
            "FooStruct",
            [
                cadence.Field(
                    "a",
                    type(cadence.Int),
                ),
                cadence.Field(
                    "b",
                    type(cadence.String),
                ),
            ],
        )

        simple_struct = _EncodeTestParams(
            "Simple",
            cadence.Struct([cadence.Int(1), cadence.String("foo")], simple_struct_type),
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

        resource_struct_type = cadence.StructType(
            _test_location,
            "FooStruct",
            [
                cadence.Field(
                    "a",
                    type(cadence.String),
                ),
                cadence.Field(
                    "b",
                    _foo_resource_type,
                ),
            ],
        )

        resource_struct = _EncodeTestParams(
            "Resources",
            cadence.Struct(
                [
                    cadence.String("foo"),
                    cadence.Resource([cadence.Int(42)], _foo_resource_type),
                ],
                resource_struct_type,
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


_test_location = cadence.StringLocation("test")

_foo_resource_type = cadence.ResourceType(
    _test_location,
    "Foo",
    [
        cadence.Field(
            "bar",
            type(cadence.Int),
        ),
    ],
)
