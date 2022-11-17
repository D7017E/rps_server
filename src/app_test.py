import unittest

from prediction import Prediction
from app import *


class TestPredictList(unittest.TestCase):
    """Tests for weighted_predictions"""

    def test_output_type(self) -> None:
        """expect the output to be the type str"""
        result = weighted_prediction([Prediction.ROCK])
        self.assertEqual(
            type(result), 
            Prediction, 
            f"wrong type, expected {Prediction} got {type(result)}",
        )

    def test_output_empty_input(self) -> None:
        """expect the first prediction when all predictions are 0"""
        result: Prediction = weighted_prediction([])
        self.assertEqual(
            result, 
            Prediction.FAIL, 
            f"expected {Prediction.FAIL.name} got {result.name}",
        )

    def test_fail_winner(self) -> None:
        """expect fail to win"""
        result: Prediction = weighted_prediction([
            Prediction.NOTHING,
            Prediction.ROCK,
            Prediction.PAPER,
            Prediction.SCISSOR,
            Prediction.FAIL,
        ])
        self.assertEqual(
            result, 
            Prediction.FAIL, 
            f"expected {Prediction.FAIL.name} got {result.name}",
        )

    def test_nothing_winner(self) -> None:
        """expect nothing to win"""
        result: Prediction = weighted_prediction([
            Prediction.FAIL,
            Prediction.ROCK,
            Prediction.PAPER,
            Prediction.SCISSOR,
            Prediction.NOTHING,
        ])
        self.assertEqual(
            result, 
            Prediction.NOTHING, 
            f"expected {Prediction.NOTHING.name} got {result.name}",
        )

    def test_rock_winner(self) -> None:
        """expect rock to win"""
        result: Prediction = weighted_prediction([
            Prediction.FAIL,
            Prediction.NOTHING,
            Prediction.PAPER,
            Prediction.SCISSOR,
            Prediction.ROCK,
        ])
        self.assertEqual(
            result, 
            Prediction.ROCK, 
            f"expected {Prediction.ROCK.name} got {result.name}",
        )

    def test_paper_winner(self) -> None:
        """expect paper to win"""
        result: Prediction = weighted_prediction([
            Prediction.FAIL,
            Prediction.NOTHING,
            Prediction.ROCK,
            Prediction.SCISSOR,
            Prediction.PAPER,
        ])
        self.assertEqual(
            result, 
            Prediction.PAPER, 
            f"expected {Prediction.PAPER.name} got {result.name}",
        )

    def test_scissor_winner(self) -> None:
        """expect rock to win"""
        result: Prediction = weighted_prediction([
            Prediction.FAIL,
            Prediction.NOTHING,
            Prediction.ROCK,
            Prediction.PAPER,
            Prediction.SCISSOR,
        ])
        self.assertEqual(
            result, 
            Prediction.SCISSOR, 
            f"expected {Prediction.SCISSOR.name} got {result.name}",
        )


if __name__ == "__main__":
    unittest.main()
