from sympy import Matrix

class SimplexSolver:
    def __init__(self, z_rows: Matrix, m: Matrix, x: Matrix, x_bv: Matrix, is_max: bool) -> None:
        self.z_rows = z_rows
        self.x_bv = x_bv
        self.x = x
        self.m = m
        self.is_max = is_max


    def make_consistent(self) -> None:
        for i in range(self.z_rows.rows):
            for j in range(self.z_rows.cols):
                # Find a basic variable with a nonzero coefficient
                if self.z_rows[i, j] != 0 and self.x[j] in self.x_bv:
                    # Find a 1 in the inconsistent column
                    for k in range(self.m.rows):
                        if self.m[k, j] == 1:
                            self.z_rows.row_op(i, lambda v, col: v - self.z_rows[i, j] * self.m[k, col])
                            break


    def __more_prior(self, row_index: int, entering_index: int) -> bool:
        for row in range(row_index):
            if self.is_max:
                if self.z_rows[row, entering_index] < 0:
                    return False
            else:
                if self.z_rows[row, entering_index] > 0:
                    return False
        return True

    def __find_entering_variable(self) -> int:
        entering_index = -1
        best_value = float('-inf') if self.is_max else float('inf')
        num_rows, num_cols = self.z_rows.shape

        for row_index in range(num_rows):
            row_values = self.z_rows[row_index, :].tolist()[0]

            for index, value in enumerate(row_values):
                if self.is_max:
                    if value > best_value:
                        best_value = value
                        entering_index = index
                else:
                    if value < best_value:
                        best_value = value
                        entering_index = index

            if entering_index != -1:
                if self.is_max and best_value < 0 and self.__more_prior(row_index, entering_index):
                    return entering_index
                elif not self.is_max and best_value > 0 and self.__more_prior(row_index, entering_index):
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

    def __pivot(self, row : int, col : int) -> None:
        if self.m[row, col] == 0:
            raise Exception("Error: can not pivot zero element.")

        pivot = self.m[row, col]
        self.m.row_op(row, lambda row_element, _: row_element / pivot)

        for r in range(self.m.rows):
            if r != row:
                factor = self.m[r, col]
                self.m.row_op(r, lambda row_element, index: row_element - factor * self.m[row, index])

    def solve(self) -> NotImplemented:
        pass