import numpy as np
from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError
# from app.schema import generate_game_schema, play_schema
from game_board import GameBoard
from game_matrix import GameMatrix
from game_solver import GameSolver
from player import Player

bp = Blueprint('api', __name__)

@bp.route('/generate', methods=['POST'])
def generate_game():
    data = request.get_json(force=True)
    # try:
    #     validate(instance=data, schema= generate_game_schema)
    # except ValidationError as e:
    #     return jsonify({
    #         'valid': False,
    #         'error': e.message,
    #         'path': list(e.path)
    #     }), 400
    
    
    game_board = GameBoard.generate(data["n"], data["m"])
    game_matrix = GameMatrix.generate(game_board)
    seeker_probabilities , hider_probabilities = GameSolver.solve(game_matrix)

    return jsonify({
        'game_matrix': game_matrix.tolist(),
        'game_board': [[cell.label for cell in row] for row in game_board],
        'seeker_probabilities': seeker_probabilities.tolist(),
        'hider_probabilities': hider_probabilities.tolist()
    }), 200

@bp.route('/play', methods=['POST'])
def play():
    data = request.get_json(force=True)
    # try:
    #     validate(instance=data, schema = play_schema)
    # except ValidationError as e:
    #     return jsonify({
    #         'valid': False,
    #         'error': e.message,
    #         'path': list(e.path)
    #     }), 400

    i, j = Player.play(data["n"], data["m"], np.array(data["probabilities"]))
    
    return jsonify({'i': i, 'j': j}), 200