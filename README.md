---
title: Flow Python SDK
description: Packages for Python developers to build applications that interact with the Flow network
contentType: INTRO
---
The Flow Python SDK provides a set of packages for Python developers to build applications that interact with the Flow network.

[![PyPI](https://img.shields.io/pypi/v/flow-py-sdk.svg)](https://pypi.org/project/flow-py-sdk/)
[![codecov](https://codecov.io/gh/janezpodhostnik/flow-py-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/codecov/example-go)


See the [DOCS](https://janezpodhostnik.github.io/flow-py-sdk)!


Note: This SDK is also fully compatible with the Flow Emulator and can be used for local development.

## Installing

To start using the SDK, install Python 3.9 or higher and install package:

```sh
pip install flow-py-sdk
```

or if using poetry:

`poetry add flow-py-sdk`

## Run examples

To run example first you need to install flow emulator and run it locally.

[go step-by-step based on your OS](https://github.com/onflow/flow-cli#flow-cli)

then install dependencies. to install dependencies of flow SDk run:

`poetry install`

after that run flow emulator  in example directory, using:

`flow emulator`

and then you can run examples using:

`poetry run examples`
