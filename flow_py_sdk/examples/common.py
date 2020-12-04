import json
import logging
from abc import ABC, abstractmethod

from flow_py_sdk.cadence import Address
from flow_py_sdk.signer import Signer, InMemorySigner, HashAlgo, SignAlgo

log = logging.getLogger(__name__)


class ExampleContext(object):

    def __init__(self) -> None:
        super().__init__()

        self.service_account_address: Address = Address.from_hex('f8d6e0586b0a20c7')
        self.service_account_signer: Signer = InMemorySigner(
            HashAlgo.SHA3_256,
            SignAlgo.ECDSA_secp256k1,
            'd7b1e643cdf601c5b3ca2cdabd731a563f100a42a2c658ece09572ae99295abf')
        self.service_account_key_id: int = 0
        self.access_node_host: str = "localhost"
        self.access_node_port: int = 3569

        # noinspection PyBroadException
        try:
            with open('../flow.json') as json_file:
                data = json.load(json_file)
                self.service_account_address = Address.from_hex(data["accounts"]["service"]["address"])
                self.service_account_signer = InMemorySigner(
                    HashAlgo.from_string(data["accounts"]["service"]["hashAlgorithm"]),
                    SignAlgo.from_string(data["accounts"]["service"]["sigAlgorithm"]),
                    data["accounts"]["service"]["privateKey"])
        except Exception:
            log.warning("Cannot open flow.json, using default settings", exc_info=True, stack_info=True)


class Example(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    @abstractmethod
    async def run(self, ctx: ExampleContext):
        pass
