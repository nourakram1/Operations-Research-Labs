import cvxpy as cp
import numpy as np

class GameSolver:
    @staticmethod
    def solve(game_matrix: np.array):
        n_rows, n_cols = game_matrix.shape

        # Primal variables: seeker probabilities x and game value v
        x = cp.Variable(n_cols)
        v = cp.Variable()

        # Constraints:
        constraints = [
            game_matrix @ x >= v * np.ones(n_rows),  # A x >= v
            cp.sum(x) == 1,
            x >= 0
        ]

        # Objective: maximize v
        prob = cp.Problem(cp.Maximize(v), constraints)
        prob.solve(solver=cp.ECOS)

        seeker_prob = x.value
        game_value = v.value

        # Dual variables of the first constraint: hider strategy
        hider_prob = constraints[0].dual_value
        hider_prob /= hider_prob.sum()

        return seeker_prob, hider_prob