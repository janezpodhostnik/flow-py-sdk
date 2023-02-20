## Overview

This reference documents all the methods available in the SDK, and explains in detail how these methods work. SDKs are
open source, and you can use them according to the licence.

The library client specifications can be found here:

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md)

## Getting Started

### Installing

```sh
pip install flow-py-sdk
```

or

```sh
poetry add flow-py-sdk
```

### Importing the Library

```sh
import flow_py_sdk
```

## Running examples

See [Running examples](./examples.md)

## Connect

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#create-a-flow-client)

The library uses gRPC to communicate with the access nodes and it must be configured with correct access node API URL.

📖 **Access API URLs** can be found [here](https://docs.onflow.org/access-api/#flow-access-node-endpoints). An error
will be returned if the host is unreachable. The Access Nodes APIs hosted by DapperLabs are accessible at:

- Testnet `access.devnet.nodes.onflow.org:9000`
- Mainnet `access.mainnet.nodes.onflow.org:9000`
- Local Emulator `127.0.0.1:3569`

Example:

```py
async with flow_client(
        host="127.0.0.1", port="3569"
) as flow_client:
# do something with `flow_client`
```

## Querying the Flow Network

After you have established a connection with an access node, you can query the Flow network to retrieve data about
blocks, accounts, events and transactions. We will explore how to retrieve each of these entities in the sections below.

### Get Blocks

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#query-blocks)

Query the network for block by id, height or get the latest block.

📖 **Block ID** is SHA3-256 hash of the entire block payload. This hash is stored as an ID field on any block response
object (ie. response from `GetLatestBlock`).

📖 **Block height** expresses the height of the block on the chain. The latest block height increases by one for every
valid block produced.

#### Examples

This example depicts ways to get the latest block as well as any other block by height or ID:

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/block_examples.py)
**

You can use the `GetLatestBlock` method to fetch the latest sealed or unsealed block:

```python
async with flow_client(
        host=ctx.access_node_host, port=ctx.access_node_port
) as client:
    block = await client.get_latest_block(
        is_sealed=False
        # or is_sealed = True can be used for retrieving sealed block
    )
    print("Block ID: {}".format(block.id.hex()))
    print("Block height: {}".format(block.height))
    print("Block timestamp: [{}]".format(block.timestamp))
```

You can use the `get_block_by_i_d` method to fetch the specific block with desired ID:

```python
async with flow_client(
        host=ctx.access_node_host, port=ctx.access_node_port
) as client:
    latest_block = await client.get_latest_block()
    block = await client.get_block_by_height(
        id=latest_block.id
    )
    print("Block ID: {}".format(block.id.hex()))
    print("Block height: {}".format(block.height))
    print("Block timestamp: [{}]".format(block.timestamp))
```

Also `get_block_by_height` method can be used to fetch the specific block with desired height:

```python
async with flow_client(
        host=ctx.access_node_host, port=ctx.access_node_port
) as client:
    latest_block = await client.get_latest_block()
    block = await client.get_block_by_height(
        height=latest_block.height
    )
    print("Block ID: {}".format(block.id.hex()))
    print("Block height: {}".format(block.height))
    print("Block timestamp: [{}]".format(block.timestamp))
```

Result output:

```bash
Block ID: 8d08c88873d079d8f2d929853a647a8703597898532f3b7f79b0e3b0320d0bf7
Block height: 146
Block timestamp: [2021-10-28 14:12:41.172587+00:00]

Block ID: 8d08c88873d079d8f2d929853a647a8703597898532f3b7f79b0e3b0320d0bf7
Block height: 146
Block timestamp: [2021-10-28 14:12:41.172587+00:00]

Block ID: 8d08c88873d079d8f2d929853a647a8703597898532f3b7f79b0e3b0320d0bf7
Block height: 146
Block timestamp: [2021-10-28 14:12:41.172587+00:00]
```

### Get Account

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#accounts)

Retrieve any account from Flow network's latest block or from a specified block height.

📖 **Account address** is a unique account identifier. Be mindful about the `0x` prefix, you should use the prefix as a
default representation but be careful and safely handle user inputs without the prefix.

An account includes the following data:

- Address: the account address.
- Balance: balance of the account.
- Contracts: list of contracts deployed to the account.
- Keys: list of keys associated with the account.

#### Examples

Example depicts ways to get an account at the latest block and at a specific block height:

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/account_examples.py)
**

Get an account using its address.

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        account = await client.get_account(
            address=ctx.service_account_address.bytes
        )
        print("Account Address: {}".format(account.address.hex()))
        print("Account Balance: {}".format(account.balance))
        print("Account Contracts: {}".format(len(account.contracts)))
        print("Account Keys: {}".format(len(account.keys)))
