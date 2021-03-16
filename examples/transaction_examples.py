import logging

from flow_py_sdk import (
    cadence,
    flow_client,
    SignAlgo,
    HashAlgo,
    AccountKey,
    create_account_template,
    Tx,
    ProposalKey,
)
from examples.common import Config, random_key_pair, Example
from flow_py_sdk.cadence import AccountCreatedEvent

log = logging.getLogger(__name__)


class TransactionExample1(Example):
    """
    sends a noop transaction
    """

    def __init__(self) -> None:
        super().__init__(tag="T.1.", name="NOOP transaction", sort_order=202)

    async def run(self, ctx: Config):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=ctx.service_account_address.bytes
            )

            tx = Tx(
                code="""transaction(){prepare(){log("OK")}}""",
                reference_block_id=block.id,
                payer=ctx.service_account_address,
                proposal_key=ProposalKey(
                    key_address=ctx.service_account_address,
                    key_id=ctx.service_account_key_id,
                    key_sequence_number=proposer.keys[
                        ctx.service_account_key_id
                    ].sequence_number,
                ),
            ).with_envelope_signature(
                ctx.service_account_address,
                ctx.service_account_key_id,
                ctx.service_account_signer,
            )

            await client.execute_transaction(tx)


class TransactionExample2(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="T.2.",
            name="Create account transaction - using the template",
            sort_order=202,
        )

    async def run(self, ctx: Config):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            pub_key, priv_key = random_key_pair(SignAlgo.ECDSA_secp256k1)

            # prepare parameters
            account_key = AccountKey(
                public_key=pub_key,
                sign_algo=SignAlgo.ECDSA_secp256k1,
                hash_algo=HashAlgo.SHA3_256,
            )

            block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=ctx.service_account_address.bytes
            )

            tx = (
                create_account_template(
                    keys=[account_key],
                    reference_block_id=block.id,
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
                .with_payload_signature(
                    ctx.service_account_address, 0, ctx.service_account_signer
                )
                .with_envelope_signature(
                    ctx.service_account_address, 0, ctx.service_account_signer
                )
            )

            result = await client.execute_transaction(tx)

            log.info(f"new address event: {result.events[0].value}")


class TransactionExample3(Example):
    def __init__(self) -> None:
        super().__init__(tag="T.3.", name="Create account transaction", sort_order=203)

    async def run(self, ctx: Config):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            pub_key, _ = random_key_pair(SignAlgo.ECDSA_secp256k1)

            # prepare parameters
            account_key = AccountKey(
                public_key=pub_key,
                sign_algo=SignAlgo.ECDSA_secp256k1,
                hash_algo=HashAlgo.SHA3_256,
            )
            account_key_hex = cadence.String(account_key.hex())
            cadence_public_keys = cadence.Array([account_key_hex])
            cadence_contracts = cadence.Dictionary([])

            block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=ctx.service_account_address.bytes
            )

            tx = (
                Tx(
                    code="""
                    transaction(publicKeys: [String], contracts:{String: String}) {
                        prepare(signer: AuthAccount) {
                            let acct = AuthAccount(payer: signer)
                    
                            for key in publicKeys {
                                acct.addPublicKey(key.decodeHex())
                            }
                    
                            for contract in contracts.keys {
                                acct.contracts.add(name: contract, code: contracts[contract]!.decodeHex())
                            }
                        }
                    }
                """,
                    reference_block_id=block.id,
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
                .add_arguments(cadence_public_keys)
                .add_arguments(cadence_contracts)
                .with_payload_signature(
                    ctx.service_account_address, 0, ctx.service_account_signer
                )
                .with_envelope_signature(
                    ctx.service_account_address, 0, ctx.service_account_signer
                )
            )

            await client.execute_transaction(tx)
