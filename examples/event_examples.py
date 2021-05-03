import logging

from examples.common import Config, random_key_pair, Example, random_account
from flow_py_sdk import (
    flow_client,
    SignAlgo,
    HashAlgo,
    AccountKey,
    create_account_template,
    ProposalKey,
    Tx,
    cadence,
)
from flow_py_sdk.cadence import AccountCreatedEvent

log = logging.getLogger(__name__)


class EventExample1(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="E.1.",
            name="Create account and get address from the event",
            sort_order=301,
        )

    async def run(self, ctx: Config):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            pub_key, _ = random_key_pair(SignAlgo.ECDSA_secp256k1)

            # prepare parameters
            account_key = AccountKey(
                public_key=pub_key,
                sign_algo=SignAlgo.ECDSA_secp256k1,
                hash_algo=HashAlgo.SHA3_256,
            )

            block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=ctx.service_account_address.bytes
            )

            tx = (
                create_account_template(
                    keys=[account_key],
                    reference_block_id=block.id,
                    payer=ctx.service_account_address,
                    proposal_key=ProposalKey(
                        key_address=ctx.service_account_address,
                        key_id=ctx.service_account_key_id,
                        key_sequence_number=proposer.keys[
                            ctx.service_account_key_id
                        ].sequence_number,
                    ),
                )
                .add_authorizers(ctx.service_account_address)
                .with_envelope_signature(
                    ctx.service_account_address, 0, ctx.service_account_signer
                )
            )

            result = await client.execute_transaction(tx)
            new_addresses = [
                e.value.address
                for e in result.events
                if isinstance(e.value, AccountCreatedEvent)
            ]
            log.info(f"new address: {new_addresses[0]}")


class EventExample2(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="E.2.",
            name="Emit event from contract",
            sort_order=302,
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

            assert add_event.fields[2].as_type(cadence.Int).value == 7


class EventExample3(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="E.3.",
            name="Emit event from contract, and get predefined event type",
            sort_order=302,
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

            class AddEvent(cadence.BaseEvent):
                def __init__(self):
                    super().__init__()
                    self.x = 0
                    self.y = 0
                    self.sum = 0

                def init_event(self):
                    self.x = self.fields[0].as_type(cadence.Int).value
                    self.y = self.fields[1].as_type(cadence.Int).value
                    self.sum = self.fields[2].as_type(cadence.Int).value

                @classmethod
                def event_id_constraint(cls) -> str:
                    return f"A.{address.hex()}.EventDemo.Add"

            cadence.EventTypeRegistry.register_event_type(AddEvent)

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
                e.value for e in result.events if isinstance(e.value, AddEvent)
            ][0]

            assert add_event.sum == 7
