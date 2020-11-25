import asyncio

from flow_py_sdk.examples.main import example


def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(example())


if __name__ == "__main__":
    run()