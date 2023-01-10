import unittest

from prediction import Prediction

class TestEmptyPredictionDict(unittest.TestCase):

    def test_output_type(self) -> None:
        """verify correct output type"""
        result = Prediction.empty_prediction_dict()
        self.assertEqual(
            type(result), 
            dict, 
            f"expected type {dict} got {type(result)}",
        )

    def test_output(self) -> None:
        """verify correct output"""
        result: dict = Prediction.empty_prediction_dict()
        self.assertEqual(
            result, 
            {
                Prediction.FAIL: 0,
                Prediction.NOTHING: 0,
                Prediction.ROCK: 0,
                Prediction.PAPER: 0,
                Prediction.SCISSORS: 0,
            },
            "invalid dictionary",
        )

if __name__ == "__main__":
    unittest.main()