```

Get an account by address at the given block height.

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        latest_block = await client.get_latest_block()
        _, _, _ = await random_account(client=client, ctx=ctx)
        account = await client.get_account_at_block_height(
            address=ctx.service_account_address.bytes,
            block_height=latest_block.height,
        )
        print("Account Address: {}".format(account.address.hex()))
        print("Account Balance: {}".format(account.balance))
        print("Account Contracts: {}".format(len(account.contracts)))
        print("Account Keys: {}".format(len(account.keys)))
```

Get an account by address at the latest sealed block.

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        _, _, _ = await random_account(client=client, ctx=ctx)
        account = await client.get_account_at_latest_block(
            address=ctx.service_account_address.bytes
        )
        print("Account Address: {}".format(account.address.hex()))
        print("Account Balance: {}".format(account.balance))
        print("Account Contracts: {}".format(len(account.contracts)))
        print("Account Keys: {}".format(len(account.keys)))
```

Result output:

```bash
Account Address: f8d6e0586b0a20c7
Account Balance: 999999999999700000
Account Balance: 2
Account Keys: 1

Account Address: f8d6e0586b0a20c7
Account Balance: 999999999999600000
Account Balance: 2
Account Keys: 1
```

### Get Transactions

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#accounts)

Retrieve transactions from the network by providing a transaction ID. After a transaction has been submitted, you can
also get the transaction result to check the status.

📖 **Transaction ID** is a hash of the encoded transaction payload and can be calculated before submitting the
transaction to the network.

⚠️ The transaction ID provided must be from the current spork.

📖 **Transaction status** represents the state of transaction in the blockchain. Status can change until is finalized.

| Status    | Final | Description                                                              |
|-----------|-------|--------------------------------------------------------------------------|
| UNKNOWN   | ❌     | The transaction has not yet been seen by the network                     |
| PENDING   | ❌     | The transaction has not yet been included in a block                     |
| FINALIZED | ❌     | The transaction has been included in a block                             |
| EXECUTED  | ❌     | The transaction has been executed but the result has not yet been sealed |
| SEALED    | ✅     | The transaction has been executed and the result is sealed in a block    |
| EXPIRED   | ✅     | The transaction reference block is outdated before being executed        |

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/transactions_examples.py)
**

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        account_address, _, new_signer = await random_account(
            client=client, ctx=ctx
        )
        latest_block = await client.get_latest_block()
        proposer = await client.get_account_at_latest_block(
            address=account_address.bytes
        )

        transaction = Tx(
            code="""transaction(){prepare(){log("OK")}}""",
            reference_block_id=latest_block.id,
            payer=account_address,
            proposal_key=ProposalKey(
                key_address=account_address,
                key_id=0,
                key_sequence_number=proposer.keys[0].sequence_number,
            ),
        ).with_envelope_signature(
            account_address,
            0,
            new_signer,
        )

        response = await client.send_transaction(transaction=transaction.to_signed_grpc())

        transaction_id = response.id

        transaction = await client.get_transaction(id=transaction_id)
        print("transaction ID: {}".format(transaction_id.hex()))
        print("transaction payer: {}".format(transaction.payer.hex()))
        print(
            "transaction proposer: {}".format(
                transaction.proposal_key.address.hex()
            )
        )
        print("transaction script: {}".format(transaction.script.decode("utf-8")))

```

Example output:

```bash
transaction ID: 8f8adbfbe85cee39d3ee180a8c148b8ebc7bca8feae9f64a4c6f0c65e9db6663
transaction payer: 01cf0e2f2f715450
transaction proposer: 01cf0e2f2f715450
transaction script: transaction(){prepare(){log("OK")}}
```

### Get Events

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#events)

Retrieve events by a given type in a specified block height range or through a list of block IDs.

📖 **Event type** is a string that follow a standard format:

```
A.{contract address}.{contract name}.{event name}
```

