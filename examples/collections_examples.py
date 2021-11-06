from flow_py_sdk import flow_client
from examples.common import Example, Config

from examples.common.utils import random_account


# -------------------------------------------------------------------------
# Retrieve a collection by ID
# -------------------------------------------------------------------------
class GetCollectionByIdExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="CL.1.", name="GetCollectionByIdExample", sort_order=201)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            _, _, _ = await random_account(client=client, ctx=ctx)
            block = await client.get_latest_block(is_sealed=True)
            collection_id = block.collection_guarantees[0].collection_id

            collection = await client.get_collection_by_i_d(id=collection_id)
            self.log.info(f"ID: {collection.id.hex()}")
            self.log.info(
                f"Transactions: [{', '.join(x.hex() for x in collection.transaction_ids)}]"
            )
