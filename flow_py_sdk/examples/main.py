from typing import List

from flow_py_sdk.examples.scripts import *

log = logging.getLogger(__name__)


async def run(ctx: ExampleContext):
    examples: List[Example] = [
        ScriptExample1(),
        ScriptExample2(),
        ScriptExample3(),
        ScriptExample4()
    ]

    i = 0
    for example in examples:
        i += 1
        # noinspection PyBroadException
        try:
            await example.run(ctx)
        except Exception:
            log.error(f'{i}. {example.name} FAILED\n', exc_info=True, stack_info=True)
            continue
        log.info(f'{i}.{example.name} OK\n')

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
