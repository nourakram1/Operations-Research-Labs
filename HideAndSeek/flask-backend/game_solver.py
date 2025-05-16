import numpy as np
import cvxpy as cp

class GameSolver:
    @staticmethod
    def solve(game_matrix: np.array):
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
