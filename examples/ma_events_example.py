import asyncio
from typing import List
from flow_py_sdk.client.entities import Collection
from flow_py_sdk import flow_client

# -------------------------------------------------------------------------
# Global variable
# -------------------------------------------------------------------------
access_node_host: str = "access.devnet.nodes.onflow.org"
access_node_port: int = 9000

# -------------------------------------------------------------------------
# Retrieve events by name in the block height range Function
# -------------------------------------------------------------------------
async def get_events_by_name_for_height_range_example(event_name: str = None, start_height: int = None, end_height: int = None):
    if(event_name == None):
        event_name = "Transfer"
    if(start_height == None):
        start_height = 46258000
    if(end_height == None):
        end_height = 46258119
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    async with flow_client(
            host = access_node_host, port = access_node_port
        ) as client:
            events = await client.get_events_for_height_range(
                type = event_name, start_height = start_height, end_height = end_height
            )
            print("Events :\n")
            print(events)
            print("\nget events for height range by name : successfully done...")

# -------------------------------------------------------------------------
# Retrieve events by name in the block ids Function
# -------------------------------------------------------------------------
async def get_events_by_name_for_block_ids_example(event_name: str = None, block_ids: List[bytes] = None):
    if(event_name == None):
        event_name = "Transfer"
    if(block_ids == None):
        block_ids = [bytes.fromhex('48338b132f33a7d8776adc777730c601e1d4f4ccb04261c066aad78269b14e9e')]

    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    async with flow_client(
            host = access_node_host, port = access_node_port
        ) as client:
            events = await client.get_events_for_block_i_ds(
                type = event_name, block_ids = block_ids
            )
            print("Events :\n")
            print(events)
            print("\nget events for block ids by name : successfully done...")

# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(get_events_by_name_for_height_range_example())
loop.run_until_complete(get_events_by_name_for_block_ids_example())


  

