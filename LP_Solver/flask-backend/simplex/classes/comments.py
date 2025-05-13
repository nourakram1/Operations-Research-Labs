import sympy as sp


class CommentGenerator:
    @staticmethod
    def pivot_element(entering_var_symbol: sp.Symbol,
                      leaving_var_symbol: sp.Symbol) -> str:
        return f"Entering variable ${sp.latex(entering_var_symbol)}$ and leaving variable ${sp.latex(leaving_var_symbol)}$"

    @staticmethod
    def initial():
        return "Initial simplex tableau"

    @staticmethod
    def inconsistent_row(row_symbol: sp.Symbol) -> str:
        return f"Row ${sp.latex(row_symbol)}$ is inconsistent"

    @staticmethod
    def row_operation(target_row_symbol: sp.Symbol,
                      pivot_row_symbol: sp.Symbol,
                      factor: sp.Expr) -> str:
        multi_term = len(sp.Add.make_args(factor)) > 1
        sgn = sp.sign(factor)
        if not multi_term:
            factor *= sgn
        if factor == 1:
            factor = ""
        sgn = "+" if sgn < 0 else "-"
        lp = "(" if multi_term else ""
        rp = ")" if multi_term else ""
        comment = (f"${sp.latex(target_row_symbol)} = {sp.latex(target_row_symbol)}"
                   f"{sgn} {lp}{sp.latex(factor)}{rp}{sp.latex(pivot_row_symbol)}$")
        return comment

    @staticmethod
    def normalize_row(row_symbol: sp.Symbol, factor: sp.Expr) -> str:
        return f"${sp.latex(row_symbol)} = \\frac{"{"}{sp.latex(row_symbol)}{"}"}{"{"}{factor}{"}"}$"
