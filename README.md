# The problem of historical data availability in EVM chains

<p align="center">
<img src="https://raw.githubusercontent.com/rotki/rotki/develop/frontend/app/public/assets/images/rotkehlchen_no_text.png" alt="An open source portfolio tracker, accounting and analytics tool that protects your privacy" width="250">
</p>

The problem of historical data availability is in EVM chains, why it exists and how we can try to tackle it.

## Prerequisites

- Python 3.10 or
- Docker

## Performing queries

### Querying the node

#### Querying a node for your balance

```bash
curl -X POST --header "Content-Type: application/json" \
--data '{"jsonrpc":"2.0","method":"eth_getBalance","params":["0xc37b40ABdB939635068d3c5f13E7faF686F03B65", "latest"],"id":1}' \
https://eth.llamarpc.com
```

#### Querying a transaction by hash

> Check [getTransactionByHash](https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_gettransactionbyhash)

```bash
curl -X POST --header "Content-Type: application/json" \
--data '{"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":["0x05da328841fccf475de11a731036b8cb10f7245a8f82f2c17a0c9cff41154995"],"id":1}' \
https://eth.llamarpc.com
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "blockHash": "0xe9a750e11ab6ea2cbb65c0d36304c280953a47bfbe71f3590ec7642bc0831b6d",
    "blockNumber": "0x114b352",
    "from": "0x3f52c7ab2f23223e0338943db61caa6700d54db3",
    "gas": "0x36945",
    "gasPrice": "0x256f43775",
    "maxPriorityFeePerGas": "0x14e427b",
    "maxFeePerGas": "0x2d8558554",
    "hash": "0x05da328841fccf475de11a731036b8cb10f7245a8f82f2c17a0c9cff41154995",
    "input": "0x3593564c000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000006502e3530000000000000000000000000000000000000000000000000000000000000002000c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000e3ada1334cc6a8fbad7000000000000000000000000000000000000000000000000013dc735c6f75f8200000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002bbe042e9d09cb588331ff911c2b46fd833a3e5bd6002710c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000013dc735c6f75f82",
    "nonce": "0x14",
    "to": "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",
    "transactionIndex": "0x89",
    "value": "0x0",
    "type": "0x2",
    "accessList": [],
    "chainId": "0x1",
    "v": "0x1",
    "r": "0x2a9ac96b560aaf028282274d9775dffd2328a473d6392e1bbc61059398213f9b",
    "s": "0x49b7062b59851aca394b5d9cf2db05372b7cb0bf4e2f3b2bce44bb57627d41d7"
  }
}
```


#### Querying logs

```bash
curl -X POST --header "Content-Type: application/json" \
--data '{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["0x05da328841fccf475de11a731036b8cb10f7245a8f82f2c17a0c9cff41154995"],"id":1}' \
https://eth.llamarpc.com
```

### Using indexers

We have created a small set of scripts that you can execute to obtain different information from indexers. They are based on the [rotki](https://github.com/rotki/rotki) codebase.


#### Setting up the works

1. Clone the repo at [github](https://github.com/yabirgb/protocolberg)
2. Setup the environment
   2.1 Using virtualenv. It requires python 3.10
    ```
    $ python3.10 -m venv env
    $ source env/bin/activate
    $ pip install .
    ```
2.2 Using Docker
```
$ docker build -t rwork .
$ docker run rwork
$ docker run rwork python src/etherscan.py
```

#### Querying Etherscan

Check [https://github.com/yabirgb/protocolberg/blob/master/src/etherscan.py](https://github.com/yabirgb/protocolberg/blob/master/src/etherscan.py)

#### Querying TheGraph

Check [https://github.com/yabirgb/protocolberg/blob/master/src/thegraph.py](https://github.com/yabirgb/protocolberg/blob/master/src/thegraph.py)

#### Querying TrueBlocks

1. Configure TrueBlocks. More information at [https://trueblocks.io/tutorials/](https://trueblocks.io/tutorials/)
2. Check [https://github.com/yabirgb/protocolberg/blob/master/src/trueblocks.py](https://github.com/yabirgb/protocolberg/blob/master/src/trueblocks.py)

You can use the following exposed TrueBlocks API during the workshop:

```
https://clean-vertically-oriole.ngrok-free.app
```

