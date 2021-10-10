import asyncio
from examples.common import Example, Config
from flow_py_sdk.tx import Tx
from flow_py_sdk import ProposalKey
from examples.common.utils import random_account
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
# Retrieve events for account creation Function
# -------------------------------------------------------------------------
class GetEventForAccountCreationExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="E.3.", name="GetEventForAccountCreationExample", sort_order=303)
    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                # Deploy a contract with an event defined
                contract = f"""
                    pub contract EventDemo {{
                        pub event Add(x: Int, y: Int, sum: Int)
                        pub fun add(x: Int, y: Int) {{
                            let sum = x + y
                            emit Add(x: x, y: y, sum: sum)
                        }}
                    }}
                """

                # get random acount
                account_address, account_key, new_signer = await random_account( client = client, ctx = ctx, contracts = {'EventDemo': contract })
                block = await client.get_latest_block()
                proposer = await client.get_account_at_latest_block(
                    address=ctx.service_account_address.bytes
                )
                
                tx = Tx(
                    code=f"""
                    import EventDemo from {account_address.hex_with_prefix()}
                    
                    transaction() {{
                        prepare() {{
                            EventDemo.add(1, 6)
                        }}
                    }}
                    """,
                    reference_block_id=block.id,
                    payer=ctx.service_account_address,
                    proposal_key=ProposalKey(
                        key_address=ctx.service_account_address,
                        key_id=ctx.service_account_key_id,
                        key_sequence_number=proposer.keys[
                            ctx.service_account_key_id
                        ].sequence_number,
                    ),
                ).with_envelope_signature(
                    ctx.service_account_address,
                    ctx.service_account_key_id,
                    ctx.service_account_signer,
                )

                tx_result = await client.execute_transaction(tx)

                # Query for account creation events by type
                events = await client.get_events_for_height_range(
                    type = "flow.AccountCreated", start_height = 0, end_height = 100
                )

                print("Events :\n")
                print(events)
                print("\nget AccountCreated event : successfully done...")

                # Query for our custom event by type
                type = 'AC.'+account_address.hex_with_prefix()+'.EventDemo.EventDemo.Add'
                events = await client.get_events_for_height_range(
                    type = type, start_height = 0, end_height = 100
                )

                print("Events :\n")
                print(events)
                print("\nget our custom event : successfully done...")

                # Query event by transaction
                print("Events :\n")
                print(tx_result.events)
                print("\nget our custom event : successfully done...")

# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(get_events_by_name_for_height_range_example())
# loop.run_until_complete(get_events_by_name_for_block_ids_example())


  

