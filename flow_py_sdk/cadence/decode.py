import json
from distutils.util import strtobool
from typing import Callable, Dict, Any, Tuple

from .types import *

_typeKey = "type"
_valueKey = "value"
_keyKey = "key"
_nameKey = "name"
_fieldsKey = "fields"
_idKey = "id"
_targetPathKey = "targetPath"
_borrowTypeKey = "borrowType"
_domainKey = "domain"
_identifierKey = "identifier"
_staticTypeKey = "staticType"
_addressKey = "address"
_pathKey = "path"

_voidTypeStr = "Void"
_optionalTypeStr = "Optional"
_boolTypeStr = "Bool"
_stringTypeStr = "String"
_addressTypeStr = "Address"
_intTypeStr = "Int"
_int8TypeStr = "Int8"
_int16TypeStr = "Int16"
_int32TypeStr = "Int32"
_int64TypeStr = "Int64"
_int128TypeStr = "Int128"
_int256TypeStr = "Int256"
_uintTypeStr = "UInt"
_uint8TypeStr = "UInt8"
_uint16TypeStr = "UInt16"
_uint32TypeStr = "UInt32"
_uint64TypeStr = "UInt64"
_uint128TypeStr = "UInt128"
_uint256TypeStr = "UInt256"
_word8TypeStr = "Word8"
_word16TypeStr = "Word16"
_word32TypeStr = "Word32"
_word64TypeStr = "Word64"
_fix64TypeStr = "Fix64"
_ufix64TypeStr = "UFix64"
_arrayTypeStr = "Array"
_dictionaryTypeStr = "Dictionary"
_structTypeStr = "Struct"
_resourceTypeStr = "Resource"
_eventTypeStr = "Event"
_contractTypeStr = "Contract"
_linkTypeStr = "Link"
_pathTypeStr = "Path"
_typeTypeStr = "Type"
_capabilityTypeStr = "Capability"


def cadence_object_hook(obj: [Dict[Any, Any]])-> Any:
    t = obj['type']
    v = obj['value']

    if t == _voidTypeStr:
        return Void()

    if t == _optionalTypeStr:
        if v is None:
            return Optional(None)
        return Optional(v)

    if t == _boolTypeStr:
        return Bool(bool(strtobool(v)))

    if t == _stringTypeStr:
        return String(str(v))

    if t == _addressTypeStr:
        addr = str(v)
        if addr[:2] != "0x":
            raise Exception()  # TODO
        addr_bytes = bytes.fromhex(addr[2:])
        return Address(addr_bytes)

    if t == _intTypeStr:
        return Int(int(str(v)))

    if t == _int8TypeStr:
        return Int8(int(str(v)))

    if t == _int16TypeStr:
        return Int16(int(str(v)))

    if t == _int32TypeStr:
        return Int32(int(str(v)))

    if t == _int64TypeStr:
        return Int64(int(str(v)))

    if t == _int128TypeStr:
        return Int128(int(str(v)))

    if t == _int256TypeStr:
        return Int256(int(str(v)))

    if t == _uintTypeStr:
        return UInt(int(str(v)))

    if t == _uint8TypeStr:
        return UInt8(int(str(v)))

    if t == _uint16TypeStr:
        return UInt16(int(str(v)))

    if t == _uint32TypeStr:
        return UInt32(int(str(v)))

    if t == _uint64TypeStr:
        return UInt64(int(str(v)))

    if t == _uint128TypeStr:
        return UInt128(int(str(v)))

    if t == _uint256TypeStr:
        return UInt256(int(str(v)))

    if t == _word8TypeStr:
        return Word8(int(str(v)))

    if t == _word16TypeStr:
        return Word16(int(str(v)))

    if t == _word32TypeStr:
        return Word32(int(str(v)))

    if t == _word64TypeStr:
        return Word64(int(str(v)))

    if t == _fix64TypeStr:
        return Fix64.parse_string(str(v))

    if t == _ufix64TypeStr:
        return UFix64.parse_string(str(v))

    if t == _arrayTypeStr:
        return Array([x for x in v])

    if t == _dictionaryTypeStr:
        return Dictionary([KeyValuePair(x[_keyKey], x[_valueKey]) for x in v])

    if t == _resourceTypeStr:
        return Dictionary([KeyValuePair(x[_keyKey], x[_valueKey]) for x in v])

    raise NotImplemented()
