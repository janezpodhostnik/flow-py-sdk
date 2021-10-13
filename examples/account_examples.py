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

from flow_py_sdk.templates import get_contract_template

import flow_py_sdk.cadence as cadence

from flow_py_sdk.signer import SignAlgo, HashAlgo
# -------------------------------------------------------------------------
# Create an account
# -------------------------------------------------------------------------
class SignTransactionExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="AC.1.", name="Create account transaction - using the template", sort_order=901)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                
                account_key, new_signer = AccountKey.from_seed(seed = "dfghj dfj kjhgf hgfd lkjhgf kjhgfd sdf45678l", sign_algo = SignAlgo.ECDSA_P256, hash_algo = HashAlgo.SHA3_256)
                latest_block = await client.get_latest_block()
                proposer = await client.get_account_at_latest_block(
                    address=ctx.service_account_address.bytes
                )

                tx = (
                    create_account_template(
                        keys=[account_key],
                        reference_block_id=latest_block.id,
                        payer=ctx.service_account_address,
                        proposal_key=ProposalKey(
                            key_address=ctx.service_account_address,
                            key_id=ctx.service_account_key_id,
                            key_sequence_number=proposer.keys[
                                ctx.service_account_key_id
                            ].sequence_number,
                        ),
                    )
                    .add_authorizers(ctx.service_account_address)
                    .with_envelope_signature(
                        ctx.service_account_address, 0, ctx.service_account_signer
                    )
                )

                result = await client.execute_transaction(tx)

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
            proposer = await client.get_account_at_latest_block(address = account_address.bytes)
            cadenceName = cadence.String(contract["Name"])
            cadenceCode = cadence.String(contract_source_hex)
            tx = (Tx(
                code = get_contract_template.addAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[
                        0
                    ].sequence_number,
                ),
                ).add_arguments(cadenceName)
                .add_arguments(cadenceCode)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

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
            proposer = await client.get_account_at_latest_block(address = account_address.bytes)
            cadenceName = cadence.String(contract["Name"])
            cadenceCode = cadence.String(contract_source_hex)
            tx = (Tx(
                code = get_contract_template.addAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[
                        0
                    ].sequence_number,
                ),
                ).add_arguments(cadenceName)
                .add_arguments(cadenceCode)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

            proposer.keys[0].sequence_number = proposer.keys[0].sequence_number + 1

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
            cadenceName = cadence.String(contract["Name"])
            cadenceCode = cadence.String(contract_source_hex)
            #Update account contract with a transaction
            tx = (
                Tx(
                code = get_contract_template.updateAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[
                        0
                    ].sequence_number,
                ),
                ).add_arguments(cadenceName)
                .add_arguments(cadenceCode)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

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
            proposer = await client.get_account_at_latest_block(address = account_address.bytes)
            cadenceName = cadence.String(contract["Name"])
            cadenceCode = cadence.String(contract_source_hex)
            tx = (Tx(
                code = get_contract_template.addAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[
                        0
                    ].sequence_number,
                ),
                ).add_arguments(cadenceName)
                .add_arguments(cadenceCode)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)

            proposer.keys[0].sequence_number = proposer.keys[0].sequence_number + 1

            # Delete the added contract from the account

            latest_block = await client.get_latest_block()

            tx = (
                Tx(
                code = get_contract_template.removeAccountContractTemplate,
                reference_block_id = latest_block.id,
                payer = account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[
                        0
                    ].sequence_number,
                ),
                ).add_arguments(cadenceName)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            result = await client.execute_transaction(tx)
