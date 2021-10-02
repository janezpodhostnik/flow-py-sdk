import asyncio
import logging
from examples.common import Example, Config
from flow_py_sdk import flow_client

# -------------------------------------------------------------------------
# Rretrieve a block by ID Class
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
                block = await client.get_block_by_i_d(
                    id = latest_block.id
                )
                print("Block :\n")
                print(block.__dict__)
                print("\nget block by id : successfully done...")

# -------------------------------------------------------------------------
# Retrieve a block by height Class
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
                block = await client.get_block_by_height(
                    height = latest_block.height
                )
                print("Block :\n")
                print(block.__dict__)
                print("\nget block by height : successfully done...")

# -------------------------------------------------------------------------
# Retrieve the latest block Class
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
                block = await client.get_latest_block(
                    is_sealed = False
                )
                print("Block :\n")
                print(block.__dict__)
                print("\nget latest block : successfully done...")

# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------
# GetLatestBlockExample.run()
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(get_block_by_height_example())
# loop.run_until_complete(get_block_by_id_example())
# loop.run_until_complete(get_latest_block_example())


  

