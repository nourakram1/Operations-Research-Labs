from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request must not be null"}), 400

        # solver = SimplexSolver(data)
        # result = solver.solve()
        #return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)
