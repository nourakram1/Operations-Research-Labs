from marshmallow import Schema, fields, ValidationError
from sympy import Matrix
from simplex.simplex_enums import RelationOperator, ArtificialSolutionMethod
from simplex.solver import SimplexSolver


class SimplexSchema(Schema):
    objective_function_coefficients_vector = fields.List(fields.Float(), required=False, missing=None)
    constraints_coefficients_matrix = fields.List(fields.List(fields.Float()), required=True)
    constraints_relations = fields.List(fields.Str(), required=True)
    goals_coefficients_matrix = fields.List(fields.List(fields.Float()), required=False, missing=None)
    goals_relations = fields.List(fields.Str(), required=False, missing=None)
    restricted = fields.List(fields.Boolean(), required=True)
    isMaximization = fields.Boolean(required=False, missing=None)
    method = fields.Str(required=True, validate=lambda x: x in ["M", "TP"])

class Marshaller:
    schema = SimplexSchema()

    @staticmethod
    def convert_input_data(data):
        try:
            validated_data = Marshaller.schema.load(data)
        except ValidationError as err:
            raise ValueError(f"Invalid input data: {err.messages}")

        return {
            "objective_function_coefficients_vector": (
                Matrix(validated_data["objective_function_coefficients_vector"])
                if validated_data["objective_function_coefficients_vector"] is not None else None
            ),
            "aug_constraints_coefficients_matrix": Matrix(validated_data["constraints_coefficients_matrix"]),
            "constraints_relations": [RelationOperator(op) for op in validated_data["constraints_relations"]],
            "aug_goals_coefficients_matrix": (
                Matrix(validated_data["goals_coefficients_matrix"])
                if validated_data["goals_coefficients_matrix"] is not None else None
            ),
            "goals_relations": [RelationOperator(op) for op in validated_data.get("goals_relations", [])],
            "restricted": list(map(bool, validated_data["restricted"])),
            "is_maximization": validated_data["isMaximization"],
            "artificial_solution_method": (
                ArtificialSolutionMethod.BIG_M if validated_data["method"] == "M"
                else ArtificialSolutionMethod.TWO_PHASE
            ),
        }

    @staticmethod
    def convert_output_data(simplex_solver: SimplexSolver):
        return {
            "variables": [str(var) for var in simplex_solver.vars],
            "steps": [
                {
                    "zRows": [str(z) for z in step["zRows"]],
                    "basicVariables": [str(var) for var in step["basicVariables"]],
                    "simplexMatrix": [[str(cell) for cell in row] for row in step["simplexMatrix"]],
                    "enteringVariable": step["enteringVariable"],
                    "leavingVariable": step["leavingVariable"],
                    "comment": step.get("comment", "")
                }
                for step in simplex_solver.steps
            ],
            "isOptimal": simplex_solver.result.get("isOptimal", False),
            "goalSatisfied": simplex_solver.result.get("goalSatisfied", []),
            "optimalSolution": simplex_solver.result.get("optimalSolution", None),
            "basicVariables": [str(var) for var in simplex_solver.basic_vars],
            "basicVariablesValues": simplex_solver.result.get("basicVariablesValues", [])
        }


