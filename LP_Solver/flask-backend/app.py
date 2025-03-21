from flask import Flask, request, jsonify
from marshmallow import ValidationError
from flask_cors import CORS
from data_mapper import Marshaller
from simplex.solver import SimplexSolver

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()

        simplex_input = Marshaller.convert_input_data(data)
        simplex_solver = SimplexSolver(**simplex_input)
        simplex_solver.solve()
        output = Marshaller.convert_output_data(simplex_solver)
        return jsonify(output), 200

    except ValidationError as err:
        return jsonify({"error": "Invalid input", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
