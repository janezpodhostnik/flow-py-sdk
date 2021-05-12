# Examples

Examples are meant to illustrate usage of `flow-py-sdk`. They can be found (here)[https://github.com/janezpodhostnik/flow-py-sdk/tree/master/examples]


## Running The examples

In case you want to debug the examples, or you just want to see them in action you can use the following steps.

### Prerequisites


- a checkout of `flow-py-sdk`
- python 3.9 or higher
- (poetry)[https://python-poetry.org/]

Run 

```sh
poetry install
``` 

in the root of the checkout.

### Run all examples

To run all the examples use:

```sh
poetry run examples
```


### Run specific examples

To run specific examples you can use the tag of the examples:

```sh
poetry run examples [ExampleTag]
```

e.g.

```sh
poetry run examples T.1. T.2. S.4.
```
