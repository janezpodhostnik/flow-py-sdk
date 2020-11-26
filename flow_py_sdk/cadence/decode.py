from typing import Any

from flow_py_sdk.cadence.types import decode


def cadence_object_hook(obj: [dict[Any, Any]]) -> Any:
    return decode(obj)

    #
    # if t == _voidTypeStr:
    #     return Void()
    #
    # v = obj[_valueKey]
    #
    # if t == _optionalTypeStr:
    #     if v is None:
    #         return Optional(None)
    #     return Optional(v)
    #
    # if t == _boolTypeStr:
    #     return Bool(bool(strtobool(v)))
    #
    # if t == _stringTypeStr:
    #     return String(str(v))
    #
    # if t == _addressTypeStr:
    #     addr = str(v)
    #     if addr[:2] != "0x":
    #         raise Exception()  # TODO
    #     addr_bytes = bytes.fromhex(addr[2:])
    #     return Address(addr_bytes)
    #
    # if t == _intTypeStr:
    #     return Int(int(str(v)))
    #
    # if t == _int8TypeStr:
    #     return Int8(int(str(v)))
    #
    # if t == _int16TypeStr:
    #     return Int16(int(str(v)))
    #
    # if t == _int32TypeStr:
    #     return Int32(int(str(v)))
    #
    # if t == _int64TypeStr:
    #     return Int64(int(str(v)))
    #
    # if t == _int128TypeStr:
    #     return Int128(int(str(v)))
    #
    # if t == _int256TypeStr:
    #     return Int256(int(str(v)))
    #
    # if t == _uintTypeStr:
    #     return UInt(int(str(v)))
    #
    # if t == _uint8TypeStr:
    #     return UInt8(int(str(v)))
    #
    # if t == _uint16TypeStr:
    #     return UInt16(int(str(v)))
    #
    # if t == _uint32TypeStr:
    #     return UInt32(int(str(v)))
    #
    # if t == _uint64TypeStr:
    #     return UInt64(int(str(v)))
    #
    # if t == _uint128TypeStr:
    #     return UInt128(int(str(v)))
    #
    # if t == _uint256TypeStr:
    #     return UInt256(int(str(v)))
    #
    # if t == _word8TypeStr:
    #     return Word8(int(str(v)))
    #
    # if t == _word16TypeStr:
    #     return Word16(int(str(v)))
    #
    # if t == _word32TypeStr:
    #     return Word32(int(str(v)))
    #
    # if t == _word64TypeStr:
    #     return Word64(int(str(v)))
    #
    # if t == _fix64TypeStr:
    #     return Fix64.parse_string(str(v))
    #
    # if t == _ufix64TypeStr:
    #     return UFix64.parse_string(str(v))
    #
    # if t == _arrayTypeStr:
    #     return Array([x for x in v])
    #
    # if t == _dictionaryTypeStr:
    #     return Dictionary([KeyValuePair(x[_keyKey], x[_valueKey]) for x in v])
    #
    # if t == _resourceTypeStr:
    #     return Dictionary([KeyValuePair(x[_keyKey], x[_valueKey]) for x in v])


