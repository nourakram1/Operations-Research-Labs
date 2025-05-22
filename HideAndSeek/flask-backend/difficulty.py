from enum import Enum
import numpy as np

class Difficulty(Enum):
    """
    Difficulty levels representing the seeker's penalties and rewards for each game cell.

    Attributes:
        label (str): The difficulty level name.
        penalty (int): The penalty applied to the seeker when on this difficulty.
        reward (int): The reward applied to the seeker when interacting with this difficulty.
    """
    EASY = ('EASY', -1, 2)
    NEUTRAL = ('NEUTRAL', -1, 1)
    HARD = ('HARD', -3, 1)
    
    def __init__(self, label, penalty, reward):
        self.label = label
        self.penalty = penalty
        self.reward = reward
        
    @staticmethod
    def of(game_board: np.array) -> np.array:
        return np.vectorize(lambda x: Difficulty[x])(game_board)