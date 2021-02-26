import logging
from typing import List

from flow_py_sdk.examples.common import ExampleContext, Example
from flow_py_sdk.examples import scripts, transactions

log = logging.getLogger(__name__)


async def run(ctx: ExampleContext):
    examples: List[Example] = [
        scripts.ScriptExample1(),
        scripts.ScriptExample2(),
        scripts.ScriptExample3(),
        scripts.ScriptExample4(),
        scripts.ScriptExample5(),
        transactions.TransactionExample1(),
        transactions.TransactionExample2(),
        transactions.TransactionExample3(),
        transactions.TransactionExample4(),
    ]

    i = 0
    for example in examples:
        i += 1
        # noinspection PyBroadException
        try:
            await example.run(ctx)
        except Exception:
            log.error(f"{i}. {example.name} FAILED\n", exc_info=True, stack_info=True)
            continue
        log.info(f"{i}.{example.name} OK\n")
