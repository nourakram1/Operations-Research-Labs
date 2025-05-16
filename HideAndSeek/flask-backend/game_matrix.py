import numpy as np
from difficulty import Difficulty

class GameMatrix:
    @staticmethod
    def generate(game_board: np.array) -> np.array:
        """
        Generates a square game matrix based on the difficulty levels of each cell in the game board.

        Each cell in the input game_board contains a difficulty EASY, NEUTRAL, HARD.
        The resulting matrix has dimensions (n*m) x (n*m), where n and m are the dimensions of game_board.

        For each cell i in the flattened game_board:
        - The diagonal element (i, i) is assigned the penalty value corresponding to that cell's difficulty.
        - All off-diagonal elements in row i are assigned the reward value for that difficulty.

        Args:
            game_board (np.array): 2D numpy array of enums of difficulties.

        Returns:
            np.array: 2D numpy integer array representing the game matrix.
        """
        n, m = game_board.shape
        game_matrix = np.zeros((n * m, n * m), dtype=int)
        
        for i in range(n * m):
            difficulty = game_board[i // m, i % m]
            for j in range(n * m):
                if i == j:
                    game_matrix[i, j] = difficulty.penalty
                else:
                    game_matrix[i, j] = difficulty.reward
                    
        return game_matrix