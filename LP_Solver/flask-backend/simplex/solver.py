from sympy import Matrix, Symbol, latex

from .enums import RelationOperator, ArtificialSolutionMethod
from .engine import SimplexEngine
from .util import compare_expressions

class SimplexSolver:
    def __init__(self,
                 objective_function_coefficients_vector: Matrix | None,
                 aug_constraints_coefficients_matrix: Matrix,
                 constraints_relations: list[RelationOperator],
                 aug_goals_coefficients_matrix: Matrix | None,
                 goals_relations: list[RelationOperator] | None,
                 restricted: list[bool],
                 is_maximization: bool | None,
                 artificial_solution_method: ArtificialSolutionMethod | None) -> None:

        self.objective_function_coefficients_vector = objective_function_coefficients_vector
        self.aug_constraints_coefficients_matrix = aug_constraints_coefficients_matrix
        self.constraints_relations = constraints_relations
        self.aug_goals_coefficients_matrix = aug_goals_coefficients_matrix
        self.goals_relations = goals_relations
        self.restricted = restricted
        self.is_maximization = is_maximization
        self.artificial_solution_method = artificial_solution_method
        self.steps: list[dict] = []
        self.vars: list[Symbol] = []
        self.restricted_decision_vars: list[tuple[int, Symbol]] = []
        self.unrestricted_decision_vars: list[tuple[int, Symbol, Symbol]] = []
        self.basic_vars: list[Symbol] = []
        self.artificial_vars: list[tuple[int, Symbol]] = []
        self.penalized_vars: list[tuple[int, int, Symbol]] = []
        self.symbols_in_z_rows: list[Symbol] = []
        self.z_rows_symbols: list[Symbol] = []
        self.result: dict = {}


    def solve(self) -> None:
        self.__standardize_coeff()
        self.__standardize_z_rows()

        if self.artificial_vars:
            match self.artificial_solution_method:
                case ArtificialSolutionMethod.BIG_M:
                    self.__init_big_m()
                case ArtificialSolutionMethod.TWO_PHASE:
                    self.__init_two_phase()

        simplex_engine = SimplexEngine(self.objective_function_coefficients_vector,
                                       self.symbols_in_z_rows,
                                       self.aug_constraints_coefficients_matrix,
                                       self.vars,
                                       self.basic_vars,
                                       self.is_maximization,
                                       self.steps,
                                       self.z_rows_symbols)
        simplex_engine.reduce()
        self.__build_result(simplex_engine)


    def __standardize_z_rows(self):
        if self.aug_goals_coefficients_matrix:
            self.__standardize_goal_programming_z_rows()
        else:
            self.z_rows_symbols = [Symbol('z')]
            self.__standardize_single_objective_simplex_z_rows()


    def __standardize_single_objective_simplex_z_rows(self):
         self.objective_function_coefficients_vector *= -1
         self.objective_function_coefficients_vector = self.objective_function_coefficients_vector.row_join(Matrix([
            [0] * (self.aug_constraints_coefficients_matrix.cols - self.objective_function_coefficients_vector.cols)
        ]))


    def __standardize_goal_programming_z_rows(self):
        self.z_rows_symbols = [Symbol(f'G_{i}') for i in range(1, self.aug_goals_coefficients_matrix.rows + 1)]
        self.aug_constraints_coefficients_matrix = self.aug_goals_coefficients_matrix.col_join(
            self.aug_constraints_coefficients_matrix)
        self.is_maximization = False
        cols = self.aug_constraints_coefficients_matrix.cols
        new_z = []
        for p in self.penalized_vars:
            penalty_sym = Symbol(f'P_{p[0] + 1}', positive=True)
            penalized_var_sym = p[2]
            col_index = self.vars.index(penalized_var_sym)
            if p[0] < len(new_z):
                new_z[p[0]][col_index] = -penalty_sym
            else:
                zero_row = [0] * cols
                zero_row[col_index] = -penalty_sym
                new_z.append(zero_row)
                self.symbols_in_z_rows.append(penalty_sym)

        self.objective_function_coefficients_vector = Matrix(new_z)


    def __init_big_m(self):
        M = Symbol('M', positive=True)
        self.symbols_in_z_rows = [M]
        big_m_coeff = M if self.is_maximization else -M
        for a in self.artificial_vars:
            artificial_var_sym = a[1]
            col_index = self.vars.index(artificial_var_sym)
            self.objective_function_coefficients_vector[col_index] = big_m_coeff


    def __init_two_phase(self):
        cols = self.aug_constraints_coefficients_matrix.cols
        num_artificial_vars = len(self.artificial_vars)
        intermediate_z = Matrix([[0] * (cols - num_artificial_vars - 1) + [-1] * num_artificial_vars + [0]])
        simplex_engine = SimplexEngine(intermediate_z, [None],
                                       self.aug_constraints_coefficients_matrix,
                                       self.vars,
                                       self.basic_vars,
                                       False,
                                       self.steps,
                                       [Symbol('r')])
        simplex_engine.reduce()
        self.aug_constraints_coefficients_matrix = simplex_engine.m
        self.basic_vars = simplex_engine.x_bv

        # Remove artificial columns (column drop)
        for a in self.artificial_vars:
            col_index = self.vars.index(a[1])
            self.vars.remove(a[1])
            self.aug_constraints_coefficients_matrix.col_del(col_index)
            self.objective_function_coefficients_vector.col_del(col_index)

        self.steps.pop()


    def __standardize_coeff(self):
        # Create decision variables, add them to vars list and
        # insert new columns for unrestricted variables
        self.__init_decision_vars()

        # Create excess, artificial and slack variables
        excess_vars, self.artificial_vars, slack_vars = self.__create_constraints_vars()

        # Create penalized and favored variables
        self.penalized_vars, favored_vars = self.__create_deviation_vars()

        # Append excess variables columns
        for e in excess_vars:
            self.__append_constraint_var_col(e[0], -1)

        # Append favored variables columns
        for f in favored_vars:
            self.__append_deviation_var_col(f[0], f[1])

        # Append penalized variables columns
        for p in self.penalized_vars:
            self.__append_deviation_var_col(p[0], p[1])

        # Append slack variables columns
        for s in slack_vars:
            self.__append_constraint_var_col(s[0], 1)

        # Append artificial variables columns
        for a in self.artificial_vars:
            self.__append_constraint_var_col(a[0], 1)

        # Add deviation and constraints variables to vars list
        self.vars += [e[1] for e in excess_vars]            \
                     + [f[2] for f in favored_vars]         \
                     + [p[2] for p in self.penalized_vars]  \
                     + [s[1] for s in slack_vars]           \
                     + [a[1] for a in self.artificial_vars]

        # Add basic variables
        self.basic_vars += [p[2] for p in list(filter(lambda pv: pv[1] > 0, self.penalized_vars))]    \
                           + [s[1] for s in slack_vars]           \
                           + [a[1] for a in self.artificial_vars]


    def __init_decision_vars(self) -> None:
        num_inserted_cols = 0
        for i in range(len(self.restricted)):
            if not self.restricted[i]:
                negated_col = -self.aug_constraints_coefficients_matrix[:, i + num_inserted_cols]
                self.aug_constraints_coefficients_matrix = self.aug_constraints_coefficients_matrix.col_insert(i + num_inserted_cols + 1, negated_col)
                self.vars.append(Symbol(f"x_{i + 1}^+"))
                self.vars.append(Symbol(f"x_{i + 1}^-"))
                self.unrestricted_decision_vars.append((i , Symbol(f"x_{i + 1}^+"), Symbol(f"x_{i + 1}^-")))
                if self.aug_goals_coefficients_matrix:
                    negated_col = -self.aug_goals_coefficients_matrix[:, i + num_inserted_cols]
                    self.aug_goals_coefficients_matrix = self.aug_goals_coefficients_matrix.col_insert(i + num_inserted_cols + 1, negated_col)
                else:
                    negated_col = -self.objective_function_coefficients_vector[:, i + num_inserted_cols]
                    self.objective_function_coefficients_vector = self.objective_function_coefficients_vector.col_insert(i + num_inserted_cols + 1, negated_col)
                num_inserted_cols += 1
            else:
                self.vars.append(Symbol(f"x_{i + 1}"))
                self.restricted_decision_vars.append((i, Symbol( f"x_{i + 1}")))


    def __create_constraints_vars(self) -> tuple[list[tuple[int, Symbol]],
                                                 list[tuple[int, Symbol]],
                                                 list[tuple[int, Symbol]]]:
        excess_vars : list[tuple[int, Symbol]] = []
        artificial_vars : list[tuple[int, Symbol]] = []
        slack_vars : list[tuple[int, Symbol]] = []
        for idx, relation in enumerate(self.constraints_relations):
            match relation:
                case RelationOperator.GEQ:
                    excess_vars.append((idx, Symbol(f"e_{idx + 1}")))
                    artificial_vars.append((idx, Symbol(f"a_{idx + 1}")))
                case RelationOperator.EQU:
                    artificial_vars.append((idx, Symbol(f"a_{idx + 1}")))
                case RelationOperator.LEQ:
                    slack_vars.append((idx, Symbol(f"s_{idx + 1}")))
        return excess_vars, artificial_vars, slack_vars


    def __create_deviation_vars(self) -> tuple[list[tuple[int, int, Symbol]],
                                               list[tuple[int, int, Symbol]]]:
        penalized_vars: list[tuple[int, int, Symbol]] = []
        favored_vars: list[tuple[int, int, Symbol]] = []
        if self.aug_goals_coefficients_matrix:
            for idx, relation in enumerate(self.goals_relations):
                match relation:
                    case RelationOperator.GEQ:
                        penalized_vars.append((idx, 1, Symbol(f"y_{idx + 1}^-")))
                        favored_vars.append((idx, -1, Symbol(f"y_{idx + 1}^+")))
                    case RelationOperator.EQU:
                        penalized_vars.append((idx, 1, Symbol(f"y_{idx + 1}^-")))
                        penalized_vars.append((idx, -1, Symbol(f"y_{idx + 1}^+")))
                    case RelationOperator.LEQ:
                        favored_vars.append((idx, 1, Symbol(f"y_{idx + 1}^-")))
                        penalized_vars.append((idx, -1, Symbol(f"y_{idx + 1}^+")))

        return penalized_vars, favored_vars


    def __append_deviation_var_col(self, var_row_index: int, sign: int):
        insert_at_col = self.aug_constraints_coefficients_matrix.cols - 1
        col = self.__create_col(self.aug_goals_coefficients_matrix.rows, var_row_index, sign)
        self.aug_goals_coefficients_matrix = self.aug_goals_coefficients_matrix.col_insert(insert_at_col, col)
        zero_col = Matrix.zeros(self.aug_constraints_coefficients_matrix.rows, 1)
        self.aug_constraints_coefficients_matrix = self.aug_constraints_coefficients_matrix.col_insert(insert_at_col,zero_col)


    def __append_constraint_var_col(self, var_row_index: int, sign: int):
        insert_at_col = self.aug_constraints_coefficients_matrix.cols - 1
        col = self.__create_col(self.aug_constraints_coefficients_matrix.rows, var_row_index, sign)
        self.aug_constraints_coefficients_matrix = self.aug_constraints_coefficients_matrix.col_insert(insert_at_col,
                                                                                                       col)
        if self.aug_goals_coefficients_matrix:
            zero_col = Matrix.zeros(self.aug_goals_coefficients_matrix.rows, 1)
            self.aug_goals_coefficients_matrix = self.aug_goals_coefficients_matrix.col_insert(insert_at_col, zero_col)


    def __build_result(self, simplex_engine: SimplexEngine) -> None:
        self.result["steps"] = self.steps
        self.result["isOptimal"] = simplex_engine.is_optimal
        self.__build__optimal_deci_vars_vals(simplex_engine)
        if self.aug_goals_coefficients_matrix:
            self.__build_goals_result(simplex_engine)
        else:
            self.__build_standard_result(simplex_engine)
        self.__build_final_comment(simplex_engine)


    def __build_goals_result(self, simplex_engine: SimplexEngine):
        goals_satisfied = []
        goals_unsatisfied = []
        for i in range(len(self.z_rows_symbols)):
            if self.__is_satisfied(i, simplex_engine):
                goals_satisfied.append(self.z_rows_symbols[i])
            else:
                goals_unsatisfied.append(self.z_rows_symbols[i])
        self.result["goalsSatisfied"] = goals_satisfied
        self.result["goalsUnsatisfied"] = goals_unsatisfied


    def __is_satisfied(self, row_index: int, simplex_engine: SimplexEngine) -> bool:
        for col_index in range(simplex_engine.z_rows.cols - 1):
            s = simplex_engine.z_rows[row_index, col_index]
            if compare_expressions(s, 0, self.symbols_in_z_rows[row_index]) > 0 and simplex_engine.x[col_index] not in simplex_engine.x_bv:
                return False
        return True


    def __build_standard_result(self, simplex_engine: SimplexEngine):
        self.__build__optimal_obj_func_val(simplex_engine)


    def __build__optimal_obj_func_val(self, simplex_engine: SimplexEngine):
        se_cols = simplex_engine.m.cols
        self.result["optimalObjectiveFunctionValue"] = simplex_engine.z_rows[0, se_cols - 1]


    def __build__optimal_deci_vars_vals(self, simplex_engine: SimplexEngine):
        se_cols = simplex_engine.m.cols
        sol_list = [0 for _ in self.restricted]

        for rv_index, rv_symbol in self.restricted_decision_vars:
            if rv_symbol in self.basic_vars:
                row_index = simplex_engine.x_bv.index(rv_symbol)
                sol_list[rv_index] = simplex_engine.m[row_index, se_cols - 1]

        for urv_index, urv_pos_symbol, urv_neg_symbol in self.unrestricted_decision_vars:
            if urv_pos_symbol in simplex_engine.x_bv:
                row_index = simplex_engine.x_bv.index(urv_pos_symbol)
                sol_list[urv_index] = simplex_engine.m[row_index, se_cols - 1]
            elif urv_neg_symbol in simplex_engine.x_bv:
                row_index = simplex_engine.x_bv.index(urv_neg_symbol)
                sol_list[urv_index] = -simplex_engine.m[row_index, se_cols - 1]

        self.result["optimalDecisionVariablesValues"] = sol_list


    def __build_final_comment(self, simplex_engine: SimplexEngine):
        comment = ""
        if self.aug_goals_coefficients_matrix:
            if self.result["goalsSatisfied"]:
                comment += "Goals satisfied: " + ", ".join(
                    map(lambda g: f"${latex(g)}$", self.result["goalsSatisfied"])) + "\n"
            if self.result["goalsUnsatisfied"]:
                comment += "Goals unsatisfied: " + ", ".join(map(lambda g: f"${latex(g)}$", self.result["goalsUnsatisfied"])) + "\n"
        else:
            comment += f"Optimal solution found at ${self.z_rows_symbols[0]} = {self.result["optimalObjectiveFunctionValue"]}$" + "\n" \
                if simplex_engine.is_optimal else "Problem is infeasible\n"

        if simplex_engine.is_optimal:
            comment += "Where (" + ", ".join([f"$x_{i}$" for i in range(1, len(self.restricted) + 1)]) + ") $=$ (" \
                    + ", ".join(map(lambda s: f"${latex(s)}$", self.result["optimalDecisionVariablesValues"])) + ")"
        self.result["steps"][-1]["comment"] = comment
        print(comment)


    @staticmethod
    def __create_col(rows: int, non_zero_index: int, sign: int) -> Matrix:
        col = Matrix.zeros(rows, 1)
        col[non_zero_index, 0] = sign
        return col