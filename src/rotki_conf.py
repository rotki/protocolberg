from pathlib import Path
from gevent import monkey
monkey.patch_all()  # isort:skip # noqa

from rotkehlchen.chain.evm.types import NodeName  # isort:skip # noqa

from rotkehlchen.config import default_data_directory
from rotkehlchen.logging import TRACE, add_logging_level
from rotkehlchen.globaldb.handler import GlobalDBHandler
from rotkehlchen.user_messages import MessagesAggregator
from rotkehlchen.externalapis.coingecko import Coingecko
from rotkehlchen.externalapis.cryptocompare import Cryptocompare
from rotkehlchen.externalapis.defillama import Defillama
from rotkehlchen.history.price import PriceHistorian
from rotkehlchen.globaldb.manual_price_oracles import ManualCurrentOracle
from rotkehlchen.inquirer import Inquirer
from rotkehlchen.db.dbhandler import DBHandler
from rotkehlchen.history.types import DEFAULT_HISTORICAL_PRICE_ORACLES_ORDER
from rotkehlchen.oracles.structures import DEFAULT_CURRENT_PRICE_ORACLES_ORDER

add_logging_level('TRACE', TRACE)

import os

from rotkehlchen.errors.misc import InputError


USERNAME_VAR = 'ROTKI_USERNAME'
PASSWORD_VAR = 'ROTKI_PASSWORD'


username = os.environ.get(USERNAME_VAR, '0xaf14')
password = os.environ.get(PASSWORD_VAR, '0xaf14')

if None in (username, password):
    msg = f'Failed to get either {USERNAME_VAR} or {PASSWORD_VAR}'
    print(msg)
    raise InputError(msg)

assert username is not None
assert password is not None


# Obtain users database
if 'PROD' in os.environ:
    data_dir = Path('./data')
else:
    data_dir = Path('/usr/src/app/data')

user_data_dir = data_dir / username
user_data_dir.mkdir(exist_ok=True, parents=True)

GlobalDBHandler(data_dir=data_dir, sql_vm_instructions_cb=0)

# Initialize things needed by rotki
msg_aggregator = MessagesAggregator()

db = DBHandler(
    user_data_dir=data_dir / username,
    password=password,
    msg_aggregator=msg_aggregator,
    initial_settings=None,
    sql_vm_instructions_cb=0,
    resume_from_backup=False,
)
cryptocompare = Cryptocompare(data_directory=data_dir, database=db)
coingecko = Coingecko()
price_historian = PriceHistorian(
    data_directory=data_dir,
    cryptocompare=cryptocompare,
    coingecko=coingecko,
    defillama=Defillama(),
)
PriceHistorian().set_oracles_order(DEFAULT_HISTORICAL_PRICE_ORACLES_ORDER)
inquirer = Inquirer(
    data_dir=data_dir,
    cryptocompare=cryptocompare,
    coingecko=coingecko,
    defillama=Defillama(),
    manualcurrent=ManualCurrentOracle(),
    msg_aggregator=msg_aggregator,
)
Inquirer().set_oracles_order(DEFAULT_CURRENT_PRICE_ORACLES_ORDER)
