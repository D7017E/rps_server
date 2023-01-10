import unittest
from prediction import Prediction
from app import *

class TestPredictList(unittest.TestCase):
    """Tests for weighted_predictions"""

    def test_output_type(self) -> None:
        """expect the output to be the type str"""
        result = weighted_prediction([(Prediction.ROCK, None)])
        self.assertEqual(
            type(result[0]), 
            Prediction, 
            f"wrong type, expected {Prediction} got {type(result[0])}",
        )

    def test_output_empty_input(self) -> None:
        """expect the first prediction when all predictions are 0"""
        result: Prediction = weighted_prediction([])
        self.assertEqual(
            result[0], 
            Prediction.FAIL, 
            f"expected {Prediction.FAIL.name} got {result[0].name}",
        )

    def test_fail_winner(self) -> None:
        """expect fail to win"""
        result: Prediction = weighted_prediction([
            (Prediction.NOTHING, None),
            (Prediction.ROCK, None),
            (Prediction.PAPER, None),
            (Prediction.SCISSORS, None),
            (Prediction.FAIL, None),
        ])
        self.assertEqual(
            result[0], 
            Prediction.FAIL, 
            f"expected {Prediction.FAIL.name} got {result[0].name}",
        )

    def test_nothing_winner(self) -> None:
        """expect nothing to win"""
        result: Prediction = weighted_prediction([
            (Prediction.FAIL, None),
            (Prediction.ROCK, None),
            (Prediction.PAPER, None),
            (Prediction.SCISSORS, None),
            (Prediction.NOTHING, None),
        ])
        self.assertEqual(
            result[0], 
            Prediction.NOTHING, 
            f"expected {Prediction.NOTHING.name} got {result[0].name}",
        )

    def test_rock_winner(self) -> None:
        """expect rock to win"""
        result: Prediction = weighted_prediction([
            (Prediction.FAIL, None),
            (Prediction.NOTHING, None),
            (Prediction.PAPER, None),
            (Prediction.SCISSORS, None),
            (Prediction.ROCK, None),
        ])
        self.assertEqual(
            result[0], 
            Prediction.ROCK, 
            f"expected {Prediction.ROCK.name} got {result[0].name}",
        )

    def test_paper_winner(self) -> None:
        """expect paper to win"""
        result: Prediction = weighted_prediction([
            (Prediction.FAIL, None),
            (Prediction.NOTHING, None),
            (Prediction.ROCK, None),
            (Prediction.SCISSORS, None),
            (Prediction.PAPER, None),
        ])
        self.assertEqual(
            result[0], 
            Prediction.PAPER, 
            f"expected {Prediction.PAPER.name} got {result[0].name}",
        )

    def test_scissor_winner(self) -> None:
        """expect rock to win"""
        result: Prediction = weighted_prediction([
            (Prediction.FAIL, None),
            (Prediction.NOTHING, None),
            (Prediction.ROCK, None),
            (Prediction.PAPER, None),
            (Prediction.SCISSORS, None),
        ])
        self.assertEqual(
            result[0], 
            Prediction.SCISSORS, 
            f"expected {Prediction.SCISSORS.name} got {result[0].name}",
        )


if __name__ == "__main__":
    unittest.main()
