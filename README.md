[![PyPI](https://img.shields.io/pypi/v/flow-py-sdk.svg)](https://pypi.org/project/flow-py-sdk/) 

# flow-py-sdk

Another unofficial flow blockchain python sdk.

Under development! I do not recommend you use this.

If you do want to use it do:

`pip install flow-py-sdk`

It supports python version 3.9 or higher

##Contributing

### Prerequisites

- [poetry](https://python-poetry.org/docs/)
- python 3.9^

### Running tests

Tests can be run using `poetry`.

```bash
poetry run pytest
```

### Running the examples locally

Install the [Flow CLI](https://docs.onflow.org/flow-cli).

Start the Flow Emulator in the `examples` directory of this repository (tha is where the `flow.json` is).

- `flow emulator start`
- `poetry install`
- `poetry build` (only the first time)
- `poetry run examples`

## Roadmap to MVP

### Docs

- [ ] Create docs folder
- [ ] Usage example docs:
    - [ ] using the emulator
    - [ ] create account
- [ ] contribution docs

### Examples

- [ ] move examples folder to root folder
- [ ] make each example runnable separately
- [ ] write instructions for running examples
- [ ] add more comments to examples
- [x] add examples to ci
- [ ] add more examples

### Tests

- [ ] add cadence decode/encode tests
- [ ] add more tests
- [x] add CI for tests

### CI

- [ ] release automation

### Implementation

- [ ] decode event payload from grpc
- [ ] implement TODOs in cadence decode/encode
- [ ] add an easy way to subscribe to blockchain events
