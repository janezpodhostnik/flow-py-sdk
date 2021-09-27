import asyncio
from flow_py_sdk.client.entities import Collection
from flow_py_sdk import flow_client

# -------------------------------------------------------------------------
# Global variable
# -------------------------------------------------------------------------
access_node_host: str = "access.devnet.nodes.onflow.org"
access_node_port: int = 9000

# -------------------------------------------------------------------------
# Retrieve a collection by ID Function
# -------------------------------------------------------------------------
async def get_collection_by_id_example(collection_id: bytes = None):
    if(collection_id == None):
        collection_id = '48338b132f33a7d8776adc777730c601e1d4f4ccb04261c066aad78269b14e9e'

    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    async with flow_client(
            host = access_node_host, port = access_node_port
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
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(get_collection_by_id_example())


  

