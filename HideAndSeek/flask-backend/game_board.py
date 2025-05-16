import numpy as np
from difficulty import Difficulty

class GameBoard:
    
    choices = list(Difficulty)
    
    @staticmethod
    def generate(n: int, m: int) -> np.array:
        """
        Generates an n x m game board where each cell is randomly assigned
        a Difficulty enum member (EASY, NEUTRAL, or HARD).

        Args:
            n (int): Number of rows.
            m (int): Number of columns.

        Returns:
            np.array: A 2D array representing the game board
            with Difficulty enum members in each cell.
        """
        return np.random.choice(GameBoard.choices, size=(n, m))