Please read more about [events in the documentation](https://docs.onflow.org/core-contracts/flow-token/). The exception
to this standard are core events, and you should read more about them
in [this document](https://docs.onflow.org/cadence/language/core-events/).

📖 **Block height range** expresses the height of the start and end block in the chain.

#### Examples

Example depicts ways to get events within block range or by block IDs:

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/events_examples.py)
**

This example shows how to retrieve events by name in the block height range Class. In this example, an account is
created and then we try to get "AccountCreated" event.

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        _, _, _ = await random_account(client=client, ctx=ctx)
        latest_block = await client.get_latest_block()
        await client.get_events_for_height_range(
            type="flow.AccountCreated",
            start_height=latest_block.height - 1,
            end_height=latest_block.height,
        )
```

This example shows how to retrieve events by name in the block ids Function In this example, an account is created and
then we try to get "AccountCreated" event.

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        _, _, _ = await random_account(client=client, ctx=ctx)
        latest_block = await client.get_latest_block()
        await client.get_events_for_block_i_ds(
            type="flow.AccountCreated", block_ids=[latest_block.id]
        )
        print("event type: {}".format(events[0].events[0].type))
        print("event value: {}".format(events[0].events[0].value))
        print("event value: {}".format(events[0].events[0].transaction_id.hex()))
```

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        address, _, _ = await random_account(
            client=client,
            ctx=ctx,
            contracts={
                "EventDemo": """
                    pub contract EventDemo {
                        pub event Add(x: Int, y: Int, sum: Int)

                        pub fun add(_ x: Int, _ y: Int) {
                            let sum = x + y
                            emit Add(x: x, y: y, sum: sum)
                        }
                    }""",
            },
        )

        block = await client.get_latest_block()
        proposer = await client.get_account_at_latest_block(
            address=ctx.service_account_address.bytes
        )

        tx = Tx(
            code=f"""
            import EventDemo from {address.hex_with_prefix()}
            
            transaction() {{
                prepare() {{
                    EventDemo.add(1, 6)
                }}
            }}
            """,
            reference_block_id=block.id,
            payer=ctx.service_account_address,
            proposal_key=ProposalKey(
                key_address=ctx.service_account_address,
                key_id=ctx.service_account_key_id,
                key_sequence_number=proposer.keys[
                    ctx.service_account_key_id
                ].sequence_number,
            ),
        ).with_envelope_signature(
            ctx.service_account_address,
            ctx.service_account_key_id,
            ctx.service_account_signer,
        )

        result = await client.execute_transaction(tx)

        add_event = [
            e.value for e in result.events if isinstance(e.value, cadence.Event)
        ][0]

        assert add_event.fields[2].as_type(cadence.Int).value == 7

        print("event type: {}".format(result.events[0].type))
        print("event value: {}".format(result.events[0].value))
        print("event value: {}".format(result.events[0].transaction_id.hex()))

```

Example output:

```bash
event type: flow.AccountCreated
event value: flow.AccountCreated(address: 0xe9dd1081676bbc90)
event value: 7762301429e09d9a981f99df24244b45ae3e9e5f084dde5f5167f1e73ce8e306

event type: A.0dbaa95c7691bc4f.EventDemo.Add
event value: A.0dbaa95c7691bc4f.EventDemo.Add(x: 1, y: 6, sum: 7)
event value: dfc8c1ea51279ddc74c16ed7644361dbe4828181d56497a4ebb18a6bbf0fd574
```

### Get Collections

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#collections)

Retrieve a batch of transactions that have been included in the same block, known as ***collections***. Collections are
used to improve consensus throughput by increasing the number of transactions per block and they act as a link between a
block and a transaction.

📖 **Collection ID** is SHA3-256 hash of the collection payload.

#### Examples

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/collections_examples.py)
**

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        _, _, _ = await random_account(client=client, ctx=ctx)
        block = await client.get_latest_block(is_sealed=True)
        collection_id = block.collection_guarantees[0].collection_id

        collection = await client.get_collection_by_i_d(id=collection_id)
        print("ID: {}".format(collection.id.hex()))
        print(
            "Transactions: [{}]".format(
                ", ".join(x.hex() for x in collection.transaction_ids)
            )
        )
```

Example output:

```bash
ID: afc6a69bf375f0eee80635091d50a1c4bb5479c1e6a04803e422a06614c45a7c
Transactions: [d3a6b0cb53dfc72c38f365bb177a327c2bae8d4a6076a2909fc11d8f95510396]
```

### Execute Scripts

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#scripts)

Scripts allow you to write arbitrary non-mutating Cadence code on the Flow blockchain and return data. You can learn
more about [Cadence and scripts here](https://docs.onflow.org/cadence/language/), but we are now only interested in
executing the script code and getting back the data.

We can execute a script using the latest state of the Flow blockchain or we can choose to execute the script at a
specific time in history defined by a block height or block ID.

📖 **Block ID** is SHA3-256 hash of the entire block payload, but you can get that value from the block response
properties.

📖 **Block height** expresses the height of the block in the chain.

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/scripts_examples.py)
**

```
// simple script
pub fun main(a: Int): Int {
    return a + 10
}
// complex script
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
```

script can be a cadence function without any input:

```python
async def run(self, ctx: Config):
    script = Script(
        code="""
                    pub fun main(): Int {
                        let a = 1
                        let b = 1
                        return a + b
                    }
                """)

    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        await client.execute_script(
            script=script
            # , block_id
            # , block_height
        )
```

or it can be a more complex function which has some input:

```python
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
        print("Name: {}".format(complex_script.fields[2].value))
        print("Address: {}".format(complex_script.fields[1].bytes.hex()))
        print("Balance: {}".format(complex_script.fields[0].value))

```

```bash
Name: flow
Address: 0000000000000001
Balance: 1000000000
```

## Mutate Flow Network

Flow, like most blockchains, allows anybody to submit a transaction that mutates the shared global chain state. A
transaction is an object that holds a payload, which describes the state mutation, and one or more authorizations that
permit the transaction to mutate the state owned by specific accounts.

Transaction data is composed and signed with help of the SDK. The signed payload of transaction then gets submitted to
the access node API. If a transaction is invalid or the correct number of authorizing signatures are not provided, it
gets rejected.

Executing a transaction requires couple of steps:

- [Building a transaction](#build-transactions).
- [Signing a transaction](#sign-transactions).
- [Sending a transaction](#send-transactions).

## Transactions

A transaction is nothing more than a signed set of data that includes script code which are instructions on how to
mutate the network state and properties that define and limit it's execution. All these properties are explained bellow.

📖 **Script** field is the portion of the transaction that describes the state mutation logic. On Flow, transaction
logic is written in [Cadence](https://docs.onflow.org/cadence/). Here is an example transaction script:

```
transaction(greeting: String) {
  execute {
    log(greeting.concat(", World!"))
  }
}
```

📖 **Arguments**. A transaction can accept zero or more arguments that are passed into the Cadence script. The arguments
on the transaction must match the number and order declared in the Cadence script. Sample script from above accepts a
single `String` argument.

📖 **[Proposal key](https://docs.onflow.org/concepts/transaction-signing/#proposal-key)** must be provided to act as a
sequence number and prevent reply and other potential attacks.

Each account key maintains a separate transaction sequence counter; the key that lends its sequence number to a
transaction is called the proposal key.

A proposal key contains three fields:

- Account address
- Key index
- Sequence number

A transaction is only valid if its declared sequence number matches the current on-chain sequence number for that key.
The sequence number increments by one after the transaction is executed.

📖 **[Payer](https://docs.onflow.org/concepts/transaction-signing/#signer-roles)** is the account that pays the fees for
the transaction. A transaction must specify exactly one payer. The payer is only responsible for paying the network and
gas fees; the transaction is not authorized to access resources or code stored in the payer account.

📖 **[Authorizers](https://docs.onflow.org/concepts/transaction-signing/#signer-roles)** are accounts that authorize a
transaction to read and mutate their resources. A transaction can specify zero or more authorizers, depending on how
many accounts the transaction needs to access.

The number of authorizers on the transaction must match the number of AuthAccount parameters declared in the prepare
statement of the Cadence script.

Example transaction with multiple authorizers:

```
transaction {
  prepare(authorizer1: AuthAccount, authorizer2: AuthAccount) { }
}
```

📖 **Gas limit** is the limit on the amount of computation a transaction requires, and it will abort if it exceeds its
gas limit. Cadence uses metering to measure the number of operations per transaction. You can read more about it in
the [Cadence documentation](/cadence).

The gas limit depends on the complexity of the transaction script. Until dedicated gas estimation tooling exists, it's
best to use the emulator to test complex transactions and determine a safe limit.

📖 **Reference block** specifies an expiration window (measured in blocks) during which a transaction is considered
valid by the network. A transaction will be rejected if it is submitted past its expiry block. Flow calculates
transaction expiry using the _reference block_ field on a transaction. A transaction expires after `600` blocks are
committed on top of the reference block, which takes about 10 minutes at average Mainnet block rates. If a reference
block is not specified, before calling `client.execute_transaction`, the latest finalized block will be used as the
reference block.

### Build Transactions

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#transactions)

Building a transaction involves setting the required properties explained above and producing a transaction object.

Here we define a simple transaction script that will be used to execute on the network and serve as a good learning
example.

```
transaction(greeting: String) {

  let guest: Address

  prepare(authorizer: AuthAccount) {
    self.guest = authorizer.address
  }

  execute {
    log(greeting.concat(",").concat(guest.toString()))
  }
}
```

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/transactions_examples.py)
**

```python
transaction = Tx(
    code="""transaction(){prepare(){log("OK")}}""",
    reference_block_id=latest_block.id,
    payer=account_address,
    proposal_key=ProposalKey(
        key_address=account_address,
        key_id=0,
        key_sequence_number=proposer.keys[0].sequence_number,
    )
```

After you have successfully [built a transaction](#build-transactions) the next step in the process is to sign it.

### Sign Transactions

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/signer.md)

Flow introduces new concepts that allow for more flexibility when creating and signing transactions. Before trying the
examples below, we recommend that you read through
the [transaction signature documentation](https://docs.onflow.org/concepts/accounts-and-keys/).

After you have successfully [built a transaction](#build-transactions) the next step in the process is to sign it. Flow
transactions have envelope and payload signatures, and you should learn about each in
the [signature documentation](https://docs.onflow.org/concepts/accounts-and-keys/#anatomy-of-a-transaction).

Quick example of building a transaction:

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        account_address, _, new_signer = await random_account(
            client=client, ctx=ctx
        )
        latest_block = await client.get_latest_block()
        proposer = await client.get_account_at_latest_block(
            address=account_address.bytes
        )

        transaction = Tx(
            code="""transaction(){prepare(){log("OK")}}""",
            reference_block_id=latest_block.id,
            payer=account_address,
            proposal_key=ProposalKey(
                key_address=account_address,
                key_id=0,
                key_sequence_number=proposer.keys[0].sequence_number,
            ),
        )
```

Signatures can be generated more securely using keys stored in a hardware device such as
an [HSM](https://en.wikipedia.org/wiki/Hardware_security_module). The `crypto.Signer` interface is intended to be
flexible enough to support a variety of signer implementations and is not limited to in-memory implementations.

Simple signature example:

```python
async def run(self, ctx: Config):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        account_address, _, new_signer = await random_account(
            client=client, ctx=ctx
        )
        latest_block = await client.get_latest_block()
        proposer = await client.get_account_at_latest_block(
            address=account_address.bytes
        )

        transaction = Tx(
            code="""transaction(){prepare(){log("OK")}}""",
            reference_block_id=latest_block.id,
            payer=account_address,
            proposal_key=ProposalKey(
                key_address=account_address,
                key_id=0,
                key_sequence_number=proposer.keys[0].sequence_number,
            ),
        ).with_envelope_signature(
            account_address,
            0,
            new_signer,
        )
```

Flow supports great flexibility when it comes to transaction signing, we can define multiple authorizers (multi-sig
transactions) and have different payer account than proposer. We will explore advanced signing scenarios bellow.

### [Single party, single signature](https://docs.onflow.org/concepts/transaction-signing/#single-party-single-signature)

- Proposer, payer and authorizer are the same account (`0x01`).
- Only the envelope must be signed.
- Proposal key must have full signing weight.

| Account | Key ID | Weight |
|---------|--------|--------|
| `0x01`  | 1      | 1.0    |

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/transactions_examples.py)
**

```python
async def run(self, ctx: Config):
    address = Address.from_hex("0x01")
    account = await client.get_account(address=address)
    # Assume you stored private key somewhere safe and restore it in private_key.
    signer = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                             sign_algo=sign_algo,
                                             private_key_hex=private_key.to_string().hex())
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        latest_block = await client.get_latest_block()

        tx = Tx(
            code="""
                    transaction {
                        prepare(signer: AuthAccount) { log(signer.address) }
                    }
                """,
            reference_block_id=latest_block.id,
            payer=account.address,
            proposal_key=ProposalKey(
                key_address=account.address,
                key_id=0,
                key_sequence_number=account.keys[
                    0
                ].sequence_number,
            ),
        ).add_authorizers([account.address])
        .with_envelope_signature(
            account.address,
            0,
            signer,
        )
```

### [Single party, multiple signatures](https://docs.onflow.org/concepts/transaction-signing/#single-party-multiple-signatures)

- Proposer, payer and authorizer are the same account (`0x01`).
- Only the envelope must be signed.
- Each key has weight 0.5, so two signatures are required.

| Account | Key ID | Weight |
|---------|--------|--------|
| `0x01`  | 1      | 0.5    |
| `0x01`  | 2      | 0.5    |

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/transactions_examples.py)
**

```python
async def run(self, ctx: Config):
    address = Address.from_hex("0x01")
    account = await client.get_account(address=address)
    # Assume you stored private key somewhere safe and restore it in private_key.
    signer1 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key1.to_string().hex())
    signer2 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key2.to_string().hex())
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        latest_block = await client.get_latest_block()

        tx = Tx(
            code="""
                    transaction {
                        prepare(signer: AuthAccount) { log(signer.address) }
                    }
                """,
            reference_block_id=latest_block.id,
            payer=account.address,
            proposal_key=ProposalKey(
                key_address=account.address,
                key_id=0,
                key_sequence_number=account.keys[
                    0
                ].sequence_number,
            ),
        ).add_authorizers([account.address])
        .with_envelope_signature(
            account.address,
            0,
            signer1,
        ).with_envelope_signature(
            account.address,
            1,
            signer2,
        )
```

### [Multiple parties](https://docs.onflow.org/concepts/transaction-signing/#multiple-parties)

- Proposer and authorizer are the same account (`0x01`).
- Payer is a separate account (`0x02`).
- Account `0x01` signs the payload.
- Account `0x02` signs the envelope.
    - Account `0x02` must sign last since it is the payer.

| Account | Key ID | Weight |
|---------|--------|--------|
| `0x01`  | 1      | 1.0    |
| `0x02`  | 3      | 1.0    |

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/trasnactions_examples.py)
**

```python
async def run(self, ctx: Config):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    address1 = Address.from_hex("0x01")
    address3 = Address.from_hex("0x02")
    account = await client.get_account(address=address)
    # Assume you stored private key somewhere safe and restore it in private_key.
    signer1 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key1.to_string().hex())
    signer3 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key3.to_string().hex())
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        latest_block = await client.get_latest_block()

        tx = Tx(
            code="""
                    transaction {
                        prepare(signer: AuthAccount) { log(signer.address) }
                    }
                """,
            reference_block_id=latest_block.id,
            payer=account3.address,
            proposal_key=ProposalKey(
                key_address=account1.address,
                key_id=0,
                key_sequence_number=account.keys[
                    0
                ].sequence_number,
            ),
        ).add_authorizers([account1.address])
        .with_payload_signature(
            account1.address,
            0,
            signer1,
        ).with_envelope_signature(
            account3.address,
            0,
            signer3,
        )
```

### [Multiple parties, two authorizers](https://docs.onflow.org/concepts/transaction-signing/#multiple-parties)

- Proposer and authorizer are the same account (`0x01`).
- Payer is a separate account (`0x02`).
- Account `0x01` signs the payload.
- Account `0x02` signs the envelope.
    - Account `0x02` must sign last since it is the payer.
- Account `0x02` is also an authorizer to show how to include two AuthAccounts into an transaction

| Account | Key ID | Weight |
|---------|--------|--------|
| `0x01`  | 1      | 1.0    |
| `0x02`  | 3      | 1.0    |

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/transactions_examples.py)
**

```python
async def run(self, ctx: Config):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    address1 = Address.from_hex("0x01")
    address3 = Address.from_hex("0x02")
    account = await client.get_account(address=address)
    # Assume you stored private key somewhere safe and restore it in private_key.
    signer1 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key1.to_string().hex())
    signer3 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key3.to_string().hex())
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        latest_block = await client.get_latest_block()

        tx = Tx(
            code="""
                    transaction {
                        prepare(signer: AuthAccount) { log(signer.address) }
                    }
                """,
            reference_block_id=latest_block.id,
            payer=account3.address,
            proposal_key=ProposalKey(
                key_address=account1.address,
                key_id=0,
                key_sequence_number=account.keys[
                    0
                ].sequence_number,
            ),
        ).add_authorizers([account1.address, account3.address])
        .with_payload_signature(
            account1.address,
            0,
            signer1,
        ).with_envelope_signature(
            account3.address,
            0,
            signer3,
        )
```

### [Multiple parties, multiple signatures](https://docs.onflow.org/concepts/transaction-signing/#multiple-parties)

- Proposer and authorizer are the same account (`0x01`).
- Payer is a separate account (`0x02`).
- Account `0x01` signs the payload.
- Account `0x02` signs the envelope.
    - Account `0x02` must sign last since it is the payer.
- Both accounts must sign twice (once with each of their keys).

| Account | Key ID | Weight |
|---------|--------|--------|
| `0x01`  | 1      | 0.5    |
| `0x01`  | 2      | 0.5    |
| `0x02`  | 3      | 0.5    |
| `0x02`  | 4      | 0.5    |

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/transactions_examples.py)
**

```python
async def run(self, ctx: Config):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    address1 = Address.from_hex("0x01")
    address3 = Address.from_hex("0x02")
    account = await client.get_account(address=address)
    # Assume you stored private key somewhere safe and restore it in private_key.
    signer1 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key1.to_string().hex())
    signer2 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key2.to_string().hex())
    signer3 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key3.to_string().hex())
    signer4 = in_memory_signer.InMemorySigner(hash_algo=hash_algo,
                                              sign_algo=sign_algo,
                                              private_key_hex=private_key4.to_string().hex())
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        latest_block = await client.get_latest_block()

        tx = Tx(
            code="""
                    transaction {
                        prepare(signer: AuthAccount) { log(signer.address) }
                    }
                """,
            reference_block_id=latest_block.id,
            payer=account2.address,
            proposal_key=ProposalKey(
                key_address=account1.address,
                key_id=0,
                key_sequence_number=account.keys[
                    0
                ].sequence_number,
            ),
        ).add_authorizers([account1.address])
        .with_payload_signature(
            account1.address,
            0,
            signer1,
        ).with_payload_signature(
            account1.address,
            1,
            signer2,
        ).with_envelope_signature(
            account3.address,
            0,
            signer3,
        ).with_envelope_signature(
            account3.address,
            1,
            signer4,
        )
