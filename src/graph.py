from rotki_conf import db, msg_aggregator
from rotkehlchen.chain.ethereum.modules.balancer import Balancer
from rotkehlchen.chain.evm.types import string_to_evm_address
from rotkehlchen.types import Timestamp
from rotkehlchen.utils.misc import ts_now

balancer = Balancer(
    ethereum_inquirer=None,
    database=db,
    premium=None,
    msg_aggregator=msg_aggregator,
)

data = balancer._get_address_to_events_data(
    addresses=[string_to_evm_address('0x7716a99194d758c8537F056825b75Dd0C8FDD89f')],
    from_timestamp=Timestamp(0),
    to_timestamp=ts_now(),
)
