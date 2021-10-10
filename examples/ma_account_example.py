import asyncio
from flow_py_sdk.cadence import address
from flow_py_sdk.proto import flow
from flow_py_sdk.tx import Tx
import logging
from examples.common import Example, Config
from flow_py_sdk.account_key import AccountKey
from flow_py_sdk import ProposalKey, create_account_template
from flow_py_sdk import flow_client
from examples.common.utils import random_account
from flow_py_sdk.client import AccessAPI

from flow_py_sdk.templates import removeAccountContractTemplate, addAccountContractTemplate, updateAccountContractTemplate

import flow_py_sdk.cadence as cadence
# -------------------------------------------------------------------------
# Create an account
# -------------------------------------------------------------------------
class SignTransactionExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="AC.1.", name="Create account transaction - using the template", sort_order=901)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        account_key, new_signer = AccountKey.from_seed(seed = "dfghj dfj kjhgf hgfd lkjhgf kjhgfd sdf45678l")

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                
                latest_block = await client.get_latest_block()
                proposer = await client.get_account_at_latest_block(address = ctx.service_account_address)

                tx = (
                    create_account_template(
                        keys = [account_key],
                        reference_block_id = latest_block.id,
                        payer = ctx.service_account_address,
                        proposal_key = ProposalKey(
                            key_address = ctx.service_account_address,
                            key_id = ctx.service_account_key_id,
                            key_sequence_number = proposer.keys[
                                ctx.service_account_key_id
                            ].sequence_number,
                        ),
                    )
                    .add_authorizers(ctx.service_account_signer)
                    .with_envelope_signature(
                        ctx.service_account_address, 0, ctx.service_account_signer
                    )
                )
                result = await client.execute_transaction(tx)


                print("new address event:\n")
                print(result.__dict__)
                print("\nCreating account : successfully done...")

# -------------------------------------------------------------------------
# Deploy a contract at an account
# -------------------------------------------------------------------------

class DeplyContract(Example):
    def __init__(self) -> None:
        super().__init__(tag="AC.2.", name="Deploy Contract at the account - using the template", sort_order=902)
    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        # A test Contract define for this example, you can modify it by your self
        contract = {
            "Name" : "TestOne",
            "source" : '''pub contract TestOne {
                                pub fun add(a: Int, b: Int): Int {
                                    return a + b
                                }
                                }'''
            }
        contract_source_hex = bytes(contract["source"],"UTF-8").hex()

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
            account_address, account_key, new_signer = await random_account( client = client, ctx = ctx)
            latest_block = await client.get_latest_block()
            cadenceName = cadence.String(contract["Name"])
            cadenceCode = cadence.String(contract_source_hex)
            tx = (
                Tx(
                code = addAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                ).add_arguments(cadenceName)
                .add_arguments(cadenceCode)
                .add_authorizers([account_address])
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

            print("Deply a contract :\n")
            print(result.__dict__)
            print("\nDeply a contract : successfully done...")

# -------------------------------------------------------------------------
# Update a contract at an account
# -------------------------------------------------------------------------
class UpdateContract(Example):
    def __init__(self) -> None:
        super().__init__(tag="AC.3.", name="Update a Contract of the account - using the template", sort_order=903)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        # A test Contract define for this example, you can modify it by your self
        contract = {
            "Name" : "TestOne",
            "source" : '''pub contract TestOne {
                                pub fun add(a: Int, b: Int): Int {
                                    return a + b
                                }
                                }'''
            }
        contract_source_hex = bytes(contract["source"],"UTF-8").hex()

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
            account_address, account_key, new_signer = await random_account( client = client, ctx = ctx)
            latest_block = await client.get_latest_block()
            cadenceName = cadence.String(contract["Name"])
            cadenceCode = cadence.String(contract_source_hex)
            tx = (
                Tx(
                code = addAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                ).add_arguments(cadenceName)
                .add_arguments(cadenceCode)
                .add_authorizers([account_address])
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

            latest_block = await client.get_latest_block()
            #Updated Contract
            contract = {
            "Name" : "TestOne",
            "source" : '''pub contract TestOne {
                                pub fun add(a: Int, b: Int): Int {
                                    return a * b
                                }
                                }'''
            }
            contract_source_hex = bytes(contract["source"],"UTF-8").hex()
            #Update account contract with a transaction
            tx = (
                Tx(
                code = updateAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                ).add_arguments(contract["Name"])
                .add_arguments(contract_source_hex)
                .add_authorizers([account_address])
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

            print("Update a contract :\n")
            print(result.__dict__)
            print("\Update a contract : successfully done...")

# -------------------------------------------------------------------------
# Remove a contract from an account
# -------------------------------------------------------------------------
class RemoveContract(Example):
    def __init__(self) -> None:
        super().__init__(tag="AC.4.", name="Remove a Contract from the account - using the template", sort_order=904)

    async def run(self, ctx: Config):
                # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        # A test Contract define for this example, you can modify it by your self
        contract = {
            "Name" : "TestOne",
            "source" : '''pub contract TestOne {
                                pub fun add(a: Int, b: Int): Int {
                                    return a + b
                                }
                                }'''
            }
        contract_source_hex = bytes(contract["source"],"UTF-8").hex()

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
            account_address, account_key, new_signer = await random_account( client = client, ctx = ctx)
            latest_block = await client.get_latest_block()
            cadenceName = cadence.String(contract["Name"])
            cadenceCode = cadence.String(contract_source_hex)
            tx = (
                Tx(
                code = addAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                ).add_arguments(cadenceName)
                .add_arguments(cadenceCode)
                .add_authorizers([account_address])
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

            # Delete the added contract from the account

            latest_block = await client.get_latest_block()

            tx = (
                Tx(
                code = removeAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                ).add_arguments(cadenceName)
                .add_authorizers([account_address])
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

            print("Remove a contract :\n")
            print(result.__dict__)
            print("\Remove a contract : successfully done...")
