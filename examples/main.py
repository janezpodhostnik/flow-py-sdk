import asyncio
import logging

from examples.common import Config, example_registry

log = logging.getLogger(__name__)


async def run_async(ctx: Config):
    await example_registry.run_all(ctx)


def run():
    ctx = Config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_async(ctx))


if __name__ == "__main__":
    run()
