# Examples

Examples are meant to illustrate usage of `flow-py-sdk`. They can be found [here](https://github.com/janezpodhostnik/flow-py-sdk/tree/master/examples)


## Running The examples

In case you want to debug the examples, or you just want to see them in action you can use the following steps.

### 1. Prerequisites


- a checkout of `flow-py-sdk`
- python 3.9 or higher
- [poetry](https://python-poetry.org/)

Run 

```sh
poetry install
``` 

in the root of the checkout to instal dependencies from `pyproject.toml`.


#### 2. Run the emulator

To run the examples, the [flow emulator](https://github.com/onflow/flow-emulator) needs to be running locally. 
To do that you can use the following instructions or the instructions directly at https://github.com/onflow/flow-emulator.

1. Install the [Flow CLI](https://docs.onflow.org/flow-cli).

2. Start the Flow Emulator in the `examples` directory of this repository (where the `flow.json` config is) using the command:

```sh
flow emulator start
```

### 3. Run examples

To run all the examples use:

`poetry run examples`

To run specific examples you can use the tag of the examples:

`poetry run examples [ExampleTag]`

e.g.:

`poetry run examples T.1. T.2. S.4.`
