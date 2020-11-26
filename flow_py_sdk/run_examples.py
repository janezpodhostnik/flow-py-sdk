import asyncio
import logging
import logging.config
from flow_py_sdk.examples.main import run as run_all, ExampleContext

_LOGCONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "handlers": {
        "console": {
            "class": "flow_py_sdk.colorstreamhandler.ColorStreamHandler",
            "stream": "ext://sys.stderr",
            "level": "INFO"
        }
    },

    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}


def run():
    ctx = ExampleContext()

    logging.config.dictConfig(_LOGCONFIG)

    logging.getLogger('flow_py_sdk').setLevel(logging.INFO)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_all(ctx))


if __name__ == "__main__":
    run()
