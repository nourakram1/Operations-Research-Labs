import numpy as np
class GameMatrix:
    difficulty = {
        'EASY': (-1, 2),
        'NEUTRAL': (-1, 1),
        'HARD': (-3, 1)
    }
    @staticmethod
    def generate(game_board: np.array):
        n, m = game_board.shape
        game_matrix = np.zeros((n * m, n * m), dtype=int)
        
        for i in range(n * m):
            d = game_board[i // m, i % m]
            for j in range(n * m):
                if i == j:
                    game_matrix[i, j] = GameMatrix.difficulty[d][0]
                else:
                    game_matrix[i, j] = GameMatrix.difficulty[d][1]
                    
        return game_matrix