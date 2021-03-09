import logging

from examples.common import Example, Config, example_registry
from flow_py_sdk import Script, flow_client

log = logging.getLogger(__name__)


class ScriptExample1(Example):
    """
    Runs a simple script
    """

    def __init__(self) -> None:
        super().__init__(tag="S.1.", name="Run script", sort_order=101)

    async def run(self, ctx: Config):
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
    """
    Runs a script that imports another contract.
    """

    def __init__(self) -> None:
        super().__init__(tag="S.2.", name="Script with import", sort_order=102)

    async def run(self, ctx: Config):
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
    """
    Runs a script that imports another contract and returns a value
    """

    def __init__(self) -> None:
        super().__init__(
            tag="S.3", name="Script with import and return", sort_order=103
        )

    async def run(self, ctx: Config):
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
    """
    Runs a script that imports another contract uses a parameter and returns a value
    """

    def __init__(self) -> None:
        super().__init__(
            tag="S.4.", name="Script with parameter, import and return", sort_order=104
        )

    async def run(self, ctx: Config):
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
