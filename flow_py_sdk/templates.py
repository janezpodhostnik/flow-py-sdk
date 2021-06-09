from typing import Annotated

import flow_py_sdk.cadence as cadence
from flow_py_sdk.account_key import AccountKey
from flow_py_sdk.tx import Tx, ProposalKey


def create_account_template(
    *,
    keys: list[AccountKey],
    reference_block_id: bytes = None,
    payer: cadence.Address = None,
    proposal_key: ProposalKey = None,
    contracts: dict[Annotated[str, "name"], Annotated[str, "source"]] = None
) -> Tx:
    if keys:
        cadence_public_keys = cadence.Array([cadence.String(k.hex()) for k in keys])
    else:
        cadence_public_keys = cadence.Array([])
    if contracts:
        cadence_contracts = cadence.Dictionary(
            [
                cadence.KeyValuePair(
                    cadence.String(k), cadence.String(v.encode("utf-8").hex())
                )
                for (k, v) in contracts.items()
            ]
        )
    else:
        cadence_contracts = cadence.Dictionary([])

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
            reference_block_id=reference_block_id,
            payer=payer,
            proposal_key=proposal_key,
        )
        .add_arguments(cadence_public_keys)
        .add_arguments(cadence_contracts)
    )

    return tx
