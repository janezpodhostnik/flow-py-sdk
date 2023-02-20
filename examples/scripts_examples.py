from flow_py_sdk import flow_client, cadence, Script
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


# -------------------------------------------------------------------------
# Submit a complex script with arguments and parse the response Function
# -------------------------------------------------------------------------
class ExecuteComplexScriptWithArgumentExample(Example):
    def __init__(self) -> None:
        super().__init__(
            tag="S.3.", name="ExecuteComplexScriptWithArgumentExample", sort_order=403
        )

    async def run(self, ctx: Config):
        script = Script(
            code="""
                    pub struct User {
                        pub var balance: UFix64
                        pub var address: Address
                        pub var name: String

                        init(name: String, address: Address, balance: UFix64) {
                            self.name = name
                            self.address = address
                            self.balance = balance
                        }
                    }

                    pub fun main(name: String): User {
                        return User(
                            name: name,
                            address: 0x1,
                            balance: 10.0
                        )
                    }
                """,
            arguments=[cadence.String("flow")],
        )

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            complex_script = await client.execute_script(
                script=script
                # , block_id
                # , block_height
            )

            if not complex_script:
                raise Exception("Script execution failed")

            script_result: cadence.Value = complex_script

            self.log.info(
                f"Name: {script_result.as_type(cadence.Struct).name.as_type(cadence.String).value}"
            )
            self.log.info(
                f"Address: {script_result.as_type(cadence.Struct).address.as_type(cadence.Address).bytes.hex()}"
            )
            self.log.info(
                f"Balance: {script_result.as_type(cadence.Struct).balance.as_type(cadence.UFix64).value}"
            )
