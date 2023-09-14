from json import JSONDecodeError
import logging
from multiprocessing.managers import RemoteError
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import requests
from rotkehlchen.logging import RotkehlchenLogsAdapter

from rotkehlchen.types import EVMTxHash, Timestamp, ChecksumEvmAddress
from rotkehlchen.utils.serialization import jsonloads_dict


if TYPE_CHECKING:
    from rotkehlchen.user_messages import MessagesAggregator


logger = logging.getLogger(__name__)
log = RotkehlchenLogsAdapter(logger)

class Trueblocks:

    def __init__(self, endpoint: str, msg_aggregator: 'MessagesAggregator') -> None:
        self.endpoint = endpoint
        self.session = requests.session()
        self.msg_aggregator = msg_aggregator

    def get_transactions_by_hash(self, tx_hashes: List[str]) -> List[Dict[str, Any]]:
        """
        Gets a transaction object by hash.
        May raise:
        - RemoteError if reading the information from the trueblocks server failed
        """
        return self._query(
            method='transactions',
            params={'transactions': ','.join(tx_hashes)},
        )

    def get_block_timestamp(self, block_numer: int) -> Timestamp:
        """
        Given a block number return the timestmap for the block
        May raise:
        - RemoteError if reading the information from the trueblocks server 
        - KeyError if the response doesn't contain the timestamp attribute
        """
        response = self._query(
            method='when',
            params={
                'timestamps': 'true',
                'blocks': block_numer,
            },
        )
        return response[0]['timestamp']

    def get_transactions(self, addrs: ChecksumEvmAddress, first_block: int, last_block: int) -> dict[str, Any]:
        return self._query(
            method='export',
            params={
                'addrs': addrs,
                'firstBlock': first_block,
                'lastBlock': last_block,
            },
        )

    def is_available(self):
        return True

    def _query(
            self,
            method: str,
            params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        try:
            response = self.session.get(f'{self.endpoint}/{method}', params=params)
        except requests.exceptions.RequestException as e:
            self.msg_aggregator.add_error(f'Failed to query trueblocks node due to {e}')

        if response.status_code != 200:
            raise RemoteError(
                f'Trueblocks query to {response.url} failed with code {response.status_code} and'
                f'text {response.text}',
            )
        
        try:
            json_response = jsonloads_dict(response.text)
        except JSONDecodeError as e:
            raise RemoteError(f'Failed to read json response {response.text}') from e
        
        try:
            result = json_response.get('data')
        except KeyError as e:
            raise RemoteError('Failed to obtain data from the trueblocks response')
        
        return result