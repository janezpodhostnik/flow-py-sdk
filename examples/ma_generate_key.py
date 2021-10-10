import asyncio
import json
from flow_py_sdk import account_key

from flow_py_sdk.account_key import AccountKey
import flow_py_sdk.client.client

from flow_py_sdk.signer.hash_algo import HashAlgo
from flow_py_sdk.signer.hash_algo import HashAlgo
from flow_py_sdk.signer.sign_algo import SignAlgo
import ecdsa
import hashlib
from flow_py_sdk import flow_client
from flow_py_sdk.cadence import Address

from examples.common import Example, Config

# -------------------------------------------------------------------------
# Global variable
# -------------------------------------------------------------------------
access_node_host: str = "access.mainnet.nodes.onflow.org"
access_node_port: int = 9000

# -------------------------------------------------------------------------
# Create AccountKey Instant.
# 
# There are 3 ways to create account key using Flow python SDK.
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# First: an account key can be creaed using a public key.
# -------------------------------------------------------------------------
class GetBlockByIdExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="A.1.", name="CreateAccountKeyByPublic", sort_order=801)
        
    def create_account_key_by_public(public_key = None,
            sign_algo = None,
            hash_algo = None):
        if public_key == None:
            public_key = bytes("dc3f27d583777e36800a0a490dc71cf1dd9348837a3ce2f66127e50ea6d5a528df72e53306ff2aa72775db1b6781158851cb2e70ffd2b314e471b18f1a477573","utf-8")
        if sign_algo == None:
            sign_algo = ecdsa.NIST256p
        if hash_algo == None:
            hash_algo = HashAlgo.SHA2_256

        acc_key = AccountKey(public_key=public_key, sign_algo=sign_algo,hash_algo=hash_algo)


        myJson = json.dumps(acc_key.__dict__)
        print(myJson)

# -------------------------------------------------------------------------
# Second: get an account key by retrieving an account
# -------------------------------------------------------------------------
class GetBlockByIdExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="A.2.", name="GetAccountKeyByProto", sort_order=802)

    async def get_account_from_proto(self, ctx: Config):

        service_account_address = Address.from_hex("0x18eb4ee6b3c026d2")
        async with flow_client(
                host = ctx.access_node_host, port = ctx.access_node_port
            ) as client:
                account = await client.get_account(address = service_account_address.bytes)

        return account

# -------------------------------------------------------------------------
# Third: Using seed pharse to create account key.
# this method also provide a signer to sign transaction or messages.
# -------------------------------------------------------------------------
class GetBlockByIdExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="A.3.", name="CreateAccountKeyBySeed", sort_order=803)
    def get_account_key_from_seed():

        acc_key, pk = AccountKey.from_seed(
            sign_algo = None, 
            hash_algo=None, 
            seed="JNFWM-NDDSE-GENPV-BUBYK-XAVEJ-MVECB-UHIHT-FKKHR-FFDQX-HNSIQ-QVATO-ZEHEQ"
            )

        return acc_key, pk

