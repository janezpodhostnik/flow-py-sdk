import logging

from flow_py_sdk.client import flow_client
from flow_py_sdk.examples.common import ExampleContext, Example
from flow_py_sdk.script import Script

log = logging.getLogger(__name__)


class ScriptExample1(Example):
    def __init__(self) -> None:
        super().__init__("Script")

    async def run(self, ctx: ExampleContext):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            script = Script(
                code=f"""
                    pub fun main() {{
                        let a = 1
                        let b = 1
                        log(a + b)
                    }}
                """
            )

            await client.execute_script(script)


class ScriptExample2(Example):
    def __init__(self) -> None:
        super().__init__("Script with import")

    async def run(self, ctx: ExampleContext):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account_to_get_balance_from = ctx.service_account_address

            script = Script(
                code=f"""
                    import FlowServiceAccount from {ctx.service_account_address}

                    pub fun main() {{
                        let acct = getAccount({account_to_get_balance_from})
                        let balance = FlowServiceAccount.defaultTokenBalance(acct)
                        log(balance)
                    }}
                """
            )

            await client.execute_script(script)


class ScriptExample3(Example):
    def __init__(self) -> None:
        super().__init__("Script with import and return")

    async def run(self, ctx: ExampleContext):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            block = await client.get_latest_block(is_sealed=True)

            account_to_get_balance_from = ctx.service_account_address

            script = Script(
                code=f"""
                    import FlowServiceAccount from {ctx.service_account_address}

                    pub fun main(): UFix64 {{
                        let acct = getAccount({account_to_get_balance_from})
                        let balance = FlowServiceAccount.defaultTokenBalance(acct)
                        return balance
                    }}
                """
            )

            result = await client.execute_script(script, at_block_id=block.id)
            log.info(f"Script returned result {result}")


class ScriptExample4(Example):
    def __init__(self) -> None:
        super().__init__("Script with parameter, import and return")

    async def run(self, ctx: ExampleContext):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            block = await client.get_latest_block(is_sealed=True)

            account_to_get_balance_from = ctx.service_account_address

            script = Script(
                code=f"""
                    import FlowServiceAccount from {ctx.service_account_address}

                    pub fun main(address: Address): UFix64 {{
                        let acct = getAccount(address)
                        let balance = FlowServiceAccount.defaultTokenBalance(acct)
                        return balance
                    }}
                """
            ).add_arguments(account_to_get_balance_from)

            result = await client.execute_script(script, at_block_height=block.height)
            log.info(f"Script returned result {result}")


class ScriptExample5(Example):
    def __init__(self) -> None:
        super().__init__("Get Account Code")

    async def run(self, ctx: ExampleContext):
        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            script = await client.get_account_at_latest_block(
                address=ctx.service_account_address.bytes
            )

            log.info(f"Account code {script.contracts}")
