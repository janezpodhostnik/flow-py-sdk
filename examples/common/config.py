import json
import logging
from pathlib import Path

from flow_py_sdk.cadence import Address
from flow_py_sdk.signer import InMemorySigner, HashAlgo, SignAlgo

log = logging.getLogger(__name__)


class Config(object):
    def __init__(self) -> None:
        super().__init__()

        self.access_node_host: str = "localhost"
        self.access_node_port: int = 3569

        self.service_account_key_id: int = 0
        config_location = Path(__file__).parent.joinpath("../flow.json")
        try:
            with open(config_location) as json_file:
                data = json.load(json_file)
                self.service_account_address = Address.from_hex(
                    data["accounts"]["emulator-account"]["address"]
                )
                self.service_account_signer = InMemorySigner(
                    HashAlgo.from_string(
                        data["accounts"]["emulator-account"]["hashAlgorithm"]
                    ),
                    SignAlgo.from_string(
                        data["accounts"]["emulator-account"]["sigAlgorithm"]
                    ),
                    data["accounts"]["emulator-account"]["keys"],
                )
        except Exception:
            log.warning(
                f"Cannot open {config_location}, using default settings",
                exc_info=True,
                stack_info=True,
            )
