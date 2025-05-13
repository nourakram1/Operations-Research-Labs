from sympy import Symbol, sympify, Expr
from functools import cmp_to_key

def compare_expressions(expr1: str | int | float | Expr,
                        expr2: str | int | float | Expr,
                        symbol: Symbol) -> int:
    expr1: Expr = sympify(expr1)
    expr2: Expr = sympify(expr2)

    lead1: Expr = expr1.coeff(symbol)
    lead2: Expr = expr2.coeff(symbol)

    return expr1 - expr2 if lead1 == lead2 else lead1 - lead2


def sort_expression_arr(arr: list[(int, str | int | float | Expr)], symbol: Symbol | None) -> list[str | int | float | Expr]:
    sort_m = lambda x, y: compare_expressions(x[1], y[1], symbol)
    return sorted(arr, key=cmp_to_key(sort_m))