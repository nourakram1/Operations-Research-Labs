import numpy as np
class Player:
        
    @staticmethod
    def play(n: int, m: int, probabilities: np.array) -> tuple:
        location = np.random.choice(n * m, p = probabilities.flatten())
        return location // m, location % m