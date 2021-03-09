from typing import Annotated

from ecdsa import SigningKey

from flow_py_sdk import cadence
from flow_py_sdk.client import AccessAPI
from examples.common.config import Config
from flow_py_sdk.signer import (
    get_signing_curve,
    SignAlgo,
    AccountKey,
    Signer,
    HashAlgo,
    InMemorySigner,
)
from flow_py_sdk.templates import create_account_template
from flow_py_sdk.tx import ProposalKey


def random_key_pair(
    sign_algo: SignAlgo,
) -> (Annotated[bytes, "public key"], Annotated[bytes, "private key"]):
    sk = SigningKey.generate(curve=get_signing_curve(sign_algo))
    return sk.verifying_key.to_string(), sk.to_string()


async def random_account(
    client: AccessAPI, ctx: Config
) -> (cadence.Address, AccountKey, Signer):
    pub, priv = random_key_pair(SignAlgo.ECDSA_secp256k1)

    account_key = AccountKey(
        public_key=pub, sign_algo=SignAlgo.ECDSA_secp256k1, hash_algo=HashAlgo.SHA3_256
    )

    block = await client.get_latest_block()
    proposer = await client.get_account_at_latest_block(
        address=ctx.service_account_address.bytes
    )

    tx = (
        create_account_template(keys=[account_key])
        .add_authorizers(ctx.service_account_address)
        .with_reference_block_id(block.id)
        .with_payer(ctx.service_account_address)
        .with_proposal_key(
            ProposalKey(
                key_address=ctx.service_account_address,
                key_id=ctx.service_account_key_id,
                key_sequence_number=proposer.keys[
                    ctx.service_account_key_id
                ].sequence_number,
            )
        )
        .with_payload_signature(
            ctx.service_account_address, 0, ctx.service_account_signer
        )
        .with_envelope_signature(
            ctx.service_account_address, 0, ctx.service_account_signer
        )
    )

    result = await client.execute_transaction(tx)

    return (
        None,
        account_key,
        InMemorySigner(
            sign_algo=SignAlgo.ECDSA_secp256k1,
            hash_algo=HashAlgo.SHA3_256,
            key_hex=priv.hex(),
        ),
    )
