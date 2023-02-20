from examples.common import Example, Config
from examples.common.utils import random_account_with_weights
from flow_py_sdk import (
    flow_client,
    AccountKey,
    utils,
)


# -------------------------------------------------------------------------
# Sign and verify a user message
# this example shows how to verify a message was signed by the owner(s) of an account
# -------------------------------------------------------------------------
class SignAndVerifyUserMessageExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="V.1.", name="SignAndVerifyUserMessageExample", sort_order=601
        )

    async def run(self, ctx: Config):
        # generate a random account with 3 keys
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            # create account with tree half weight keys
            # only two signatures are required to sign a message (or a transaction)
            account_address, _, account_signers = await random_account_with_weights(
                client=client,
                ctx=ctx,
                weights=[
                    int(AccountKey.weight_threshold / 2),
                    int(AccountKey.weight_threshold / 2),
                    int(AccountKey.weight_threshold / 2),
                ],
            )

            # the message to sign. Could include some extra information, like the reference block id or the address.
            message = b"Hello World!"

            # get two signatures from the account signers
            # signer 1
            signature = account_signers[0].sign_user_message(message)
            c_signature_1 = utils.CompositeSignature(
                account_address.hex(), 0, signature.hex()
            )

            # signer 3
            signature = account_signers[2].sign_user_message(message)
            c_signature_2 = utils.CompositeSignature(
                account_address.hex(), 2, signature.hex()
            )

            # verify the signature is valid
            signature_is_valid = await utils.verify_user_signature(
                message=message,
                client=client,
                composite_signatures=[c_signature_1, c_signature_2],
            )

            assert signature_is_valid
