from typing import Union
from web3 import Web3

toBNWei = lambda x: Web3.toWei(x, "ether")
fixedPointAdjustment = toBNWei("1")
BigNumberish = Union[int, str]
