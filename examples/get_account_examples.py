from flow_py_sdk import flow_client
from examples.common import Example, Config
from examples.common.utils import random_account


# -------------------------------------------------------------------------
# Get an account using its address.
# -------------------------------------------------------------------------
class GetAccountExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="GA.1.", name="GetAccountExample", sort_order=901)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account = await client.get_account(
                # pass address as cadence.Address object
                address=ctx.service_account_address
            )
            self.log.info(f"Account Address: {account.address.hex()}")
            self.log.info(f"Account Balance: {account.balance}")
            self.log.info(f"Account Contracts: {len(account.contracts)}")
            self.log.info(f"Account Keys: {len(account.keys)}")


# -------------------------------------------------------------------------
# Get an account by address at the latest sealed block.
# -------------------------------------------------------------------------
class GetAccountAtLatestBlockExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="GA.2.", name="GetAccountAtLatestBlockExample", sort_order=902
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            _, _, _ = await random_account(client=client, ctx=ctx)
            account = await client.get_account_at_latest_block(
                # pass address as hex string
                address=ctx.service_account_address.hex()
            )
            self.log.info(f"Account Address: {account.address.hex()}")
            self.log.info(f"Account Balance: {account.balance}")
            self.log.info(f"Account Contracts: {len(account.contracts)}")
            self.log.info(f"Account Keys: {len(account.keys)}")


# -------------------------------------------------------------------------
# Get an account by address at the given block height.
# -------------------------------------------------------------------------
class GetAccountAtBlockHeightExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="GA.3.", name="GetAccountAtBlockHeightExample", sort_order=903
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            latest_block = await client.get_latest_block()
            _, _, _ = await random_account(client=client, ctx=ctx)
            account = await client.get_account_at_block_height(
                # pass address as bytes
                address=ctx.service_account_address.bytes,
                block_height=latest_block.height,
            )
            self.log.info(f"Account Address: {account.address.hex()}")
            self.log.info(f"Account Balance: {account.balance}")
            self.log.info(f"Account Contracts: {len(account.contracts)}")
            self.log.info(f"Account Keys: {len(account.keys)}")
