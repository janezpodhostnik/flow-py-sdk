import logging

from examples.common import Example, Config
from flow_py_sdk import flow_client

log = logging.getLogger(__name__)


class ClientExample1(Example):
    """
    Use the client to get an accounts deployed contracts
    """

    def __init__(self) -> None:
        super().__init__(tag="C.1.", name="Get Account Code", sort_order=51)

    async def run(self, ctx: Config):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            script = await client.get_account_at_latest_block(
                address=ctx.service_account_address.bytes
            )

            log.info(f"Account code {script.contracts}")
