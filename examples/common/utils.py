from typing import Annotated

from ecdsa import SigningKey

from examples.common.config import Config
from flow_py_sdk import (
    cadence,
    AccessAPI,
    SignAlgo,
    AccountKey,
    Signer,
    HashAlgo,
    InMemorySigner,
    create_account_template,
    ProposalKey,
)


def random_key_pair(
    sign_algo: SignAlgo,
) -> (Annotated[bytes, "public key"], Annotated[bytes, "private key"]):
    sk = SigningKey.generate(curve=sign_algo.get_signing_curve())
    return sk.verifying_key.to_string(), sk.to_string()


async def random_account(
    *,
    client: AccessAPI,
    ctx: Config,
    contracts: dict[Annotated[str, "name"], Annotated[str, "source"]] = None,
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
        create_account_template(
            keys=[account_key],
            contracts=contracts,
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
        .with_envelope_signature(
            ctx.service_account_address, 0, ctx.service_account_signer
        )
    )

    result = await client.execute_transaction(tx)
    new_addresses = [
        e.value.address
        for e in result.events
        if isinstance(e.value, cadence.AccountCreatedEvent)
    ]

    return (
        new_addresses[0],
        account_key,
        InMemorySigner(
            sign_algo=SignAlgo.ECDSA_secp256k1,
            hash_algo=HashAlgo.SHA3_256,
            key_hex=priv.hex(),
        ),
    )
