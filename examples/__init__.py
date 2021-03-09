import logging.config
from pathlib import Path

import toml

# TODO figure out how to not need this for the _ExampleMetaClass to work correctly
import examples.script_examples
import examples.transaction_examples
import examples.client_examples

logging_config = toml.load(Path(__file__).parent.joinpath("./logging.toml"))
logging.config.dictConfig(logging_config)
