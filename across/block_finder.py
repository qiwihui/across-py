from typing import Optional
from web3.types import BlockData
from web3 import Web3


class BlockFinder:

    def __init__(self, provider) -> None:
        self.provider = provider
        self.w3 = Web3(provider=provider)

    def get_block_for_timestamp(self, timestamp: int) -> Optional[BlockData]:
        """Gets the latest block whose timestamp is less than the provided timestamp.

        Args:
            timestamp (int): timestamp in seconds of latest block on L2 chain.

        Returns:
            Optional[BlockData]: latest block whose timestamp is less than the provided timestamp.
        """
        raise NotImplementedError()
        # return self.w3.eth.getBlock('latest')
