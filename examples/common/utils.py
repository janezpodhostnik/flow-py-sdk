from typing import Annotated

import ecdsa

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
    sk = ecdsa.SigningKey.generate(curve=sign_algo.get_signing_curve())
    return sk.verifying_key.to_string(), sk.to_string()


async def random_account(
    *,
    client: AccessAPI,
    ctx: Config,
    contracts: dict[Annotated[str, "name"], Annotated[str, "source"]] = None,
) -> (cadence.Address, AccountKey, Signer):
    """
    Generate a random account.
    Parameters
    ----------
    client: AccessAPI
        The client to use to create the account.
    ctx: Config
        The configuration to use.
    contracts: dict[str, str]
        The contracts to use for the account.

    Returns
    -------
    (cadence.Address, AccountKey, Signer)
        The address, account key, and signer for the new account.

    """
    address, keys, signers = await random_account_with_weights(
        client=client,
        ctx=ctx,
        weights=[AccountKey.weight_threshold],
        contracts=contracts,
    )
    return address, keys[0], signers[0]


async def random_account_with_weights(
    *,
    client: AccessAPI,
    ctx: Config,
    weights: list[int],
    contracts: dict[Annotated[str, "name"], Annotated[str, "source"]] = None,
) -> (cadence.Address, list[AccountKey], list[Signer]):
    """
    Generate a random account with a given set of weights.

    Parameters
    ----------
    client: AccessAPI
        The client to use to create the account.
    ctx: Config
        The configuration to use.
    weights: list[int]
        The weights to use for the account.
    contracts: dict[str, str]
        The contracts to use for the account.

    Returns
    -------
    (cadence.Address, list[AccountKey], list[Signer])
        The address, account keys, and signers for the new account.

    """
    keys = [random_key_pair(SignAlgo.ECDSA_P256) for _ in weights]

    account_keys = [
        AccountKey(
            public_key=keys[i][0],
            sign_algo=SignAlgo.ECDSA_P256,
            hash_algo=HashAlgo.SHA3_256,
            weight=weights[i],
        )
        for i in range(len(keys))
    ]

    block = await client.get_latest_block()
    proposer = await client.get_account_at_latest_block(
        address=ctx.service_account_address.bytes
    )

    tx = (
        create_account_template(
            keys=account_keys,
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
        e.value.address for e in result.events if e.value.id == "flow.AccountCreated"
    ]

    return (
        new_addresses[0],
        account_keys,
        [
            InMemorySigner(
                sign_algo=SignAlgo.ECDSA_P256,
                hash_algo=HashAlgo.SHA3_256,
                private_key_hex=priv.hex(),
            )
            for _, priv in keys
        ],
    )
