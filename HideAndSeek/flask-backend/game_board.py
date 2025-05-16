import numpy as np
import random

class GameBoard:

    plays = ['EASY', 'NEUTRAL', 'HARD']
    probabilities = [1/3, 1/3, 1/3]
    
    @staticmethod
    def generate(n, m):
        game_board = np.empty((n, m), dtype=object)
        
        for i in range(n):
            for j in range(m):
                play_choice = random.choices(GameBoard.plays, weights=GameBoard.probabilities, k=1)[0]
                game_board[i, j] = play_choice
                    
        return game_board
    

