import math
from decimal import Decimal
from typing import Dict
from web3 import Web3
from across.utils import BigNumberish, toBNWei, fixedPointAdjustment


__all__ = [
    "calculate_instantaneous_rate",
    "calculate_apy_from_utilization",
    "calculate_realized_lp_fee_pct",
]
RateModel = Dict[str, int]


def calculate_instantaneous_rate(
    rate_model: RateModel, utilization: BigNumberish
):
    """Calculate the rate for a 0 sized deposit (infinitesimally small)."""

    before_kink = (
        min(utilization, rate_model["UBar"])
        * rate_model["R1"]
        // rate_model["UBar"]
    )
    after_kink = (
        max(0, utilization - rate_model["UBar"])
        * rate_model["R2"]
        // (toBNWei("1") - rate_model["UBar"])
    )

    return rate_model["R0"] + before_kink + after_kink


def calculate_area_under_rate_curve(
    rate_model: RateModel, utilization: int
) -> int:
    """Compute area under curve of the piece-wise linear rate model.
    """
    
    # Area under first piecewise component
    utilization_before_kink = min(utilization, rate_model["UBar"])
    rectangle1_area = (
        utilization_before_kink * rate_model["R0"] // fixedPointAdjustment
    )
    triangle1_area = (
        toBNWei("0.5")
        * (
            calculate_instantaneous_rate(rate_model, utilization_before_kink)
            - rate_model["R0"]
        )
        * utilization_before_kink
        // fixedPointAdjustment
        // fixedPointAdjustment
    )

    # Area under second piecewise component
    utilization_after = max(0, utilization - rate_model["UBar"])
    rectangle2_area = (
        utilization_after
        * (rate_model["R0"] + rate_model["R1"])
        // fixedPointAdjustment
    )
    triangle2_area = (
        toBNWei("0.5")
        * (
            calculate_instantaneous_rate(rate_model, utilization)
            - (rate_model["R0"] + rate_model["R1"])
        )
        * utilization_after
        // fixedPointAdjustment
        // fixedPointAdjustment
    )
    return rectangle1_area + triangle1_area + rectangle2_area + triangle2_area


def convert_apy_to_weekly_fee(apy: int) -> str:
    """converts an APY rate to a one week rate.
    Uses the Decimal library to take a fractional exponent
    """

    # R_week = (1 + apy)^(1/52) - 1
    weeklyFeePct = (Decimal("1.0") + Web3.fromWei(apy, "ether")) ** (
        Decimal("1.0") / Decimal("52.0")
    ) - Decimal(1.0)
    # Convert from decimal back to BN, scaled by 1e18.
    return math.floor(weeklyFeePct * fixedPointAdjustment)


def calculate_apy_from_utilization(
    rate_model, utilization_before_deposit: int, utilization_after_deposit: int
) -> int:
    """Calculate the realized yearly LP Fee APY Percent for a given rate model, 
    utilization before and after the deposit.
    """
    if utilization_before_deposit == utilization_after_deposit:
        raise Exception("Deposit cant have zero size")
    area_before_deposit = calculate_area_under_rate_curve(
        rate_model, utilization_before_deposit
    )
    area_after_deposit = calculate_area_under_rate_curve(
        rate_model, utilization_after_deposit
    )
    numerator = area_after_deposit - area_before_deposit
    denominator = utilization_after_deposit - utilization_before_deposit
    return numerator * fixedPointAdjustment // denominator


def calculate_realized_lp_fee_pct(
    rate_model,
    utilization_before_deposit: BigNumberish,
    utilization_after_deposit: BigNumberish,
):
    apy = calculate_apy_from_utilization(
        rate_model, utilization_before_deposit, utilization_after_deposit
    )
    return convert_apy_to_weekly_fee(apy)
