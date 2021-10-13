import asyncio
import logging
import sys

from examples.common import Config, example_registry

log = logging.getLogger(__name__)


async def run_async(ctx: Config, examples: list[str]):
    if not examples:
        await example_registry.run_all(ctx)
    else:
        for ex in examples:
            await example_registry.run(ctx, ex)


def run():

    # last index of string "examples"
    example_index = len(sys.argv[0]) - 1 - sys.argv[::-1][0].index("examples")
    examples = sys.argv[example_index + 1 :]

    ctx = Config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_async(ctx, examples))


if __name__ == "__main__":
    run()
