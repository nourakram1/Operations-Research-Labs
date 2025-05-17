import numpy as np
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from game_board import GameBoard
from game_matrix import GameMatrix
from game_solver import GameSolver
from player import Player

bp = Blueprint('api', __name__)
CORS(bp)

@bp.route('/generate', methods=['POST'])
def generate_game():
    data = request.get_json(force=True)

    game_board = GameBoard.generate(data["n"], data["m"])
    game_matrix = GameMatrix.generate(game_board)
    seeker_probabilities , hider_probabilities = GameSolver.solve(game_matrix)

    response = {
        'gameMatrix': game_matrix.tolist(),
        'gameBoard': [[cell.label for cell in row] for row in game_board],
        'seekerProbabilities': seeker_probabilities.tolist(),
        'hiderProbabilities': hider_probabilities.tolist()
    }

    return jsonify(response), 200

@bp.route('/play', methods=['POST'])
def play():
    data = request.get_json(force=True)
    i, j = Player.play(data["n"], data["m"], np.array(data["probabilities"]))
    
    response = {'row': i, 'col': j}
    return jsonify(response), 200