import asyncio
from flow_py_sdk.cadence import address
from flow_py_sdk.tx import Tx
import logging
from examples.common import Example, Config
from flow_py_sdk.account_key import AccountKey
from flow_py_sdk import ProposalKey
from flow_py_sdk import flow_client
from examples.common.utils import random_account
from flow_py_sdk import cadence


# -------------------------------------------------------------------------
# Sign a transaction
# -------------------------------------------------------------------------
class SignTransactionExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="T.2.", name="SignTransactionExample", sort_order=502)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                account_address, account_key, new_signer = await random_account( client = client, ctx = ctx)
                latest_block = await client.get_latest_block()
                proposer = await client.get_account_at_latest_block(address = ctx.service_account_address)

                tx = Tx(
                    code="""transaction(){prepare(){log("OK")}}""",
                    reference_block_id = latest_block.id,
                    payer = account_address,
                    proposal_key = ProposalKey(
                        key_address = account_address,
                        key_id = 0,
                        key_sequence_number = proposer.keys[
                            0
                        ].sequence_number,
                    ),
                ).with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )

                print("Sign Transaction :\n")
                print("Signed Transaction : \n")
                print(tx.__dict__)
                print("\nsign transaction : successfully done...")

# -------------------------------------------------------------------------
# Submit a signed transaction
# -------------------------------------------------------------------------
class SubmitSignedTransactionExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="T.3.", name="SubmitSignedTransactionExample", sort_order=503)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                account_address, account_key, new_signer = await random_account( client = client, ctx = ctx)
                latest_block = await client.get_latest_block()
                proposer = await client.get_account_at_latest_block(address = ctx.service_account_address)

                tx = Tx(
                    code="""transaction(){prepare(){log("OK")}}""",
                    reference_block_id = latest_block.id,
                    payer = account_address,
                    proposal_key = ProposalKey(
                        key_address = account_address,
                        key_id = 0,
                        key_sequence_number = proposer.keys[
                            0
                        ].sequence_number,
                    ),
                ).with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )

                await client.execute_transaction(tx)

                print("Submit a Signed Transaction :\n")
                print("\nsubmit a signed transaction : successfully done...")

# -------------------------------------------------------------------------
# Submit a signed transaction with arguments
# -------------------------------------------------------------------------
class SubmitSignedTransactionWithArgumentsExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="T.4.", name="SubmitSignedTransactionWithArgumentsExample", sort_order=504)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                account_address, account_key, new_signer = await random_account( client = client, ctx = ctx)
                latest_block = await client.get_latest_block()
                proposer = await client.get_account_at_latest_block(address = ctx.service_account_address)

                tx = (
                    Tx(
                    code="""transaction(arg : {String}){prepare(){log(arg)}}""",
                    reference_block_id = latest_block.id,
                    payer = account_address,
                    proposal_key = ProposalKey(
                        key_address = account_address,
                        key_id = 0,
                        key_sequence_number = proposer.keys[
                            0
                        ].sequence_number,
                    ),
                    ).add_arguments("argument1")
                    .with_envelope_signature(
                        account_address,
                        0,
                        new_signer,
                    )
                )

                await client.execute_transaction(tx)

                print("Submit a Signed Transaction with arguments :\n")
                print("\nsubmit a signed transaction with arguments : successfully done...")

# -------------------------------------------------------------------------
# Submit a signed transaction with multi party
# -------------------------------------------------------------------------
class SubmitMultiSignedTransactionExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="T.5.", name="SubmitMultiSignedTransactionExample", sort_order=505)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                account_address1, account_key1, new_signer1 = await random_account( client = client, ctx = ctx)
                account_address2, account_key2, new_signer2 = await random_account( client = client, ctx = ctx)
                latest_block = await client.get_latest_block()
                proposer = await client.get_account_at_latest_block(address = ctx.service_account_address)

                tx = (
                    Tx(
                    code="""transaction(){prepare(){log("OK")}}""",
                    reference_block_id = latest_block.id,
                    payer = account_address1,
                    proposal_key = ProposalKey(
                        key_address = account_address1,
                        key_id = 0,
                        key_sequence_number = proposer.keys[
                            0
                        ].sequence_number,
                    ),
                    ).add_authorizers([account_address1, account_address2])
                    .with_payload_signature(
                        account_address2,
                        0,
                        new_signer2,
                    )
                    .with_envelope_signature(
                        account_address1,
                        0,
                        new_signer1,
                    )
                )

                await client.execute_transaction(tx)

                print("Submit a multi Signed Transaction :\n")
                print("\nsubmit a multi signed transaction : successfully done...")

# -------------------------------------------------------------------------
# Rretrieve a transaction by ID Class
# -------------------------------------------------------------------------
class GetTransactionByIdExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="T.1.", name="GetTransactionByIdExample", sort_order=501)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:

                account_address, account_key, new_signer = await random_account( client = client, ctx = ctx)
                latest_block = await client.get_latest_block()
                proposer = await client.get_account_at_latest_block(address = ctx.service_account_address)

                tx = Tx(
                    code="""transaction(){prepare(){log("OK")}}""",
                    reference_block_id = latest_block.id,
                    payer = account_address,
                    proposal_key = ProposalKey(
                        key_address = account_address,
                        key_id = 0,
                        key_sequence_number = proposer.keys[
                            0
                        ].sequence_number,
                    ),
                ).with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )

                response = await client.send_transaction(tx)

                transactionId = response.id

                transaction = await client.get_transaction(
                    id = transactionId
                )
                print("Transaction :\n")
                print(transaction.__dict__)
                print("\nget transaction by id : successfully done...")