from abc import ABC, abstractmethod

from flow_py_sdk.cadence.types import Address


class ExampleContext(object):
    service_account_address: Address = Address.from_hex('f8d6e0586b0a20c7')
    access_node_host: str = "localhost"
    access_node_port: int = 3569


class Example(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    @abstractmethod
    async def run(self, ctx: ExampleContext):
        pass
