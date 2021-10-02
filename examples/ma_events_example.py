import asyncio
from examples.common import Example, Config
from flow_py_sdk import flow_client

# -------------------------------------------------------------------------
# Retrieve events by name in the block height range Class
# -------------------------------------------------------------------------
class GetEventByNameForHeightRangeExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="E.1.", name="GetEventByNameForHeightRangeExample", sort_order=301)
    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                events = await client.get_events_for_height_range(
                    type = "", start_height = 0, end_height = 0
                )
                print("Events :\n")
                print(events)
                print("\nget events for height range by name : successfully done...")

# -------------------------------------------------------------------------
# Retrieve events by name in the block ids Function
# -------------------------------------------------------------------------
class GetEventByNameForBlockIdsExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="E.2.", name="GetEventByNameForBlockIdsExample", sort_order=302)
    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                latest_block = await client.get_latest_block()
                events = await client.get_events_for_block_i_ds(
                    type = "", block_ids = [latest_block.id]
                )
                print("Events :\n")
                print(events)
                print("\nget events for block ids by name : successfully done...")

# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(get_events_by_name_for_height_range_example())
# loop.run_until_complete(get_events_by_name_for_block_ids_example())


  

