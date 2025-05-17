import numpy as np

class ProximityPenalty:
    @staticmethod
    def apply(game_matrix: np.array, n: int, m: int) -> np.array:
        """
        Adjusts the payoffs in the game matrix based on the Manhattan distance between hider and seeker.
        """
        adjusted = game_matrix.astype(float)

        size = n * m
        for hider in range(size):
            for seeker in range(size):
                if hider == seeker:
                    continue
                dist = ProximityPenalty._manhatten_dist(seeker, hider, n, m)
                if dist == 1:
                    adjusted[hider, seeker] *= 0.5
                elif dist == 2:
                    adjusted[hider, seeker] *= 0.75

        return adjusted

    @staticmethod
    def _manhatten_dist(seeker: int, hider: int, n: int, m: int) -> int:
        seeker_row, seeker_col = divmod(seeker, m)
        hider_row, hider_col = divmod(hider, m)
        return abs(seeker_row - hider_row) + abs(seeker_col - hider_col)
