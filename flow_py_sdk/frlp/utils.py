def rlp_encode_uint64(value: int) -> bytes:
    return value.to_bytes(8, "big", signed=False).lstrip(b"\0")
