import asyncio
from examples.common import Example, Config
from flow_py_sdk import flow_client

# -------------------------------------------------------------------------
# Retrieve a collection by ID Class
# -------------------------------------------------------------------------
class GetCollectioByIdExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="CL.1.", name="GetCollectioByIdExample", sort_order=201)
    async def run(self, ctx: Config):
        collection_id = '48338b132f33a7d8776adc777730c601e1d4f4ccb04261c066aad78269b14e9e'

        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                collection = await client.get_collection_by_i_d(
                    id = bytes.fromhex(collection_id)
                )
                print("Collection :\n")
                print(collection.__dict__)
                print("\nget collection by id : successfully done...")

# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(get_collection_by_id_example())


  

