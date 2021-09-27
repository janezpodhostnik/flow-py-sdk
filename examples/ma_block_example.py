import asyncio
from flow_py_sdk import flow_client

# -------------------------------------------------------------------------
# Global variable
# -------------------------------------------------------------------------
access_node_host: str = "access.devnet.nodes.onflow.org"
access_node_port: int = 9000

# -------------------------------------------------------------------------
# Rretrieve a block by ID Function
# -------------------------------------------------------------------------
async def get_block_by_id_example(block_id: bytes = None):
    if(block_id == None):
        block_id = '48338b132f33a7d8776adc777730c601e1d4f4ccb04261c066aad78269b14e9e'

    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    async with flow_client(
            host = access_node_host, port = access_node_port
        ) as client:
            block = await client.get_block_by_i_d(
                id = bytes.fromhex(block_id)
            )
            print("Block :\n")
            print(block.__dict__)
            print("\nget block by id : successfully done...")

# -------------------------------------------------------------------------
# Retrieve a block by height Function
# -------------------------------------------------------------------------
async def get_block_by_height_example(block_height: int = None):
    if(block_height == None):
        block_height = 46183307

    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    async with flow_client(
            host = access_node_host, port = access_node_port
        ) as client:
            block = await client.get_block_by_height(
                height = block_height
            )
            print("Block :\n")
            print(block.__dict__)
            print("\nget block by height : successfully done...")

# -------------------------------------------------------------------------
# Retrieve the latest block Function
# -------------------------------------------------------------------------
async def get_latest_block_example(is_sealed : bool = False):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    async with flow_client(
            host = access_node_host, port = access_node_port
        ) as client:
            block = await client.get_latest_block(
            )
            print("Block :\n")
            print(block.__dict__)
            print("\nget latest block : successfully done...")

# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(get_block_by_height_example())
loop.run_until_complete(get_block_by_id_example())
loop.run_until_complete(get_latest_block_example())


  

