from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def solve():
    return jsonify({"Message": "Hello World"})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
