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


class TransactionTemplates:
    updateAccountContractTemplate = """
    transaction(name: String, code: String) {
        prepare(signer: AuthAccount) {
            signer.contracts.update__experimental(name: name, code: code.decodeHex())
        }
    }
    """

    addAccountContractTemplate = """
    transaction(name: String, code: String) {
        prepare(signer: AuthAccount) {
            signer.contracts.add(name: name, code: code.decodeHex())
        }
    }
    """

    removeAccountContractTemplate = """
    transaction(name: String) {
        prepare(signer: AuthAccount) {
            signer.contracts.remove(name: name)
        }
    }
    """

    verifyAccountSignaturesTemplate = """
    import Crypto
    pub fun main(
      address: Address,
      signatures: [String],
      keyIndexes: [Int],
      message: String,
    ): Bool {
        let keyList = Crypto.KeyList()
        
        let account = getAccount(address)
        let keys = account.keys
        for keyIndex in keyIndexes {
            if let key = keys.get(keyIndex: keyIndex) {
                if key.isRevoked {
                    // cannot verify: the key at this index is revoked
                    return false
                }
                keyList.add(
                    PublicKey(
                        publicKey: key.publicKey.publicKey,
                        signatureAlgorithm: key.publicKey.signatureAlgorithm
                    ),
                    hashAlgorithm: key.hashAlgorithm,
                    weight: key.weight / 1000.0,
                )
            } else {
                // cannot verify: they key at this index doesn't exist
                return false
            }
        }
        
        let signatureSet: [Crypto.KeyListSignature] = []
        
        var i = 0
        for signature in signatures {
            signatureSet.append(
                Crypto.KeyListSignature(
                    keyIndex: i,
                    signature: signature.decodeHex()
                )
            )
            i = i + 1
        }
        
        return keyList.verify(
            signatureSet: signatureSet,
            signedData: message.utf8,
        )
    }
    """
