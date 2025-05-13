from sympy import Matrix, Symbol
from simplex.util import sort_expression_arr, compare_expressions
from simplex.classes import SimplexTerminationStatus, CommentGenerator


class SimplexEngine:
    def __init__(self, z_rows: Matrix, symbols_in_z_rows: list[Symbol], m: Matrix, x: list[Symbol],
                 x_bv: list[Symbol],
                 is_maximization: bool, steps: list[dict], z_rows_symbols: list[Symbol],
                 artificial_vars: list[Symbol] | None = None,
                 comment_generator: CommentGenerator | None = None) -> None:
        self.z_rows = z_rows
        self.symbols_in_z_rows = symbols_in_z_rows if symbols_in_z_rows else [None] * z_rows.rows
        self.x_bv = x_bv
        self.x = x
        self.m = m
        self.is_max = is_maximization
        self.steps = steps
        self.z_rows_symbols = z_rows_symbols
        self.artificial_vars = artificial_vars
        self.step_cnt = 0
        self.termination_status : SimplexTerminationStatus | None = None
        self.cg = comment_generator if comment_generator is not None else CommentGenerator()
        self.rows_symbols = [Symbol(f"R_{i + 1}") for i in range(m.rows)]


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
                self.__push_step(comment=self.cg.inconsistent_row(self.z_rows_symbols[i]), cnt_step=False)
                factor = self.z_rows[i, j]
                self.z_rows[i, :] -= factor * self.m[k, :]
                self.__push_step(comment=self.cg.row_operation(self.z_rows_symbols[i], self.rows_symbols[k], factor))
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
            symbol = self.symbols_in_z_rows[row_index]
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
                entering_index, _ = sorted_arr[i]
                if self.__more_prior(row_index, entering_index):
                    return entering_index
        return -1


    def __find_leaving_variable(self, col: int) -> int:
        """
        Returns the row index of the leaving variable or -1 if there is no variable can leave.
        """
        min_row: int = -1
        min_ratio: float = float('inf')

        for row in range(self.m.rows):
            if self.m[row, col] > 0:
                ratio: float = self.m[row, -1] / self.m[row, col]
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

        if pivot_element != 1:
            self.m[row, :] = self.m[row, :] / pivot_element
            self.__push_step(comment=self.cg.normalize_row(self.rows_symbols[row], pivot_element))

        # Pivot z rows
        for target_row in range(self.z_rows.rows):
            self.__row_op(self.z_rows, target_row, row, col, self.z_rows_symbols[target_row])

        # Pivot m rows
        for target_row in range(self.m.rows):
            if target_row != row:
                self.__row_op(self.m, target_row, row, col, self.rows_symbols[target_row])


    def __row_op(self, matrix: Matrix, target_row: int, pivot_row: int, pivot_col: int, target_row_symbol: Symbol) -> None:
        factor = matrix[target_row, pivot_col]
        if factor == 0: return
        matrix[target_row, :] -= factor * self.m[pivot_row, :]
        self.__push_step(comment=self.cg.row_operation(target_row_symbol, self.rows_symbols[pivot_row], factor))


    def __push_step(self,
                    entering_var_index: int | None = None,
                    leaving_var_index: int | None = None,
                    comment: str = "",
                    cnt_step: bool = True) -> None:
        if cnt_step:
            self.step_cnt += 1

        step = {
            "variables": self.x.copy(),
            "zRowsSymbols": self.z_rows_symbols,
            "basicVariables": self.x_bv.copy(),
            "simplexMatrix": self.z_rows.col_join(self.m).tolist().copy(),
            "comment": f"Step {self.step_cnt}:\n" + comment if cnt_step else comment
        }
        if entering_var_index is not None and leaving_var_index is not None:
            step["enteringVariableIndex"] = entering_var_index
            step["leavingVariableIndex"] = leaving_var_index

        self.steps.append(step)


    def __infer_termination_status(self) -> None:
        self.termination_status : SimplexTerminationStatus = \
                                  SimplexTerminationStatus.INFEASIBLE if self.__infeasible() \
                             else SimplexTerminationStatus.UNBOUNDED if self.__unbounded() \
                             else SimplexTerminationStatus.INFINITE_SOLUTIONS if self.__infinite_solutions() \
                             else SimplexTerminationStatus.DEGENERATE if self.__degenerate() \
                             else SimplexTerminationStatus.OPTIMAL


    def __degenerate(self) -> bool:
        return any(self.m[row, -1] == 0 for row in range(self.m.rows)
                   if self.x_bv[row] not in self.artificial_vars)


    def __unbounded(self) -> bool:
        return any(not self.__can_leave(self.__can_enter(i))
                   for i in range(self.z_rows.rows) if self.__can_enter(i))


    def __infinite_solutions(self) -> bool:
        return any(all(self.z_rows[i, j] == 0 for i in range(self.z_rows.rows))
                   for j in range(self.z_rows.cols - 1) if self.x[j] not in self.x_bv and self.__can_leave(j))


    def __infeasible(self) -> bool:
        return any(self.m[self.x_bv.index(a), -1] > 0 for a in self.artificial_vars if a in self.x_bv)


    def __can_enter(self, row_index: int) -> int:
        """
        Returns the index of the column containing a non-basic variable
        with positive coefficient in case of maximization or
        with negative coefficient in case of minimization
        such that in the column of the non-basic variables, all rows before row_index contain zeros or
        -1 otherwise
        """
        return next((j for j in range(self.z_rows.cols - 1)
                     if self.x[j] not in self.x_bv
                     and (compare_expressions(self.z_rows[row_index, j], 0, self.symbols_in_z_rows[row_index]) < 0
                          if self.is_max
                          else compare_expressions(self.z_rows[row_index, j], 0, self.symbols_in_z_rows[row_index]) > 0)
                     and self.__more_prior(row_index, j)), -1)


    def __can_leave(self, col_index: int) -> bool:
        """
        Returns true if one basic variable can leave in the specified column.
        """
        return any(self.m[i, col_index] > 0 for i in range(self.m.rows))


    def reduce(self) -> None:
        self.__push_step(comment=self.cg.initial(), cnt_step=False)
        self.__make_consistent()

        entering_var: int = self.__find_entering_variable()
        while entering_var != -1:
            leaving_var: int = self.__find_leaving_variable(entering_var)
            if leaving_var != -1:
                self.__push_step(entering_var, leaving_var, self.cg.pivot_element(self.x[entering_var],
                                                                                  self.x_bv[leaving_var]))
                self.__pivot(leaving_var, entering_var)
                entering_var: int = self.__find_entering_variable()
            else:
                break

        self.__infer_termination_status()
        self.__push_step()