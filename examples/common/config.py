import json
import logging
from pathlib import Path

from flow_py_sdk.cadence import Address
from flow_py_sdk.signer import InMemorySigner, HashAlgo, SignAlgo

log = logging.getLogger(__name__)


class Config(object):
    def __init__(self, config_location: Path) -> None:
        super().__init__()

        self.access_node_host: str = "localhost"
        self.access_node_port: int = 3569

        self.service_account_key_id: int = 0
        # noinspection PyBroadException
        try:
            with open(config_location) as json_file:
                data = json.load(json_file)
                self.service_account_address = Address.from_hex(
                    data["accounts"]["emulator-account"]["address"]
                )
                self.service_account_signer = InMemorySigner(
                    hash_algo=HashAlgo.from_string(
                        data["accounts"]["emulator-account"]["hashAlgorithm"]
                    ),
                    sign_algo=SignAlgo.from_string(
                        data["accounts"]["emulator-account"]["sigAlgorithm"]
                    ),
                    private_key_hex=data["accounts"]["emulator-account"]["keys"],
                )
        except Exception:
            log.warning(
                f"Cannot open {config_location}, using default settings",
                exc_info=True,
                stack_info=True,
            )