```

### Signing user messages

Signing and verifying user messages can be done by using `Signer.sign_user_message`. Verifying that an account (via its
owners keys) has been signed can be done with `utils.verify_user_signature`

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/user_message_examples.py)
**

Short sample:

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        # create account
        account_address, _, account_signer = await random_account(
            client=client,
            ctx=ctx,
        )

        # the message to sign. Could include some extra information, like the reference block id or the address.
        message = b"Hello World!"

        # sign message
        signature = account_signer.sign_user_message(message)
        c_signature = utils.CompositeSignature(
            account_address.hex(), 0, signature.hex()
        )

        # verify the signature is valid
        signature_is_valid = await utils.verify_user_signature(
            message=message,
            client=client,
            composite_signatures=[c_signature],
        )

        assert signature_is_valid
```

### Send Transactions

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/client.md#transactions)

After a transaction has been [built](#build-transactions) and [signed](#sign-transactions), it can be sent to the Flow
blockchain where it will be executed. If sending was successful you can
then [retrieve the transaction result](#get-transactions).

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/transactions_examples.py)
**

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        account_address, _, new_signer = await random_account(
            client=client, ctx=ctx
        )
        latest_block = await client.get_latest_block()
        proposer = await client.get_account_at_latest_block(
            address=account_address.bytes
        )

        transaction = Tx(
            code="""transaction(){prepare(){log("OK")}}""",
            reference_block_id=latest_block.id,
            payer=account_address,
            proposal_key=ProposalKey(
                key_address=account_address,
                key_id=0,
                key_sequence_number=proposer.keys[0].sequence_number,
            ),
        ).with_envelope_signature(
            account_address,
            0,
            new_signer,
        )

        response = await client.send_transaction(transaction=transaction.to_signed_grpc())
```

### Create Accounts

*
*[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/try.svg" width="130"/>](https://github.com/janezpodhostnik/flow-py-sdk/blob/master/examples/account_examples.py)
**

On Flow, account creation happens inside a transaction. Because the network allows for a many-to-many relationship
between public keys and accounts, it's not possible to derive a new account address from a public key offline.

The Flow VM uses a deterministic address generation algorithm to assigen account addresses on chain. You can find more
details about address generation in
the [accounts & keys documentation](https://docs.onflow.org/concepts/accounts-and-keys/).

#### Public Key

Flow uses ECDSA key pairs to control access to user accounts. Each key pair can be used in combination with the SHA2-256
or SHA3-256 hashing algorithms.

⚠️ You'll need to authorize at least one public key to control your new account.

Flow represents ECDSA public keys in raw form without additional metadata. Each key is a single byte slice containing a
concatenation of its X and Y components in big-endian byte form.

A Flow account can contain zero (not possible to control) or more public keys, referred to as account keys. Read more
about [accounts in the documentation](https://docs.onflow.org/concepts/accounts-and-keys/#accounts).

An account key contains the following data:

- Raw public key (described above)
- Signature algorithm
- Hash algorithm
- Weight (integer between 0-1000)

Account creation happens inside a transaction, which means that somebody must pay to submit that transaction to the
network. We'll call this person the account creator. Make sure you have
read [sending a transaction section](#send-transactions) first.

```python
async def run(self, ctx: Config):
    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        latest_block = await client.get_latest_block()
        proposer = await client.get_account_at_latest_block(address=ctx.service_account_address.bytes)

        tx = (
            create_account_template(
                keys=[account_key],
                reference_block_id=latest_block.id,
                payer=ctx.service_account_address,
                proposal_key=ProposalKey(
                    key_address=ctx.service_account_address,
                    key_id=ctx.service_account_key_id,
                    key_sequence_number=proposer.keys[
                        ctx.service_account_key_id
                    ].sequence_number,
                ),
            )
            .add_authorizers(ctx.service_account_address)
            .with_envelope_signature(
                ctx.service_account_address, 0, ctx.service_account_signer
            )
        )
        result = await client.execute_transaction(tx)

        print("new address event:\n")
        print(result.__dict__)
        print("\nCreating account : successfully done...")
```

After the account creation transaction has been submitted you can retrieve the new account address
by [getting the transaction result](#get-transactions).

The new account address will be emitted in a system-level `flow.AccountCreated` event.

await client.get_events_for_block_i_ds(
type="flow.AccountCreated", block_ids=[latest_block.id]
)

### Contracts

Flow smart contracts are Codance scripts that run on Flow blockchain and can returns values. a contract can be add,
update or remove from an account.

A contracts contains the following fields:

- `Name` - Name of contract.
- `source` - Script of contract.

## Adding a contract to an account

```python
async def run(self, ctx: Config):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    # A test Contract define for this example, you can modify it by your self
    contract = {
        "Name": "TestOne",
        "source": '''pub contract TestOne {
                            pub fun add(a: Int, b: Int): Int {
                                return a + b
                            }
                            }'''
    }
    contract_source_hex = bytes(contract["source"], "UTF-8").hex()

    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        account_address, account_key, new_signer = await random_account(client=client, ctx=ctx)
    latest_block = await client.get_latest_block()
    cadenceName = cadence.String(contract["Name"])
    cadenceCode = cadence.String(contract_source_hex)
    tx = (
        Tx(
            code=addAccountContractTemplate,
            reference_block_id=latest_block.id,
            payer=account_address,
        ).add_arguments(cadenceName)
        .add_arguments(cadenceCode)
        .add_authorizers([account_address])
        .with_envelope_signature(
            account_address,
            0,
            new_signer,
        )
    )

    result = await client.execute_transaction(tx)

```

## Updating a contract of an account

```python
async def run(self, ctx: Config):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    # A test Contract define for this example, you can modify it by your self
    contract = {
        "Name": "TestOne",
        "source": '''pub contract TestOne {
                            pub fun add(a: Int, b: Int): Int {
                                return a + b
                            }
                            }'''
    }
    contract_source_hex = bytes(contract["source"], "UTF-8").hex()

    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        account_address, account_key, new_signer = await random_account(client=client, ctx=ctx)
        latest_block = await client.get_latest_block()
        cadenceName = cadence.String(contract["Name"])
        cadenceCode = cadence.String(contract_source_hex)
        tx = (
            Tx(
                code=addAccountContractTemplate,
                reference_block_id=latest_block.id,
                payer=account_address,
            ).add_arguments(cadenceName)
            .add_arguments(cadenceCode)
            .add_authorizers([account_address])
            .with_envelope_signature(
                account_address,
                0,
                new_signer,
            )
        )

        result = await client.execute_transaction(tx)

        latest_block = await client.get_latest_block()
        # Updated Contract
        contract = {
            "Name": "TestOne",
            "source": '''pub contract TestOne {
                            pub fun add(a: Int, b: Int): Int {
                                return a * b
                            }
                            }'''
        }
        contract_source_hex = bytes(contract["source"], "UTF-8").hex()
        # Update account contract with a transaction
        tx = (
            Tx(
                code=updateAccountContractTemplate,
                reference_block_id=latest_block.id,
                payer=account_address,
            ).add_arguments(contract["Name"])
            .add_arguments(contract_source_hex)
            .add_authorizers([account_address])
            .with_envelope_signature(
                account_address,
                0,
                new_signer,
            )
        )

        result = await client.execute_transaction(tx)

```

## Removing a contract from an account

```python
async def run(self, ctx: Config):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    # A test Contract define for this example, you can modify it by your self
    contract = {
        "Name": "TestOne",
        "source": '''pub contract TestOne {
                            pub fun add(a: Int, b: Int): Int {
                                return a + b
                            }
                            }'''
    }
    contract_source_hex = bytes(contract["source"], "UTF-8").hex()

    async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        account_address, account_key, new_signer = await random_account(client=client, ctx=ctx)
        latest_block = await client.get_latest_block()
        cadenceName = cadence.String(contract["Name"])
        cadenceCode = cadence.String(contract_source_hex)
        tx = (
            Tx(
                code=addAccountContractTemplate,
                reference_block_id=latest_block.id,
                payer=account_address,
            ).add_arguments(cadenceName)
            .add_arguments(cadenceCode)
            .add_authorizers([account_address])
            .with_envelope_signature(
                account_address,
                0,
                new_signer,
            )
        )

        result = await client.execute_transaction(tx)

        # Delete the added contract from the account

        latest_block = await client.get_latest_block()

        tx = (
            Tx(
                code=removeAccountContractTemplate,
                reference_block_id=latest_block.id,
                payer=account_address,
            ).add_arguments(cadenceName)
            .add_authorizers([account_address])
            .with_envelope_signature(
                account_address,
                0,
                new_signer,
            )
        )

        result = await client.execute_transaction(tx)

```

### Generate Keys

[<img src="https://raw.githubusercontent.com/onflow/sdks/main/templates/documentation/ref.svg" width="130"/>](./api_docs/keys.md#generate-new-keys)

Flow uses [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) signatures to control access
to user accounts. Each key pair can be used in combination with the `SHA2-256` or `SHA3-256` hashing algorithms.

Here's how to generate an ECDSA private key for the P-256 (secp256r1) curve.

```python
private_key = ecdsa.SigningKey.generate(curve="ECDSA_secp256k1")
public_key = sk.verifying_key.to_string()
```

The example above uses an ECDSA key pair on the P-256 (secp256r1) elliptic curve. Flow also supports the secp256k1 curve
used by Bitcoin and Ethereum. Read more
about [supported algorithms here](https://docs.onflow.org/concepts/accounts-and-keys/#supported-signature--hash-algorithms).
