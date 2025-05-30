import numpy as np
from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError
from app.schema import generate_game_schema, play_schema, play_response_schema, generate_game_response_schema, simulate_schema, simulate_response_schema
from game_board import GameBoard
from game_matrix import GameMatrix
from game_solver import GameSolver
from player import Player
from proximity_penalty import ProximityPenalty
from test import Test

bp = Blueprint('api', __name__)

@bp.route('/generate', methods=['POST'])
def generate_game():
    data = request.get_json(force=True)
    try:
        validate(instance=data, schema= generate_game_schema)
    except ValidationError as e:
        return jsonify({
            'error': e.message,
            'path': list(e.path)
        }), 400
    
    n, m, proximity = data["n"], data["m"], data["proximity"]
    
    if Test.test_mode:
        try:
            game_board, proximity = Test.get_test_case()
            n, m = game_board.shape
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    else:
        game_board = GameBoard.generate(n, m)
    
    game_matrix = GameMatrix.generate(game_board)
    
    if proximity:
        game_matrix = ProximityPenalty.apply(game_matrix, n, m)

    hider_probabilities = GameSolver.solve_hider_strategy(game_matrix)
    seeker_probabilities = GameSolver.solve_seeker_strategy(game_matrix)
    
    response = {
        'gameMatrix': game_matrix.tolist(),
        'gameBoard': [[cell.label for cell in row] for row in game_board],
        'seekerProbabilities': seeker_probabilities.tolist(),
        'hiderProbabilities': hider_probabilities.tolist()
    }
    try:
        validate(instance=response, schema=generate_game_response_schema)
    except ValidationError as e:
        return jsonify({
            'error': f"Internal response validation error: {e.message}",
            'path': list(e.path)
        }), 500
    return jsonify(response), 200

@bp.route('/play', methods=['POST'])
def play():
    data = request.get_json(force=True)
    try:
        validate(instance=data, schema = play_schema)
    except ValidationError as e:
        return jsonify({
            'error': e.message,
            'path': list(e.path)
        }), 400

    i, j = Player.play(data["n"], data["m"], np.array(data["probabilities"]))
    
    response = {'row': i, 'col': j}
    try:
        validate(instance=response, schema=play_response_schema)
    except ValidationError as e:
        return jsonify({
            'error': f"Internal response validation error: {e.message}",
            'path': list(e.path)
        }), 500
    return jsonify(response), 200

@bp.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json(force=True)
    try:
        validate(instance=data, schema = simulate_schema)
    except ValidationError as e:
        return jsonify({
            'error': e.message,
            'path': list(e.path)
        }), 400
    
    moves = Player.play_n(data["n"], data["m"], np.array(data["probabilities"]), data["num"])
    
    response = { 'moves': moves }
    try:
        validate(instance=response, schema = simulate_response_schema)
    except ValidationError as e:
        return jsonify({
            'error': f"Internal response validation error: {e.message}",
            'path': list(e.path)
        }), 500
    return jsonify(response), 200