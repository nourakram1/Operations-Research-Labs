from sympy import Matrix, Symbol
from typing import Union
from util import sort_expression_arr, compare_expressions


class SimplexSolver:
    def __init__(self, z_rows: Matrix, z_rows_symbols: list[Union[Symbol, None]], m: Matrix, x: Matrix, x_bv: Matrix,
                 is_maximization: bool) -> None:
        self.z_rows = z_rows
        self.z_rows_symbols = z_rows_symbols
        self.x_bv = x_bv
        self.x = x
        self.m = m
        self.is_max = is_maximization


    def __make_consistent(self) -> None:
        for i in range(self.z_rows.rows):
            for j in range(self.z_rows.cols - 1):
                # Find a basic variable with a nonzero coefficient
                if self.z_rows[i, j] != 0 and self.x[j] in self.x_bv:
                    # Find a 1 in the inconsistent column
                    for k in range(self.m.rows):
                        if self.m[k, j] == 1:
                            self.z_rows[i, :] -= self.z_rows[i, j] * self.m[k, :]
                            break


    def __more_prior(self, row_index: int, entering_index: int) -> bool:
        for row in range(row_index):
            if self.z_rows[row, entering_index] != 0:
                return False
        return True


    def __find_entering_variable(self) -> int:
        possible_entering_vars = []
        num_rows, num_cols = self.z_rows.shape

        for row_index in range(num_rows):
            for col_index in range(num_cols - 1):
                value = self.z_rows[row_index, col_index]
                if self.is_max:
                    if compare_expressions(value, 0, self.z_rows_symbols[row_index]) < 0:
                        possible_entering_vars.append((col_index, value))
                else:
                    if compare_expressions(value, 0, self.z_rows_symbols[row_index]) > 0:
                        possible_entering_vars.append((col_index, -value))
            sorted_arr = sort_expression_arr(possible_entering_vars, self.z_rows_symbols[row_index])
            for i in range(len(sorted_arr)):
                entering_index,_ =  sorted_arr[i]
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


    def solve(self) -> bool:
        self.__make_consistent()

        entering_var: int = self.__find_entering_variable()
        while entering_var != -1:
            leaving_var : int = self.__find_leaving_variable(entering_var)
            if leaving_var != -1:
                self.__pivot(leaving_var, entering_var)
                entering_var: int = self.__find_entering_variable()
            else: return False
        return True