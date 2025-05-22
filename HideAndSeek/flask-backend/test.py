import numpy as np
from difficulty import Difficulty

class Test:
    test_mode = False
    test_number = 1
        
    @staticmethod
    def test1() -> tuple[np.array, bool]:
        data = [
        ["EASY", "EASY", "EASY", "HARD"],
        ["EASY", "HARD", "EASY", "EASY"],
        ["EASY", "HARD", "NEUTRAL", "NEUTRAL"],
        ["EASY", "HARD", "NEUTRAL", "NEUTRAL"]
        ]
        proximity = True
        return Difficulty.of(np.array(data)), proximity
    
    @staticmethod
    def test2() -> tuple[np.array, bool]:
        data = [
            ["NEUTRAL", "NEUTRAL"],
            ["EASY", "EASY"]
        ]
        proximity = True
        return Difficulty.of(np.array(data)), proximity

    @staticmethod
    def test3() -> tuple[np.array, bool]:
        data = [["EASY", "EASY", "NEUTRAL", "HARD"]]
        proximity = False
        return Difficulty.of(np.array(data)), proximity
    
    @staticmethod
    def get_test_case():
        try:
            return getattr(Test, f"test{Test.test_number}")()
        except AttributeError:
            raise ValueError(f"Test.test{Test.test_number} does not exist.")