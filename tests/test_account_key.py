from unittest import TestCase

from flow_py_sdk import AccountKey, SignAlgo, HashAlgo
from flow_py_sdk.proto.flow.entities import AccountKey as ProtoAccountKey


class TestAccountKey(TestCase):
    def test_rlp(self):
        expected_rlp_hex = "f847b840c51c02aa382d8d382a121178de8ac97eb6a562a1008660669ab6a220c96fce76e1d392b0c156380ae713b0aa18ad9cff7b85bcc44a9eb43fcddb467f456f0ec803038203e8"

        key = AccountKey(
            public_key=bytes.fromhex(
                "c51c02aa382d8d382a121178de8ac97eb6a562a1008660669ab6a220c96fce76e1d392b0c156380ae713b0aa18ad9cff7b85bcc44a9eb43fcddb467f456f0ec8"
            ),
            sign_algo=SignAlgo.ECDSA_secp256k1,
            hash_algo=HashAlgo.SHA3_256,
            weight=AccountKey.weight_threshold,
        )
        rlp = key.rlp()

        self.assertEqual(expected_rlp_hex, rlp.hex())

    def test_hex(self):
        expected_rlp_hex = "f847b840c51c02aa382d8d382a121178de8ac97eb6a562a1008660669ab6a220c96fce76e1d392b0c156380ae713b0aa18ad9cff7b85bcc44a9eb43fcddb467f456f0ec803038203e8"

        key = AccountKey(
            public_key=bytes.fromhex(
                "c51c02aa382d8d382a121178de8ac97eb6a562a1008660669ab6a220c96fce76e1d392b0c156380ae713b0aa18ad9cff7b85bcc44a9eb43fcddb467f456f0ec8"
            ),
            sign_algo=SignAlgo.ECDSA_secp256k1,
            hash_algo=HashAlgo.SHA3_256,
            weight=AccountKey.weight_threshold,
        )
        rlp_hex = key.hex()

        self.assertEqual(expected_rlp_hex, rlp_hex)

    def test_from_proto(self):
        proto_account_key = ProtoAccountKey()
        proto_account_key.sign_algo = 2
        proto_account_key.hash_algo = 1

        AccountKey.from_proto(proto_account_key)
