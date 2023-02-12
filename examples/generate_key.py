import ecdsa
from flow_py_sdk import flow_client, AccountKey, signer
from ecdsa.keys import SigningKey
from examples.common import Example, Config


# -------------------------------------------------------------------------
# Create AccountKey Instant.
#
# There are 3 ways to create account key using Flow python SDK.
# -------------------------------------------------------------------------


# # -------------------------------------------------------------------------
# # First: an account key can be created using a public key.
# # -------------------------------------------------------------------------
class CreateAccountKeyByPublicExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="A.1.", name="CreateAccountKeyByPublicExample", sort_order=801
        )

    async def run(self, ctx: Config):
        sign_algo = ecdsa.NIST256p
        hash_algo = signer.HashAlgo.SHA2_256

        secret_key = SigningKey.generate()
        _ = secret_key.to_string()  # private_key
        verifying_key = secret_key.get_verifying_key()
        public_key = verifying_key.to_string()

        acc_key = AccountKey(
            public_key=public_key, sign_algo=sign_algo, hash_algo=hash_algo
        )

        self.log.info(acc_key.__dict__)


# -------------------------------------------------------------------------
# Second: get an account key by retrieving an account
# -------------------------------------------------------------------------


class GetAccountKeyByProtoExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="A.2.", name="GetAccountKeyByProtoExample", sort_order=802)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account = await client.get_account(
                address=ctx.service_account_address.bytes
            )


# # -------------------------------------------------------------------------
# # Third: Using seed phrase to create account key.
# # this method also provide a signer to sign transaction or messages.
# # -------------------------------------------------------------------------


class CreateAccountKeyBySeedExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="A.3.", name="CreateAccountKeyBySeedExample", sort_order=803
        )

    async def run(self, ctx: Config):
        # This function return AccountKey and Signer
        _, _ = AccountKey.from_seed(
            sign_algo=signer.SignAlgo.ECDSA_P256,
            hash_algo=signer.HashAlgo.SHA3_256,
            seed="JNFWM-NDDSE-GENPV-BUBYK-XAVEJ-MVECB-UHIHT-FKKHR-FFDQX-HNSIQ-QVATO-ZEHEQ",
        )
