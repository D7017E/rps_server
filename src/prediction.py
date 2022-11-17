from enum import IntEnum


class Prediction(IntEnum):
    """Enum for predictions"""
    FAIL = 0
    NOTHING = 1
    ROCK = 2
    PAPER = 3
    SCISSORS = 4

    @staticmethod
    def empty_prediction_dict() -> dict:
        """Return empty dictionary for all values"""
        return {
            Prediction.FAIL: 0,
            Prediction.NOTHING: 0,
            Prediction.ROCK: 0,
            Prediction.PAPER: 0,
            Prediction.SCISSORS: 0,
        }
        
