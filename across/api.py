import requests
from typing import Dict
from .exceptions import AcrossException


__all__ = ["AcrossException", "AcrossAPI"]


class AcrossAPI:

    BASEURL = "https://across.to/api"

    def suggested_fees(
        self, l2Token: str, chainId: int, amount: int
    ) -> Dict[str, int]:
        """get suggested fees for a given amount of l2Token.

        Args:
            l2Token (str): Address of L2 Token Contract to Transfer. For ETH use address `0x0`.
            chainId (int): Chain ID to transfer from.
            amount (int): Amount of the token to transfer.
                          Note: this amount is in the native decimals of the token.
                          So, for ETH this would be the amount of human-readable ETH multiplied by `1e18`.
                          For USDC, you would multiply the number of human-readable USDC by `1e6`.

        Returns:
            suggested fees for slow and instant relay.
                - slowFeePct (int): Fee for slow relay.
                - instantFeePct (int): Fee for instant relay.

        Raises:
            AcrossException: if the request fails.
                - 400: if either the slow fee or the instant fee exceeds 25% of the amount.
                - 400: invalid input.
                - 500: an unexpected error within the API.
        """
        url = f"{self.BASEURL}/suggested-fees"
        params = {"amount": amount, "chainId": chainId, "l2Token": l2Token}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise AcrossException(
                f"Failed to get fees for {l2Token}: {response.text}"
            )
        return response.json()


if __name__ == "__main__":
    api = AcrossAPI()
    print(
        api.suggested_fees(
            "0x7f5c764cbc14f9669b88837ca1490cca17c31607", 10, 1000000000
        )
    )
