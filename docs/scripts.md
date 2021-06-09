# Scripts

Cadence scripts can be used to get information from the Flow blockchain.

You can see scripts in action in the
examples [here](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/script_examples.py).

## Sending scripts

To following code can be used to send a script to an access ot the emulator.

```py
from flow_py_sdk import flow_client, Script

# ...

async with flow_client(host=access_node_host, port=access_node_port) as client:
    script = Script(
        code="""
            pub fun main() {
                let a = 1
                let b = 1
                log(a + b)
            }
        """
    )
    await client.execute_script(script)
```

If this script is sent to the emulator, the log will be visible in the emulator output.

## Getting script results

The return value of `client.execute_script` is the script result if the script returns a result. 
The type of the result is an abstract `cadence.Value`.

```py
async with flow_client(host=access_node_host, port=access_node_port) as client:
    script = Script(
        code="""
            pub fun main(): Int {
                let a = 1
                let b = 1
                return a + b
            }
        """
    )
    result = await client.execute_script(script)
    a_plus_b = result.as_type(cadence.Int).value
```

## Sending scripts with parameters

To execute scripts with arguments (parameters) two approaches can be used.

By using `__init__` parameters.

```py
async with flow_client(host=access_node_host, port=access_node_port) as client:
    script = Script(
        code="""
            pub fun main(a: Int, b: Int) {
                log(a + b)
            }
        """,
        arguments=[cadence.Int(1), cadence.Int(1)]
    )
    await client.execute_script(script)
```

By using `add_arguments`. 

```py
async with flow_client(host=access_node_host, port=access_node_port) as client:
    script = Script(
        code="""
            pub fun main(a: Int, b: Int) {
                log(a + b)
            }
        """
    ).add_arguments(cadence.Int(1), cadence.Int(1))
    
    await client.execute_script(script)
```

`add_arguments` can also be used to add one argument at a time.

```py
async with flow_client(host=access_node_host, port=access_node_port) as client:
    script = Script(
        code="""
            pub fun main(a: Int, b: Int) {
                log(a + b)
            }
        """
    ).add_arguments(cadence.Int(1)).add_arguments(cadence.Int(1))
    
    await client.execute_script(script)
```

All arguments ned to be a `cadence.Value` otherwise a `NotCadenceValueError` is raised.