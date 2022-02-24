from typing import Union, Iterable, Any, Optional
from web3 import Web3

toBNWei = lambda x: Web3.toWei(x, "ether")
fixedPointAdjustment = toBNWei("1")
BigNumberish = Union[int, str]


def sorted_index_by(arr: Iterable, target: Any, key: Optional[str]) -> int:
    """find the first index that can insert K in a sorted array"""
    if key:
        key_fun = lambda x: x[key] if isinstance(x, dict) else getattr(x, key)
    else:
        key_fun = lambda x: x
    lo = 0
    hi = len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if key_fun(arr[mid]) < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
