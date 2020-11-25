import json

from ..cadence.decode import cadence_object_hook
from ..client import flow_client


async def example():
    async with flow_client(host="localhost", port=3569) as client:
        response = await client.get_latest_block(is_sealed=True)
        print(response.block.id.hex())

        result = await client.execute_script_at_latest_block(script=b"""
            import FlowServiceAccount from 0xf8d6e0586b0a20c7

            pub fun main(): UFix64 {
                let acct = getAccount(0xf8d6e0586b0a20c7)
                let balance = FlowServiceAccount.defaultTokenBalance(acct)
                return balance
            }
            """)
        cadence_value = json.loads(result.value, object_hook=cadence_object_hook)
        print(cadence_value.value)
