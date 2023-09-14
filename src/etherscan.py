from rotki_conf import db, msg_aggregator
from rotkehlchen.chain.ethereum.etherscan import EthereumEtherscan


etherscan = EthereumEtherscan(database=db, msg_aggregator=msg_aggregator)
data = etherscan._query(
    module='account',
    action='txlist',
    options={'sort': 'asc', 'address': '0xc37b40ABdB939635068d3c5f13E7faF686F03B65', 'startBlock': 15546236},
)

print(data[-1])