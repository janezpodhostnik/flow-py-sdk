import asyncio
from examples.common import Example, Config
from flow_py_sdk import cadence
from flow_py_sdk import script
from flow_py_sdk.script import Script
from flow_py_sdk import flow_client

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

        # --------------------------------
        # script with arguments Example
        # --------------------------------
        # script = Script(
        #         code="""
        #             pub fun main(a: Int, b: Int): Int {
        #                 return a + b
        #             }
        #         """,
        #         arguments=[cadence.Int(1), cadence.Int(1)]
        #     )

        script = Script()

        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
            ) as client:
                result = await client.execute_script(
                    script = script
                    # , block_id
                    # , block_height
                )
                print("Script result :\n")
                print(result.__dict__)
                print("\nrun script : successfully done...")


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------
# submit a script without arguments
# script = Script(
#         code="""
#             pub fun main(): Int {
#                 let a = 1
#                 let b = 1
#                 return a + b
#             }
#         """
#     )

# # script with arguments
# script_with_arg = Script(
#         code="""
#             pub fun main(a: Int, b: Int): Int {
#                 return a + b
#             }
#         """,
#         arguments=[cadence.Int(1), cadence.Int(1)]
#     )
    
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# # submit a script
# loop.run_until_complete(execute_script_example(script = script))
# # submit a script with arguments
# loop.run_until_complete(execute_script_example(script = script_with_arg))


  

