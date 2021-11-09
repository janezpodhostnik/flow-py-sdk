from flow_py_sdk import SignAlgo, HashAlgo, InMemorySigner, InMemoryVerifier
from examples.common.utils import random_key_pair
from examples.common import Example, Config


# -------------------------------------------------------------------------
# Sign and verify a user message off-chain
# -------------------------------------------------------------------------
class SignAndVerifyUserMessageOffChainExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="T.2.", name="SignAndVerifyUserMessageOfflineExample", sort_order=601)

    async def run(self, ctx: Config):
        # generate a random key pair for the user
        pub, priv = random_key_pair(SignAlgo.ECDSA_P256)

        signer = InMemorySigner(hash_algo=HashAlgo.SHA3_256, sign_algo=SignAlgo.ECDSA_P256, private_key_hex=priv.hex())

        # sign a message
        message = b"Hello World!"
        signature = signer.sign_user_message(message)

        # the verifier would only have the public key
        verifier = InMemoryVerifier(hash_algo=HashAlgo.SHA3_256, sign_algo=SignAlgo.ECDSA_P256,
                                    public_key_hex=pub.hex())

        # verify the signature
        is_valid = verifier.verify_user_message(message, signature)
        assert is_valid

        # the signer object is also a verifier and can be also be used to verify a message
        is_valid = signer.verify_user_message(message, signature)
        assert is_valid
