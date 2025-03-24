from enum import Enum


class ArtificialSolutionMethod(Enum):
    BIG_M = 1
    TWO_PHASE = 2


class RelationOperator(Enum):
    EQU = "="
    LEQ = "<="
    GEQ = ">="


class SimplexTerminationStatus(Enum):
    DEGENERATE = "Degeneracy"
    INFEASIBLE = "Infeasible"
    INFINITE_SOLUTIONS = "Infinite solutions"
    UNBOUNDED = "Unbounded"
    OPTIMAL = "Optimal"