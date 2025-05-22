import numpy as np
from difficulty import Difficulty

class Test:
    test_mode = False
    test_number = 1
        
    @staticmethod
    def test1() -> np.array:
        data = [
        ["EASY", "EASY", "EASY", "HARD"],
        ["EASY", "HARD", "EASY", "EASY"],
        ["EASY", "HARD", "NEUTRAL", "NEUTRAL"],
        ["EASY", "HARD", "NEUTRAL", "NEUTRAL"]
        ]
        return Difficulty.of(np.array(data))
    
    @staticmethod
    def test2() -> np.array:
        data = [
            ["NEUTRAL", "NEUTRAL"],
            ["EASY", "EASY"]
        ]
        return Difficulty.of(np.array(data))

    @staticmethod
    def test3() -> np.array:
        data = [["EASY", "EASY", "NEUTRAL", "HARD"]]
        return Difficulty.of(np.array(data))
    
    @staticmethod
    def get_test_case():
        try:
            return getattr(Test, f"test{Test.test_number}")()
        except AttributeError:
            raise ValueError(f"Test.test{Test.test_number} does not exist.")