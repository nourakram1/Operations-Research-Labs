import numpy as np
import cvxpy as cp

class GameSolver:
    @staticmethod
    def solve(game_matrix: np.array) -> tuple[np.array, np.array]:
        """
        Solve a two-player zero-sum matrix game to find the optimal mixed strategies
        for both players using linear programming.

        This method computes the Nash equilibrium strategies for the seeker and hider
        in a zero-sum game represented by the payoff matrix `game_matrix`. The game is
        defined such that the seeker selects a column strategy and the hider selects
        a row strategy, with the payoff to the seeker given by the corresponding matrix entry.

        The algorithm solves the linear program:

            maximize v
            subject to A x >= v * 1
                       sum(x) = 1
                       x >= 0

        where:
        - A is the payoff matrix (`game_matrix`).
        - x is the seeker's mixed strategy vector (probabilities over columns).
        - v is the value of the game (minimum guaranteed expected payoff for the seeker).
        - The constraint `A x >= v * 1` ensures that for every hider strategy, the expected
          payoff is at least v.

        The dual variables associated with the first constraint correspond to the hider's
        optimal mixed strategy over rows.

        Parameters
        ----------
        game_matrix : np.array
            A 2D numpy array of shape (n_rows, n_cols) representing the payoff matrix.
            Each entry game_matrix[i, j] is the payoff to the seeker when the hider
            plays strategy i and the seeker plays strategy j.

        Returns
        -------
        tuple[np.array, np.array]
            - seeker_prob: 1D numpy array of length n_cols representing the seeker's
              optimal mixed strategy probabilities.
            - hider_prob: 1D numpy array of length n_rows representing the hider's
              optimal mixed strategy probabilities (from the dual variables).

        Raises
        ------
        ValueError
            If the solver fails to find an optimal or near-optimal solution, an error
            is raised with the solver status.

        Implementation Details
        ----------------------
        - Uses the ECOS solver via CVXPY with stringent solver tolerances for improved
          numerical precision (`abstol=1e-12`, `reltol=1e-12`, `feastol=1e-12`).
        - Due to floating-point inaccuracies, negative values in the probability vectors
          are clamped to zero before normalization.
        - The method normalizes the probability distributions to ensure they sum exactly
          to 1.
        """
        n_rows, n_cols = game_matrix.shape

        # Primal variables: seeker probabilities (x) and game value (v)
        x = cp.Variable(n_cols)
        v = cp.Variable()

        # Constraints:
        constraints = [
            game_matrix @ x >= v * np.ones(n_rows),     # A x >= v
            cp.sum(x) == 1,                             # probabilities sum to 1
            x >= 0                                      # probabilities >= 0
        ]

        # Objective: maximize v
        prob = cp.Problem(cp.Maximize(v), constraints)
        prob.solve(solver=cp.ECOS, abstol=1e-12, reltol=1e-12, feastol=1e-12)

        # Check if the solution is valid
        if prob.status not in ["optimal", "optimal_inaccurate"]:
            raise ValueError(f"Solver did not find optimal solution. Status: {prob.status}")

        seeker_prob = x.value
        game_value = v.value

        # Dual variables of the first constraint: hider strategy
        hider_prob = constraints[0].dual_value

        # Clamp negatives to zero due to numerical errors, then normalize
        seeker_prob = np.maximum(seeker_prob, 0)
        seeker_prob /= seeker_prob.sum()

        hider_prob = np.maximum(hider_prob, 0)
        hider_prob /= hider_prob.sum()

        return seeker_prob, hider_prob
