from flow_py_sdk import ProposalKey, flow_client, cadence, Tx
from examples.common.utils import random_account
from examples.common import Example, Config


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
            account_address, _, new_signer = await random_account(
                client=client, ctx=ctx
            )
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=account_address.bytes
            )

            transaction = Tx(
                code="""transaction(){prepare(){log("OK")}}""",
                reference_block_id=latest_block.id,
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            ).with_envelope_signature(
                account_address,
                0,
                new_signer,
            )


# -------------------------------------------------------------------------
# Submit a signed transaction
# -------------------------------------------------------------------------
class SubmitSignedTransactionExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="T.3.", name="SubmitSignedTransactionExample", sort_order=503
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

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

            transaction = Tx(
                code="""transaction(){prepare(){log("OK")}}""",
                reference_block_id=latest_block.id,
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            ).with_envelope_signature(
                account_address,
                0,
                new_signer,
            )

            await client.execute_transaction(transaction)


# -------------------------------------------------------------------------
# Submit a signed transaction without a reference block.
# the reference block will be set to the latest finalized block
# -------------------------------------------------------------------------
class SubmitSignedTransactionWithoutReferenceBlockExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="T.4.",
            name="SubmitSignedTransactionWithoutReferenceBlockExample",
            sort_order=504,
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account_address, _, new_signer = await random_account(
                client=client, ctx=ctx
            )
            proposer = await client.get_account_at_latest_block(
                address=account_address.bytes
            )

            transaction = Tx(
                code="""transaction(){prepare(){log("OK")}}""",
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            ).with_envelope_signature(
                account_address,
                0,
                new_signer,
            )

            result = await client.execute_transaction(transaction)
            assert result.error_message is None or len(result.error_message) == 0


# -------------------------------------------------------------------------
# Submit a signed transaction with arguments
# -------------------------------------------------------------------------
class SubmitSignedTransactionWithArgumentsExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="T.5.",
            name="SubmitSignedTransactionWithArgumentsExample",
            sort_order=505,
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

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
            arg1 = cadence.String("Hooray!!! It worked :))")
            transaction = (
                Tx(
                    code="""transaction(arg1 : String){prepare(){log(arg1)}}""",
                    reference_block_id=latest_block.id,
                    payer=account_address,
                    proposal_key=ProposalKey(
                        key_address=account_address,
                        key_id=0,
                        key_sequence_number=proposer.keys[0].sequence_number,
                    ),
                )
                .add_arguments(arg1)
                .with_envelope_signature(
                    account_address,
                    0,
                    new_signer,
                )
            )

            await client.execute_transaction(transaction)


# -------------------------------------------------------------------------
# Submit a signed transaction with multi party
# -------------------------------------------------------------------------
class SubmitMultiSignedTransactionExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="T.6.", name="SubmitMultiSignedTransactionExample", sort_order=506
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account_address1, _, new_signer1 = await random_account(
                client=client, ctx=ctx
            )
            account_address2, _, new_signer2 = await random_account(
                client=client, ctx=ctx
            )
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=account_address1.bytes
            )

            transaction = (
                Tx(
                    code="""transaction {
                    prepare(signer1: AuthAccount, signer2: AuthAccount) { 
                        log(signer1.address) 
                        log(signer2.address)
                    }
                }""",
                    reference_block_id=latest_block.id,
                    payer=account_address1,
                    proposal_key=ProposalKey(
                        key_address=account_address1,
                        key_id=0,
                        key_sequence_number=proposer.keys[0].sequence_number,
                    ),
                )
                .add_authorizers(account_address1)
                .add_authorizers(account_address2)
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

            await client.execute_transaction(transaction)


# -------------------------------------------------------------------------
# Retrieve a transaction by ID Class
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
            account_address, _, new_signer = await random_account(
                client=client, ctx=ctx
            )
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=account_address.bytes
            )

            transaction = Tx(
                code="""transaction(){prepare(){log("OK")}}""",
                reference_block_id=latest_block.id,
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            ).with_envelope_signature(
                account_address,
                0,
                new_signer,
            )

            response = await client.execute_transaction(transaction)
            transaction_id = response.id

            transaction = await client.get_transaction(id=transaction_id)
            self.log.info(f"transaction ID: {transaction_id.hex()}")
            self.log.info(f"transaction payer: {transaction.payer.hex()}")
            self.log.info(
                f"transaction proposer: {transaction.proposal_key.address.hex()}"
            )
            self.log.info(f"transaction script: {transaction.script.decode('utf-8')}")
