from unittest import TestCase

from flow_py_sdk import SignAlgo


class TestHashAlgo(TestCase):
    def test_from_string(self):
        cases = [
            (SignAlgo.ECDSA_P256, "ECDSA_P256"),
            (SignAlgo.ECDSA_secp256k1, "ECDSA_secp256k1"),
        ]
        for algo, name in cases:
            with self.subTest(msg=name):
                self.assertEqual(algo, SignAlgo.from_string(name))

    def test_create_signer(self):
        cases = [
            (
                SignAlgo.ECDSA_P256,
                "ECDSA_P256",
                "NIST256p",
            ),
            (
                SignAlgo.ECDSA_secp256k1,
                "ECDSA_secp256k1",
                "SECP256k1",
            ),
        ]
        for algo, name, expected_curve_name in cases:
            with self.subTest(msg=name):
                curve = algo.get_signing_curve()
                self.assertEqual(expected_curve_name, curve.name)
