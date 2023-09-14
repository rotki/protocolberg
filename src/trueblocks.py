from rotkehlchen.chain.evm.types import string_to_evm_address

from rotki_conf import msg_aggregator
from lib.trueblocks import Trueblocks

trueblocks = Trueblocks(
    endpoint='http://localhost:8080',
    msg_aggregator=msg_aggregator,
)


# print(trueblocks.get_block_timestamp(213444))
# print(trueblocks.get_transactions_by_hash(['0x05da328841fccf475de11a731036b8cb10f7245a8f82f2c17a0c9cff41154995']))
data = trueblocks.get_transactions(
    addrs=string_to_evm_address('0xc37b40ABdB939635068d3c5f13E7faF686F03B65'),
    first_block=15546236,
    last_block=17826050,
)
print(data)