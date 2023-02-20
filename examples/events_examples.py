from flow_py_sdk import flow_client, ProposalKey, Tx, cadence
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
            events = await client.get_events_for_height_range(
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
            events = await client.get_events_for_block_i_ds(
                type="flow.AccountCreated", block_ids=[latest_block.id]
            )
            self.log.info(f"event type: {events[0].events[0].type}")
            self.log.info(f"event value: {events[0].events[0].value}")
            self.log.info(f"event value: {events[0].events[0].transaction_id.hex()}")


# -------------------------------------------------------------------------
# This example shows that how an event type can be define using python SDK
# and how created event will be shown up on chain.
# -------------------------------------------------------------------------


class EmitEventFromContractExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="E.3.",
            name="Emit event from contract",
            sort_order=303,
        )

    async def run(self, ctx: Config):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            address, _, _ = await random_account(
                client=client,
                ctx=ctx,
                contracts={
                    "EventDemo": """
                        pub contract EventDemo {
                            pub event Add(x: Int, y: Int, sum: Int)

                            pub fun add(_ x: Int, _ y: Int) {
                                let sum = x + y
                                emit Add(x: x, y: y, sum: sum)
                            }
                        }""",
                },
            )

            block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=ctx.service_account_address.bytes
            )

            tx = Tx(
                code=f"""
                import EventDemo from {address.hex_with_prefix()}
                
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

            result = await client.execute_transaction(tx)

            add_event = [
                e.value for e in result.events if isinstance(e.value, cadence.Event)
            ][0]

            assert add_event.sum.as_type(cadence.Int).value == 7

            self.log.info(f"event type: {result.events[0].type}")
            self.log.info(f"event value: {result.events[0].value}")
            self.log.info(f"event value: {result.events[0].transaction_id.hex()}")
