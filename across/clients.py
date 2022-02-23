import typing

import json
from pathlib import Path
from web3 import Web3
from web3.providers import BaseProvider
from web3.contract import Contract


class BridgePool:
    """
    A class for interacting with the bridge pool contract.
    """

    @staticmethod
    def connect(address: str, provider: BaseProvider) -> Contract:
        w3 = Web3(provider)
        with open(
            Path(__file__).parent / "abis/bridge_pool_abi.json", "r"
        ) as abi_file:
            abi = json.load(abi_file)
        contract_instance = w3.eth.contract(address=address, abi=abi)
        return contract_instance


class RateModelStore:
    """
    A class for interacting with the rate model store contract.
    """

    @staticmethod
    def connect(address: str, provider: BaseProvider) -> Contract:
        w3 = Web3(provider)
        with open(
            Path(__file__).parent / "abis/rate_model_store_abi.json", "r"
        ) as abi_file:
            abi = json.load(abi_file)
        contract_instance = w3.eth.contract(address=address, abi=abi)
        return contract_instance

    def get_address(self, network_id: int) -> str:
        # FIXME: hardcoded
        if network_id == 1:
            return "0xd18fFeb5fdd1F2e122251eA7Bf357D8Af0B60B50"
        else:
            return ""
