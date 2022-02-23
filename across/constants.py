from typing import TypedDict, Dict


expectedRateModelKeys = ["UBar", "R0", "R1", "R2"]


class RateModel(TypedDict):
    UBar: int  # denote the utilization kink along the rate model where the slope of the interest rate model changes.
    R0: int  # is the interest rate charged at 0 utilization
    R1: int  # R_0+R_1 is the interest rate charged at UBar
    R2: int  # R_0+R_1+R_2 is the interest rate charged at 100% utilization


RATE_MODELS: Dict[str, RateModel] = {
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": {
        "UBar": 650000000000000000,
        "R0": 0,
        "R1": 80000000000000000,
        "R2": 1000000000000000000,
    },
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": {
        "UBar": 800000000000000000,
        "R0": 0,
        "R1": 40000000000000000,
        "R2": 600000000000000000,
    },
    "0x04Fa0d235C4abf4BcF4787aF4CF447DE572eF828": {
        "UBar": 500000000000000000,
        "R0": 0,
        "R1": 50000000000000000,
        "R2": 2000000000000000000,
    },
    "0x3472A5A71965499acd81997a54BBA8D852C6E53d": {
        "UBar": 500000000000000000,
        "R0": 25000000000000000,
        "R1": 25000000000000000,
        "R2": 2000000000000000000,
    },
}
