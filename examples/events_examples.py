from flow_py_sdk import flow_client
from examples.common import Example, Config
from examples.common.utils import random_account

# -------------------------------------------------------------------------
# Retrieve events by name in the block height range Class
# In this example, an account is created and then we try to get "AccountCreated"
# event.
# -------------------------------------------------------------------------
class GetEventByNameForHeightRangeExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="E.1.", name="GetEventByNameForHeightRangeExample", sort_order=301
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            _, _, _ = await random_account(client=client, ctx=ctx)
            latest_block = await client.get_latest_block()
            await client.get_events_for_height_range(
                type="flow.AccountCreated",
                start_height=latest_block.height - 1,
                end_height=latest_block.height,
            )


# -------------------------------------------------------------------------
# Retrieve events by name in the block ids Function
# In this example, an account is created and then we try to get "AccountCreated"
# event.
# -------------------------------------------------------------------------
class GetEventByNameForBlockIdsExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="E.2.", name="GetEventByNameForBlockIdsExample", sort_order=302
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            _, _, _ = await random_account(client=client, ctx=ctx)
            latest_block = await client.get_latest_block()
            await client.get_events_for_block_i_ds(
                type="flow.AccountCreated", block_ids=[latest_block.id]
            )
