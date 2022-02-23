# Across

Across is the fastest, cheapest and most secure cross-chain bridge. It is a system that uses UMA contracts to quickly move tokens across chains. This contains various utilities to support applications on across.

## How to use

### Get suggested fees from online API

Use across official API to get suggested fees.

```py
>>> import across
>>> a = across.AcrossAPI()
>>> a.suggested_fees("0x7f5c764cbc14f9669b88837ca1490cca17c31607", 10, 1000000000)
{'slowFeePct': '43038790000000000', 'instantFeePct': '5197246000000000'}
```

### Fee Calculator

Calculates lp fee percentages when doing a transfer.

```py
from across.fee_calculator import (
    calculate_apy_from_utilization,
    calculate_realized_lp_fee_pct,
)
from across.utils import toBNWei

rate_model = {
    "UBar": toBNWei("0.65"),
    "R0": toBNWei("0.00"),
    "R1": toBNWei("0.08"),
    "R2": toBNWei("1.00"),
}

interval = { "utilA": 0, "utilB": toBNWei(0.01), "apy": 615384615384600, "wpy": 11830749673498 }
apy_fee_pct = calculate_apy_from_utilization(rate_model, interval["utilA"], interval["utilB"])
assert apy_fee_pct == interval["apy"]

realized_lp_fee_pct = calculate_realized_lp_fee_pct(rate_model, interval["utilA"], interval["utilB"])
assert realized_lp_fee_pct == interval["wpy"]
```

### LP Fee Calculator

Get lp fee calculations by timestamp. **Currently only support `latest`**.

```py
from across import LpFeeCalculator
from web3 import Web3

provider = Web3.WebsocketProvider("{YOUR-PROVIDER-ADDRESS}")
calculator = LpFeeCalculator(provider)
token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" # WETH on mainnet
bridge_pool_address = "0x7355Efc63Ae731f584380a9838292c7046c1e433" # WETH BridgePool on mainnet
amount = "1000000000000000000" # 1 ETH
timestamp = None # timestamp in seconds
percent = calculator.get_lp_fee_pct(
    token_address, bridge_pool_address, amount, timestamp
)
print(percent)
```

## How to build and test

Install poetry and install the dependencies:

```shell
pip3 install poetry

poetry install

# test
python -m unittest

# local install and test
pip3 install twine
python3 -m twine upload --repository testpypi dist/*
pip3 install --index-url https://test.pypi.org/simple/ --no-deps across
```
