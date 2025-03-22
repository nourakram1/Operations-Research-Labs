from sympy import Matrix, Symbol
from .util import sort_expression_arr, compare_expressions


class SimplexEngine:
    def __init__(self, z_rows: Matrix, symbols_in_z_rows: list[Symbol | None], m: Matrix, x: list[Symbol], x_bv: list[Symbol],
                 is_maximization: bool, steps: list[dict], z_rows_symbols: list[Symbol]) -> None:
        self.z_rows = z_rows
        self.symbols_in_z_rows = symbols_in_z_rows
        self.x_bv = x_bv
        self.x = x
        self.m = m
        self.is_max = is_maximization
        self.is_optimal: bool = False
        self.steps = steps
        self.z_rows_symbols = z_rows_symbols


    def __make_consistent(self) -> None:
        for i in range(self.z_rows.rows):
            for j in range(self.z_rows.cols - 1):
                if self.__is_inconsistent(i, j):
                    self.__fix_inconsistency(i, j)


    def __is_inconsistent(self, i: int, j: int) -> bool:
        return self.z_rows[i, j] != 0 and self.x[j] in self.x_bv


    def __fix_inconsistency(self, i: int, j: int) -> None:
        for k in range(self.m.rows):
            if self.m[k, j] == 1:
                self.z_rows[i, :] -= self.z_rows[i, j] * self.m[k, :]
                return


    def __more_prior(self, row_index: int, entering_index: int) -> bool:
        for row in range(row_index):
            if self.z_rows[row, entering_index] != 0:
                return False
        return True


    def __find_entering_variable(self) -> int:
        possible_entering_vars = []
        num_rows, num_cols = self.z_rows.shape

        for row_index in range(num_rows):
            symbol = self.symbols_in_z_rows[row_index] if self.symbols_in_z_rows else None
            for col_index in range(num_cols - 1):
                value = self.z_rows[row_index, col_index]
                if self.is_max:
                    if compare_expressions(value, 0, symbol) < 0:
                        possible_entering_vars.append((col_index, value))
                else:
                    if compare_expressions(value, 0, symbol) > 0:
                        possible_entering_vars.append((col_index, -value))
            sorted_arr = sort_expression_arr(possible_entering_vars, symbol)
            for i in range(len(sorted_arr)):
                entering_index, _ =  sorted_arr[i]
                if self.__more_prior(row_index, entering_index):
                    return entering_index
        return -1


    def __find_leaving_variable(self, col : int) -> int:
        """
        Returns the row index of the leaving variable or -1 if there is no variable can leave.
        """
        min_row : int = -1
        min_ratio : float = float('inf')

        for row in range(self.m.rows):
            if self.m[row, col] > 0:
                ratio : float = self.m[row, -1] / self.m[row, col]
                if 0 <= ratio < min_ratio:
                    min_ratio = ratio
                    min_row = row

        return min_row


    def __pivot(self, row: int, col: int) -> None:
        """
        Perform pivoting on the tableau at (row, col).
        """
        self.x_bv[row] = self.x[col]

        pivot_element = self.m[row, col]
        if pivot_element == 0:
            raise ValueError("Error: cannot pivot on a zero element.")

        self.m[row, :] = self.m[row, :] / pivot_element

        for r in range(self.z_rows.rows):
            factor = self.z_rows[r, col]
            self.z_rows[r, :] -= factor * self.m[row, :]

        for r in range(self.m.rows):
            if r != row:
                factor = self.m[r, col]
                self.m[r, :] -= factor * self.m[row, :]


    def __push_step(self,
                    entering_var_index: int | None = None,
                    leaving_var_index: int | None = None,
                    comment: str = "") -> None:
        step = {
            "zRowsSymbols": self.z_rows_symbols,
            "basicVariables": self.x_bv.copy(),
            "simplexMatrix": self.z_rows.col_join(self.m).tolist().copy(),
            "comment": comment
        }
        if entering_var_index is not None and leaving_var_index is not None:
            step["enteringVariableIndex"] = entering_var_index
            step["leavingVariableIndex"] = leaving_var_index

        self.steps.append(step)


    def reduce(self) -> None:
        self.__push_step()
        self.__make_consistent()

        entering_var: int = self.__find_entering_variable()
        while entering_var != -1:
            leaving_var : int = self.__find_leaving_variable(entering_var)
            if leaving_var != -1:
                self.__push_step(entering_var, leaving_var)
                self.__pivot(leaving_var, entering_var)
                entering_var: int = self.__find_entering_variable()
            else:
                self.is_optimal = False
                return
        self.__push_step()
        self.is_optimal = True