from dataclasses import dataclass

from flow_py_sdk import cadence
from flow_py_sdk.exceptions import PySDKError
from flow_py_sdk.templates import TransactionTemplates
from flow_py_sdk.client import AccessAPI
from flow_py_sdk.script import Script


@dataclass
class CompositeSignature(object):
    addr: str
    keyId: int
    signature: str


async def verify_user_signature(
    *, client: AccessAPI, message: bytes, composite_signatures: list[CompositeSignature]
) -> bool:
    # if there is no signature return False
    if len(composite_signatures) == 0:
        return False

    # it does not make sense for the signatures to be from different addresses
    if any(x.addr != composite_signatures[0].addr for x in composite_signatures):
        raise PySDKError("All signatures must be from the same address")

    address = cadence.Address.from_hex(composite_signatures[0].addr)
    signatures = cadence.Array(
        [cadence.String(x.signature) for x in composite_signatures]
    )
    key_indexes = cadence.Array([cadence.Int(x.keyId) for x in composite_signatures])
    cadence_message = cadence.String(str(message, "utf-8"))

    script = Script(
        code=TransactionTemplates.verifyAccountSignaturesTemplate,
        arguments=[
            address,
            signatures,
            key_indexes,
            cadence_message,
        ],
    )

    script_result = await client.execute_script(script)

    if script_result is None:
        return False

    return script_result.as_type(cadence.Bool).value
