from unittest import TestCase

from flow_py_sdk import HashAlgo


class TestHashAlgo(TestCase):
    def test_from_string(self):
        cases = [
            (HashAlgo.SHA2_256, "SHA2_256"),
            (HashAlgo.SHA2_384, "SHA2_384"),
            (HashAlgo.SHA3_256, "SHA3_256"),
            (HashAlgo.SHA3_384, "SHA3_384"),
        ]
        for algo, name in cases:
            with self.subTest(msg=name):
                self.assertEqual(algo, HashAlgo.from_string(name))

    def test_create_hasher(self):
        message = "some random message"
        cases = [
            (
                HashAlgo.SHA2_256,
                "SHA2_256",
                bytes.fromhex(
                    "68fb87dfba69b956f4ba98b748a75a604f99b38a4f2740290037957f7e830da8"
                ),
            ),
            (
                HashAlgo.SHA2_384,
                "SHA2_384",
                bytes.fromhex(
                    "a9b3e62ab9b2a33020e015f245b82e063afd1398211326408bc8fc31c2c15859594b0aee263fbb02f6d8b5065ad49df2"
                ),
            ),
            (
                HashAlgo.SHA3_256,
                "SHA3_256",
                bytes.fromhex(
                    "38effea5ab9082a2cb0dc9adfafaf88523e8f3ce74bfbeac85ffc719cc2c4677"
                ),
            ),
            (
                HashAlgo.SHA3_384,
                "SHA3_384",
                bytes.fromhex(
                    "f41e8de9af0c1f46fc56d5a776f1bd500530879a85f3b904821810295927e13a54f3e936dddb84669021052eb12966c3"
                ),
            ),
        ]
        for algo, name, expected_hash in cases:
            with self.subTest(msg=name):
                hasher = algo.create_hasher()
                hasher.update(message.encode("utf-8"))
                _hash = hasher.digest()
                self.assertEqual(expected_hash, _hash)
