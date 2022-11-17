import unittest

from app import *


class TestPredictList(unittest.TestCase):
    """Tests for weighted_predictions"""

    def test_output_type(self) -> None:
        """expect the output to be the type str"""
        result = weighted_prediction(["rock"])
        self.assertEqual(type(result), str, "wrong type")

    def test_output_empty_input(self) -> None:
        """expect the first prediction when all predictions are 0"""
        result = weighted_prediction([])
        self.assertEqual(result, "fail", "expected fail")

    def test_fail_winner(self) -> None:
        """expect fail to win"""
        result: str = weighted_prediction([
            "nothing",
            "scissors",
            "paper",
            "rock",
            "fail"
        ])
        self.assertEqual(result, "fail", "expected fail as output")

    def test_nothing_winner(self) -> None:
        """expect nothing to win"""
        result: str = weighted_prediction([
            "fail",
            "scissors",
            "paper",
            "rock",
            "nothing",
        ])
        self.assertEqual(result, "nothing", "expected nothing as output")

    def test_rock_winner(self) -> None:
        """expect rock to win"""
        result: str = weighted_prediction([
            "fail",
            "nothing",
            "scissors",
            "paper",
            "rock",
        ])
        self.assertEqual(result, "rock", "expected rock as output")

    def test_paper_winner(self) -> None:
        """expect paper to win"""
        result: str = weighted_prediction([
            "fail",
            "nothing",
            "scissors",
            "rock",
            "paper",
        ])
        self.assertEqual(result, "paper", "expected paper as output")

    def test_scissor_winner(self) -> None:
        """expect rock to win"""
        result: str = weighted_prediction([
            "fail",
            "nothing",
            "paper",
            "rock",
            "scissors",
        ])
        self.assertEqual(result, "scissors", "expected scissors as output")


if __name__ == "__main__":
    unittest.main()
