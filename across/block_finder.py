from typing import Callable, Optional, Union
from web3.types import BlockData
from web3 import Web3
from .utils import sorted_index_by


def average_block_time_seconds(lookbackSeconds: Optional[int]=1, networkId: Optional[int]=1) -> float:
    # Return average block-time for a period.
    # TODO: Call an external API to get this data. Currently this value is a hard-coded estimate
    # based on the data from https://etherscan.io/chart/blocktime. ~13.5 seconds has been the average
    # since April 2016, although this value seems to spike periodically for a relatively short period of time.
    defaultBlockTimeSeconds = 13.5
    if not defaultBlockTimeSeconds:
        raise Exception("Missing default block time value")

    if networkId == 137:
        # Source: https://polygonscan.com/chart/blocktime
        return 2.5
    elif networkId == 1:
        return defaultBlockTimeSeconds
    else:
        return defaultBlockTimeSeconds


def estimate_blocks_elapsed(seconds: int, cushionPercentage=0.0) -> int:
    cushionMultiplier = cushionPercentage + 1.0
    averageBlockTime = average_block_time_seconds()
    # FIXME: if need floow
    return int((seconds * cushionMultiplier) // averageBlockTime)


class BlockFinder:
    def __init__(self, provider, request_block: Callable) -> None:
        self.provider = provider
        self.w3 = Web3(provider=provider)
        self.request_block = request_block
        self.blocks = []

    def get_block_for_timestamp(
        self, timestamp: Union[int, str]
    ) -> Optional[BlockData]:
        """Gets the latest block whose timestamp is less than the provided timestamp.

        Args:
            timestamp (int): timestamp in seconds of latest block on L2 chain.

        Returns:
            Optional[BlockData]: latest block whose timestamp is less than the provided timestamp.
        """
        timestamp = int(timestamp)
        assert timestamp is not None, "timestamp must be provided"
        # If the last block we have stored is too early, grab the latest block.
        if len(self.blocks) == 0 or self.blocks[-1].timestamp < timestamp:
            block = self.get_latest_block()
            if block and timestamp >= block.timestamp:
                return block
        # Check the first block. If it's grater than our timestamp, we need to find an earlier block.
        if len(self.blocks) > 0 and self.blocks[0].timestamp > timestamp:
            initial_block = self.blocks[0]
            cushion = 1.1
            # Ensure the increment block distance is _at least_ a single block to prevent an infinite loop.
            increment_distance = max(
                estimate_blocks_elapsed(
                    initial_block.timestamp - timestamp, cushion
                ),
                1,
            )

            # Search backwards by a constant increment until we find a block before the timestamp or hit block 0.
            multiplier = 1
            while True:
                distance = multiplier * increment_distance
                block_bumber = max(0, initial_block.number - distance)
                block = self.get_block(block_bumber)
                if block.timestamp <= timestamp:
                    break  # Found an earlier block.
                assert block_bumber > 0, "timestamp is before block 0"
                multiplier += 1
        index = sorted_index_by(self.blocks, timestamp, "timestamp")
        return self.find_block(
            self.blocks[index - 1], self.blocks[index], timestamp
        )

    def get_latest_block(self) -> BlockData:
        # Grabs the most recent block and caches it.
        block = self.request_block("latest")
        index = sorted_index_by(self.blocks, block, "number")
        if index > len(self.blocks) - 1 or self.blocks[index].number != block.number:
            self.blocks.insert(index, block)
        return self.blocks[index]

    def get_block(self, number: int) -> BlockData:
        # Grabs the block for a particular number and caches it.
        index = sorted_index_by(self.blocks, number, "number")
        if index > len(self.blocks) - 1 and self.blocks[index].number == number:
            return self.blocks[index]  # Return early if block already exists.
        block = self.request_block(number)
        self.blocks.insert(index, block) # A simple insert at index.
        return block

    def find_block(
        self, start_block: BlockData, end_block: BlockData, timestamp: int
    ) -> BlockData:
        # In the case of equality, the end_block is expected to be passed as the one whose timestamp === the requested
        # timestamp.
        if end_block.timestamp == timestamp:
            return end_block

        # If there's no equality, but the blocks are adjacent, return the start_block, since we want the returned block's
        # timestamp to be <= the requested timestamp.
        if end_block.number == start_block.number + 1:
            return start_block

        assert (
            end_block.number != start_block.number
        ), "start_block cannot equal end_block"
        assert (
            timestamp < end_block.timestamp
            and timestamp > start_block.timestamp
        ), "timestamp not in between start and end blocks"

        # Interpolating the timestamp we're searching for to block numbers.
        total_time_difference = end_block.timestamp - start_block.timestamp
        total_block_distance = end_block.number - start_block.number
        block_percentile = (
            timestamp - start_block.timestamp
        ) / total_time_difference
        estimated_block = start_block.number + round(
            block_percentile * total_block_distance
        )

        # Clamp ensures the estimated block is strictly greater than the start block and strictly less than the end block.
        clamp = lambda v, minv, maxv: max(min(v, maxv), minv)
        new_block = self.get_block(
            clamp(estimated_block, start_block.number + 1, end_block.number - 1)
        )

        # Depending on whether the new block is below or above the timestamp, narrow the search space accordingly.
        if new_block.timestamp < timestamp:
            return self.find_block(new_block, end_block, timestamp)
        else:
            return self.find_block(start_block, new_block, timestamp)
