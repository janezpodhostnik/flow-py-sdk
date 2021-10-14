from flow_py_sdk.script import Script
from flow_py_sdk import flow_client, cadence
from examples.common import Example, Config

# -------------------------------------------------------------------------
# Submit a script and parse the response Function
# -------------------------------------------------------------------------
class ExecuteScriptExample(Example):
    def __init__(self) -> None:
        super().__init__(tag="S.1.", name="ExecuteScriptExample", sort_order=401)

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

        # --------------------------------
        # script without arguments Example
        # --------------------------------
        script = Script(
            code="""
                    pub fun main(): Int {
                        let a = 1
                        let b = 1
                        return a + b
                    }
                """
        )

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            await client.execute_script(
                script=script
                # , block_id
                # , block_height
            )


# -------------------------------------------------------------------------
# Submit a script with arguments and parse the response Function
# -------------------------------------------------------------------------
class ExecuteScriptWithArgumentExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="S.2.", name="ExecuteScriptWithArgumentExample", sort_order=402
        )

    async def run(self, ctx: Config):
        # First Step : Create a client to connect to the flow blockchain
        # flow_client function creates a client using the host and port

        # --------------------------------
        # script with arguments Example
        # --------------------------------
        script = Script(
            code="""
                    pub fun main(a: Int, b: Int): Int {
                        return a + b
                    }
                """,
            arguments=[cadence.Int(1), cadence.Int(1)],
        )

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            await client.execute_script(
                script=script
                # , block_id
                # , block_height
            )
