from flow_py_sdk import flow_client
from examples.common import Example, Config


# -------------------------------------------------------------------------
# Retrieve a block by ID
# -------------------------------------------------------------------------
class GetBlockByIdExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="B.1.", name="GetBlockByIdExample", sort_order=101)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            latest_block = await client.get_latest_block()
            block = await client.get_block_by_i_d(id=latest_block.id)
            self.log.info(f"Block ID: {block.id.hex()}")
            self.log.info(f"Block height: {block.height}")
            self.log.info(f"Block timestamp: [{block.timestamp}]")


# -------------------------------------------------------------------------
# Retrieve a block by height
# -------------------------------------------------------------------------
class GetBlockByHeightExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="B.2.", name="GetBlockByHeightExample", sort_order=102)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            latest_block = await client.get_latest_block()
            block = await client.get_block_by_height(height=latest_block.height)
            self.log.info(f"Block ID: {block.id.hex()}")
            self.log.info(f"Block height: {block.height}")
            self.log.info(f"Block timestamp: [{block.timestamp}]")


# -------------------------------------------------------------------------
# Retrieve the latest block
# -------------------------------------------------------------------------
class GetLatestBlockExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="B.3.", name="GetLatestBlockExample", sort_order=103)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            block = await client.get_latest_block(is_sealed=False)
            self.log.info(f"Block ID: {block.id.hex()}")
            self.log.info(f"Block height: {block.height}")
            self.log.info(f"Block timestamp: [{block.timestamp}]")
