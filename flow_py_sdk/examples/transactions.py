import logging
from ecdsa import SigningKey

from flow_py_sdk.cadence import Dictionary, Array, String
from flow_py_sdk.client import flow_client
from flow_py_sdk.examples.common import ExampleContext, Example
from flow_py_sdk.signer import get_signing_curve, SignAlgo, HashAlgo, AccountKey
from flow_py_sdk.tx import Tx, ProposalKey

log = logging.getLogger(__name__)


class TransactionExample1(Example):
    def __init__(self) -> None:
        super().__init__('NOOP transaction')

    async def run(self, ctx: ExampleContext):
        async with flow_client(host=ctx.access_node_host, port=ctx.access_node_port) as client:
            block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(address=ctx.service_account_address.bytes)

            tx = Tx(code="""transaction(){prepare(){log("OK")}}""",
                    reference_block_id=block.id,
                    payer=ctx.service_account_address,
                    proposal_key=ProposalKey(
                        key_address=ctx.service_account_address,
                        key_id=ctx.service_account_key_id,
                        key_sequence_number=proposer.keys[ctx.service_account_key_id].sequence_number
                    )) \
                .with_envelope_signature(ctx.service_account_address, ctx.service_account_key_id,
                                         ctx.service_account_signer)

            await client.execute_transaction(tx)


class TransactionExample2(Example):

    def __init__(self) -> None:
        super().__init__('Create account transaction')

    async def run(self, ctx: ExampleContext):
        async with flow_client(host=ctx.access_node_host, port=ctx.access_node_port) as client:
            sk = SigningKey.generate(curve=get_signing_curve(SignAlgo.ECDSA_secp256k1))
            log.info(sk.verifying_key.to_string().hex())

            account_key = AccountKey(public_key=sk.verifying_key.to_string(), sign_algo=SignAlgo.ECDSA_secp256k1,
                                     hash_algo=HashAlgo.SHA3_256)
            public_key = String(account_key.hex())

            cadence_public_keys = Array([public_key])
            cadence_contracts = Dictionary([])

            block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(address=ctx.service_account_address.bytes)

            tx = Tx(
                code=f"""
                    transaction(publicKeys: [String], contracts:{{String: String}}) {{
                        prepare(signer: AuthAccount) {{
                            let acct = AuthAccount(payer: signer)
                    
                            for key in publicKeys {{
                                acct.addPublicKey(key.decodeHex())
                            }}
                    
                            for contract in contracts.keys {{
                                acct.contracts.add(name: contract, code: contracts[contract]!.decodeHex())
                            }}
                        }}
                    }}
                """,
                reference_block_id=block.id,
                payer=ctx.service_account_address,
                proposal_key=ProposalKey(
                    key_address=ctx.service_account_address,
                    key_id=ctx.service_account_key_id,
                    key_sequence_number=proposer.keys[ctx.service_account_key_id].sequence_number
                )) \
                .add_authorizers(ctx.service_account_address) \
                .add_arguments(cadence_public_keys) \
                .add_arguments(cadence_contracts) \
                .with_payload_signature(ctx.service_account_address, 0, ctx.service_account_signer) \
                .with_envelope_signature(ctx.service_account_address, 0, ctx.service_account_signer)

            await client.execute_transaction(tx)
