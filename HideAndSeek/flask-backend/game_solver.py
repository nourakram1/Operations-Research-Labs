import numpy as np
from scipy.optimize import linprog

class GameSolver:
  @staticmethod
  def solve(constraints: np.array, primal=True) -> np.array:
    num_strategies = constraints.shape[0]
    
    c = [0] * num_strategies + [-1 if primal else 1]

    A_ub = np.hstack((constraints, (1 if primal else -1) * np.ones((num_strategies, 1))))
    b_ub = [0] * num_strategies

    A_eq = [[1] * num_strategies + [0]]
    probs_sum = [1]

    bounds = [(0, 1)] * num_strategies + [(None, None)]

    result = linprog(c, A_ub=A_ub, b_ub=b_ub,
                        A_eq=A_eq, b_eq=probs_sum,
                        method='highs', bounds=bounds)
    if result.success:
        return result.x[:-1]
    else:
        print("Optimization failed:", result.message)
        print("Status code:", result.status)
        raise ValueError("Linear program failed to solve.")

  @staticmethod
  def solve_hider_strategy(game_matrix: np.array) -> np.array:
    return GameSolver.solve(-game_matrix.T, primal=True)

  @staticmethod
  def solve_seeker_strategy(game_matrix: np.array) -> np.array:
    return GameSolver.solve(game_matrix, primal=False)