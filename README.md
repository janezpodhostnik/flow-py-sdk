# flow-py-sdk

Another unofficial flow blockchain python sdk.

Under development! I do not recommend you use this.

If you do want to used do:

`pip install flow-py-sdk`

## Prerequisites

- [poetry](https://python-poetry.org/docs/)
- python 3.9^

## Examples

First, install the [Flow CLI](https://docs.onflow.org/flow-cli).

Start the Flow Emulator in the main directory of this repository:

- `flow emulator start`
- `poetry build` (only the first time)
- `poetry install`
- `poetry run examples`

## TODO

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
- [ ] add more examples

### Tests

- [ ] add cadence decode/encode tests
- [ ] add more tests
- [ ] add CI for tests

### Implementation

- [ ] decode event payload from grpc
- [ ] implement TODOs in cadence decode/encode
- [ ] add an easy way to subscribe to blockchain events
