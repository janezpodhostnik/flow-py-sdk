import logging

from flow_py_sdk.client import flow_client
from flow_py_sdk.examples.common import ExampleContext, Example
from flow_py_sdk.script import Script
from flow_py_sdk.tx import Tx

log = logging.getLogger(__name__)


class TransactionExample1(Example):

    def __init__(self) -> None:
        super().__init__('Empty transaction')

    async def run(self, ctx: ExampleContext):
        async with flow_client(host=ctx.access_node_host, port=ctx.access_node_port) as client:
            await Tx() \
                .with_cadence_code(
                f"""
                    pub fun main() {{
                        let a = 1
                        let b = 1
                        log(a + b)
                    }}
                """) \
                .execute(client=client)


# async def example2():
#     async with flow_client(host="localhost", port=3569) as client:
#         tx_result = await Tx(). \
#             with_script("tx"). \
#             add_arguments(Value(), Value()). \
#             with_authorizer(). \
#             with_refernce_block(). \
#             with_proposal_key(). \
#             with_reference_block_id(). \
#             with_payer(). \
#             with_payload_signature(). \
#             with_envelope_signature(). \
#             send(client=client, wait_for_seal=True)
