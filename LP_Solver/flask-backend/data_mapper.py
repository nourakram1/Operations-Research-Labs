from marshmallow import Schema, fields, validate, ValidationError
from sympy import Matrix, latex, nsimplify
from simplex.enums import RelationOperator, ArtificialSolutionMethod


class SimplexSchema(Schema):
    objectiveFunctionCoefficientsVector = fields.List(fields.List(fields.Number()), required=False, missing=None)
    constraintsCoefficientsMatrix = fields.List(fields.List(fields.Number()), required=True)
    constraintsRelations = fields.List(fields.Str(validate=validate.OneOf([">=", "=", "<="])), required=True)
    goalsCoefficientsMatrix = fields.List(fields.List(fields.Number()), required=False, missing=None)
    goalsRelations = fields.List(fields.Str(validate=validate.OneOf([">=", "=", "<="])), required=False, missing=None)
    restricted = fields.List(fields.Boolean(), required=True)
    isMaximization = fields.Boolean(required=False, missing=None)
    method = fields.Str(required=False, validate=validate.OneOf(["M", "TP"]), missing=None)


class Marshaller:
    schema = SimplexSchema()

    @staticmethod
    def convert_input_data(data):
        try:
            validated_data = Marshaller.schema.load(data)
        except ValidationError as err:
            raise ValueError(f"Invalid input data: {err.messages}")

        print("Validated input data")
        print(validated_data)
        simplex_input: dict = {}

        if validated_data["objectiveFunctionCoefficientsVector"]:
            simplex_input["objective_function_coefficients_vector"] = Matrix(
                [[nsimplify(val) for val in row] for row in validated_data["objectiveFunctionCoefficientsVector"]])
        else:
            simplex_input["objective_function_coefficients_vector"] = None
        simplex_input["aug_constraints_coefficients_matrix"] = Matrix([[nsimplify(val) for val in row] for row in validated_data["constraintsCoefficientsMatrix"]])
        simplex_input["constraints_relations"] = [RelationOperator(op) for op in validated_data["constraintsRelations"]]
        if validated_data["goalsCoefficientsMatrix"]:
            simplex_input["aug_goals_coefficients_matrix"] = Matrix(
                [[nsimplify(val) for val in row] for row in validated_data["goalsCoefficientsMatrix"]])
        else:
            simplex_input["aug_goals_coefficients_matrix"] = None
        if validated_data["goalsRelations"]:
            simplex_input["goals_relations"] = [RelationOperator(op) for op in validated_data["goalsRelations"]]
        else:
            simplex_input["goals_relations"] = None
        simplex_input["restricted"] = list(map(bool, validated_data["restricted"]))
        simplex_input["is_maximization"] = validated_data["isMaximization"]
        if validated_data["method"]:
             simplex_input["artificial_solution_method"] = ArtificialSolutionMethod.BIG_M if validated_data["method"] == "M" \
                else ArtificialSolutionMethod.TWO_PHASE
        else:
            simplex_input["artificial_solution_method"] = None

        print("Simplex input:")
        print(simplex_input)
        return simplex_input

    @staticmethod
    def convert_output_data(result):
        print("Simplex result:")
        r: dict = {
            "steps": [
                {
                    "variables": [latex(var) for var in step["variables"]],
                    "zRowsSymbols": [latex(z) for z in step["zRowsSymbols"]],
                    "basicVariables": [latex(var) for var in step["basicVariables"]],
                    "simplexMatrix": [[latex(cell) for cell in row] for row in step["simplexMatrix"]],
                    "enteringVariableIndex": step.get("enteringVariableIndex"),
                    "leavingVariableIndex": step.get("leavingVariableIndex"),
                    "comment": step["comment"]
                }
                for step in result["steps"]
            ],
            "status": result["status"].value,
            "finalDecisionVariablesValues": [latex(val) for val in result["finalDecisionVariablesValues"]]
        }
        if result.get("goalsSatisfied"):
            r["goalsSatisfied"] = [latex(goal) for goal in result.get("goalsSatisfied", [])]
        else:
            r["finalObjectiveFunctionValue"] =  latex(result["finalObjectiveFunctionValue"])

        return r

