import unittest
from across.fee_calculator import (
    calculate_apy_from_utilization,
    calculate_realized_lp_fee_pct,
)
from across.utils import toBNWei


class TestFeeCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.rateModel = {
            "UBar": toBNWei("0.65"),
            "R0": toBNWei("0.00"),
            "R1": toBNWei("0.08"),
            "R2": toBNWei("1.00"),
        }
        self.tested_intervals = [
            { "utilA": 0, "utilB": toBNWei(0.01), "apy": 615384615384600, "wpy": 11830749673498 },
            { "utilA": toBNWei("0"), "utilB": toBNWei("0.50"), "apy": 30769230769230768, "wpy": 582965040710805 },
            { "utilA": toBNWei("0.5"), "utilB": toBNWei("0.51"), "apy": 62153846153846200, "wpy": 1160264449662626 },
            { "utilA": toBNWei("0.5"), "utilB": toBNWei("0.56"), "apy": 65230769230769233, "wpy": 1215959072035989 },
            { "utilA": toBNWei("0.5"), "utilB": toBNWei("0.5") + 100, "apy": 60000000000000000, "wpy": 1121183982821340 },
            { "utilA": toBNWei("0.6"), "utilB": toBNWei("0.7"), "apy": 114175824175824180, "wpy": 2081296752280018 },
            { "utilA": toBNWei("0.7"), "utilB": toBNWei("0.75"), "apy": 294285714285714280, "wpy": 4973074331615530 },
            { "utilA": toBNWei("0.7"), "utilB": toBNWei("0.7") + 100, "apy": 220000000000000000, "wpy": 3831376003126766 },
            { "utilA": toBNWei("0.95"), "utilB": toBNWei("1.00"), "apy": 1008571428571428580, "wpy": 13502339199904125 },
            { "utilA": toBNWei("0"), "utilB": toBNWei("0.99"), "apy": 220548340548340547, "wpy": 3840050658887291 },
            { "utilA": toBNWei("0"), "utilB": toBNWei("1.00"), "apy": 229000000000000000, "wpy": 3973273191633388 },
        ]
        return super().setUp()

    def test_calculate_apy_from_utilization(self):

        for interval in self.tested_intervals:
            apyFeePct = calculate_apy_from_utilization(
                self.rateModel, interval["utilA"], interval["utilB"]
            )
            self.assertEqual(apyFeePct, interval["apy"])

    def test_calculate_realized_lp_fee_pct(self):
        for interval in self.tested_intervals:
            realizedLpFeePct = calculate_realized_lp_fee_pct(
                self.rateModel, interval["utilA"], interval["utilB"]
            )
            self.assertEqual(realizedLpFeePct, interval["wpy"])
