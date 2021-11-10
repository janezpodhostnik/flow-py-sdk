from unittest import TestCase

import ecdsa

from flow_py_sdk import InMemorySigner, SignAlgo, HashAlgo


class TestInMemorySigner(TestCase):
    def test_sign(self):
        s = [SignAlgo.ECDSA_P256, SignAlgo.ECDSA_secp256k1]

        h = [
            HashAlgo.SHA2_256,
            # HashAlgo.SHA2_384,
            HashAlgo.SHA3_256,
            # HashAlgo.SHA3_384,
        ]

        tags = [True, False]

        for sign_algo in s:
            for hash_algo in h:
                for tag in tags:
                    with self.subTest(
                        f"sign_algo: {sign_algo}, hash_algo: {hash_algo}, tag: {tag}"
                    ):
                        private_key = ecdsa.SigningKey.generate(
                            curve=sign_algo.get_signing_curve()
                        )

                        signer = InMemorySigner(
                            sign_algo=sign_algo,
                            hash_algo=hash_algo,
                            private_key_hex=private_key.to_string().hex(),
                        )
                        if tag:
                            signature = signer.sign(b"some_message", b"some_tag")
                        else:
                            signature = signer.sign(b"some_message")

                        hasher = hash_algo.create_hasher()
                        if tag:
                            hasher.update(b"some_tagsome_message")
                        else:
                            hasher.update(b"some_message")
                        _hash = hasher.digest()

                        valid = private_key.get_verifying_key().verify_digest(
                            signature, _hash
                        )

                        self.assertTrue(valid)

    def test_sign_verify(self):
        s = [SignAlgo.ECDSA_P256, SignAlgo.ECDSA_secp256k1]

        h = [
            HashAlgo.SHA2_256,
            # HashAlgo.SHA2_384,
            HashAlgo.SHA3_256,
            # HashAlgo.SHA3_384,
        ]

        for sign_algo in s:
            for hash_algo in h:
                with self.subTest(f"sign_algo: {sign_algo}, hash_algo: {hash_algo}"):
                    private_key = ecdsa.SigningKey.generate(
                        curve=sign_algo.get_signing_curve()
                    )

                    signer = InMemorySigner(
                        sign_algo=sign_algo,
                        hash_algo=hash_algo,
                        private_key_hex=private_key.to_string().hex(),
                    )
                    message = b"some_message"

                    signature = signer.sign_user_message(message)
                    valid = signer.verify_user_message(signature, message)

                    self.assertTrue(valid)

                    signature = signer.sign_transaction(message)
                    valid = signer.verify_transaction(signature, message)

                    self.assertTrue(valid)

                    signature = signer.sign_transaction(message)
                    valid = signer.verify_user_message(signature, message)

                    self.assertFalse(valid)

                    signature = signer.sign_user_message(message)
                    valid = signer.verify_transaction(signature, message)

                    self.assertFalse(valid)
