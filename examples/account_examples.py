from flow_py_sdk import (
    flow_client,
    AccountKey,
    ProposalKey,
    create_account_template,
    Tx,
    TransactionTemplates,
    cadence,
    SignAlgo,
    HashAlgo,
)
from examples.common import Example, Config
from examples.common.utils import random_account


# -------------------------------------------------------------------------
# Create an account
# -------------------------------------------------------------------------
class SignTransactionExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="AC.1.",
            name="Create account transaction - using the template",
            sort_order=901,
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account_key, _ = AccountKey.from_seed(
                seed="dfghj dfj kjhgf hgfd lkjhgf kjhgfd sdf45678l",
                sign_algo=SignAlgo.ECDSA_P256,
                hash_algo=HashAlgo.SHA3_256,
            )
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=ctx.service_account_address.bytes
            )
            transaction = (
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

            await client.execute_transaction(transaction)


# -------------------------------------------------------------------------
# Deploy a contract at an account
# -------------------------------------------------------------------------


class DeployContract(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="AC.2.",
            name="Deploy Contract at the account - using the template",
            sort_order=902,
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        # A test Contract define for this example, you can modify it by your self
        contract = {
            "Name": "TestOne",
            "source": """pub contract TestOne {
                                pub fun add(a: Int, b: Int): Int {
                                    return a + b
                                }
                                }""",
        }
        contract_source_hex = bytes(contract["source"], "UTF-8").hex()

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account_address, _, new_signer = await random_account(
                client=client, ctx=ctx
            )
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=account_address.bytes
            )
            contract_name = cadence.String(contract["Name"])
            contract_code = cadence.String(contract_source_hex)
            transaction = (
                Tx(
                    code=TransactionTemplates.addAccountContractTemplate,
                    reference_block_id=latest_block.id,
                    payer=account_address,
                    proposal_key=ProposalKey(
                        key_address=account_address,
                        key_id=0,
                        key_sequence_number=proposer.keys[0].sequence_number,
                    ),
                )
                .add_arguments(contract_name)
                .add_arguments(contract_code)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            await client.execute_transaction(transaction)


# -------------------------------------------------------------------------
# Update a contract at an account
# -------------------------------------------------------------------------
class UpdateContract(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="AC.3.",
            name="Update a Contract of the account - using the template",
            sort_order=903,
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        # A test Contract define for this example, you can modify it by your self
        contract = {
            "Name": "TestOne",
            "source": """pub contract TestOne {
                                pub fun add(a: Int, b: Int): Int {
                                    return a + b
                                }
                                }""",
        }
        contract_source_hex = bytes(contract["source"], "UTF-8").hex()

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account_address, _, new_signer = await random_account(
                client=client, ctx=ctx
            )
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=account_address.bytes
            )
            contract_name = cadence.String(contract["Name"])
            contract_code = cadence.String(contract_source_hex)
            transaction = (
                Tx(
                    code=TransactionTemplates.addAccountContractTemplate,
                    reference_block_id=latest_block.id,
                    payer=account_address,
                    proposal_key=ProposalKey(
                        key_address=account_address,
                        key_id=0,
                        key_sequence_number=proposer.keys[0].sequence_number,
                    ),
                )
                .add_arguments(contract_name)
                .add_arguments(contract_code)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            await client.execute_transaction(transaction)

            proposer.keys[0].sequence_number = proposer.keys[0].sequence_number + 1

            latest_block = await client.get_latest_block()
            # Updated Contract
            contract = {
                "Name": "TestOne",
                "source": """pub contract TestOne {
                                pub fun add(a: Int, b: Int): Int {
                                    return a * b
                                }
                                }""",
            }
            contract_source_hex = bytes(contract["source"], "UTF-8").hex()
            contract_name = cadence.String(contract["Name"])
            contract_code = cadence.String(contract_source_hex)
            # Update account contract with a transaction
            transaction = (
                Tx(
                    code=TransactionTemplates.updateAccountContractTemplate,
                    reference_block_id=latest_block.id,
                    payer=account_address,
                    proposal_key=ProposalKey(
                        key_address=account_address,
                        key_id=0,
                        key_sequence_number=proposer.keys[0].sequence_number,
                    ),
                )
                .add_arguments(contract_name)
                .add_arguments(contract_code)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            await client.execute_transaction(transaction)


# -------------------------------------------------------------------------
# Remove a contract from an account
# -------------------------------------------------------------------------
class RemoveContract(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="AC.4.",
            name="Remove a Contract from the account - using the template",
            sort_order=904,
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        # A test Contract define for this example, you can modify it by your self
        contract = {
            "Name": "TestOne",
            "source": """pub contract TestOne {
                                pub fun add(a: Int, b: Int): Int {
                                    return a + b
                                }
                                }""",
        }
        contract_source_hex = bytes(contract["source"], "UTF-8").hex()

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account_address, _, new_signer = await random_account(
                client=client, ctx=ctx
            )
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=account_address.bytes
            )
            contract_name = cadence.String(contract["Name"])
            contract_code = cadence.String(contract_source_hex)
            transaction = (
                Tx(
                    code=TransactionTemplates.addAccountContractTemplate,
                    reference_block_id=latest_block.id,
                    payer=account_address,
                    proposal_key=ProposalKey(
                        key_address=account_address,
                        key_id=0,
                        key_sequence_number=proposer.keys[0].sequence_number,
                    ),
                )
                .add_arguments(contract_name)
                .add_arguments(contract_code)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            await client.execute_transaction(transaction)

            proposer.keys[0].sequence_number = proposer.keys[0].sequence_number + 1

            # Delete the added contract from the account

            latest_block = await client.get_latest_block()

            transaction = (
                Tx(
                    code=TransactionTemplates.removeAccountContractTemplate,
                    reference_block_id=latest_block.id,
                    payer=account_address,
                    proposal_key=ProposalKey(
                        key_address=account_address,
                        key_id=0,
                        key_sequence_number=proposer.keys[0].sequence_number,
                    ),
                )
                .add_arguments(contract_name)
                .add_authorizers(account_address)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            await client.execute_transaction(transaction)
