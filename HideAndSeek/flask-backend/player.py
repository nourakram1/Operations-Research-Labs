import numpy as np
class Player:
        
    @staticmethod
    def play(n: int, m: int, probabilities: np.array) -> tuple[int, int]:
        """
        Randomly selects a cell in an n x m grid based on the given 1D probabilities array.

        Args:
            n (int): Number of rows.
            m (int): Number of columns.
            probabilities (np.array): A 1D array of length n * m representing selection probabilities.

        Returns:
            tuple[int, int]: The (row, column) of the selected cell.
        """
        return divmod(np.random.choice(n * m, p = probabilities), m)

    @staticmethod
    def play_n(n: int, m: int, probabilities: np.array, size: int) -> list[list[int]]:
        """
        Randomly selects a cell in an n x m grid based on the given 1D probabilities array.

        Args:
            size (int): Number of moves.
            n (int): Number of rows.
            m (int): Number of columns.
            probabilities (np.array): A 1D array of length n * m representing selection probabilities.

        Returns:
            tuple[int, int]: The (row, column) of the selected cell.
        """
        return [[int(a), int(b)] for x in np.random.choice(n * m, size=size, p=probabilities) for a, b in [divmod(x, m)]]
