from typing import Optional
from .utils import BigNumberish
from .fee_calculator import calculate_realized_lp_fee_pct
from .rate_model import parse_and_return_rate_model_from_string
from .clients import BridgePool, RateModelStore
from .block_finder import BlockFinder
from web3 import Web3

__all__ = ["LpFeeCalculator"]


class LpFeeCalculator:
    def __init__(self, provider) -> None:
        self.provider = provider
        self.w3 = Web3(provider=provider)
        self.block_finder = BlockFinder(provider, self.w3.eth.get_block)

    def get_lp_fee_pct(
        self,
        token_address: str,
        bridge_pool_address: str,
        amount: BigNumberish,
        timestamp: Optional[int] = None,
    ) -> int:
        """Estimate LP Fees charged for a relay from L2 -> L1

        Args:
            token_address (str): token address on L1 to transfer from l2 to l1
            bridge_pool_address (str): bridge pool address on L1 with the liquidity pool
            amount (BigNumberish): amount in wei for user to send across
            timestamp (Optional[int], optional): timestamp in seconds of latest block on L2 chain. Defaults to None.

        Returns:
            int: estimated LP Fees in wei charged for a relay from L2 -> L1
        
        Raises:
            AcrossException:
                - Unable to find target block for timestamp
                - Amount must be greater than 0
        """
        amount = int(amount)
        assert amount > 0, "Amount must be greater than 0"

        bridge_pool_instance = BridgePool.connect(
            bridge_pool_address, self.provider
        )
        rate_model_store_address = RateModelStore().get_address(self.w3.eth.chain_id)
        rate_model_store_instance = RateModelStore.connect(
            rate_model_store_address, self.provider
        )

        if timestamp is not None:
            targetBlock = self.block_finder.get_block_for_timestamp(timestamp)
        else:
            targetBlock = self.w3.eth.get_block("latest")
        assert targetBlock is not None, (
            "Unable to find target block for timestamp: " + \
                timestamp or "latest"
        )
        blockTag = targetBlock.number

        results = [
            bridge_pool_instance.functions.liquidityUtilizationCurrent().call({"blockTag": blockTag}),
            bridge_pool_instance.functions.liquidityUtilizationPostRelay(amount).call(
                {"blockTag": blockTag}
            ),
            rate_model_store_instance.functions.l1TokenRateModels(token_address).call(
                {"blockTag": blockTag}
            ),
        ]
        [currentUt, nextUt, rate_model_for_block_height] = results

        # Parsing stringified rate model will error if the rate model doesn't contain exactly the expected keys or isn't
        # a JSON object.
        rateModel = parse_and_return_rate_model_from_string(
            rate_model_for_block_height
        )

        return calculate_realized_lp_fee_pct(rateModel, currentUt, nextUt)
