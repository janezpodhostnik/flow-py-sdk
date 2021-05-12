[![PyPI](https://img.shields.io/pypi/v/flow-py-sdk.svg)](https://pypi.org/project/flow-py-sdk/) 

# flow-py-sdk

Another unofficial flow blockchain python sdk.

Under development! Currently this is close to an "MVP" it is mostly missing docs and organization.

If you do want to use it, install it with:

`pip install flow-py-sdk`

or if using poetry:

`poetry add flow-py-sdk`

It supports python version 3.9 or higher

## Contributing

### Prerequisites

- [poetry](https://python-poetry.org/docs/)
- python 3.9^

### Running tests

Tests can be run using `poetry`.

```bash
poetry run pytest
```

### Running the examples locally

To run the examples, the [flow emulator](https://github.com/onflow/flow-emulator) needs to be running locally. 
To do that you can use the following instructions or the instructions directly at https://github.com/onflow/flow-emulator.

#### 1. Run the emulator

Install the [Flow CLI](https://docs.onflow.org/flow-cli).

Start the Flow Emulator in the `examples` directory of this repository (where the `flow.json` is).

`flow emulator start`

#### 2. Poetry Install (in case of first run)

In the base directory run:

`poetry install`


#### 3. Run The examples

To run all the examples use:

`poetry run examples`

To run specific examples you can use the tag of the examples:

`poetry run examples [ExampleTag]`

e.g.:

`poetry run examples T.1. T.2. S.4.`
