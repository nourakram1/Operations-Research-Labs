import json
import os

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'schema')

def load_schema(filename):
    with open(os.path.join(SCHEMA_DIR, filename), 'r') as f:
        return json.load(f)

generate_game_schema = load_schema('generate_request.json')
play_schema = load_schema('play_request.json')
generate_game_response_schema = load_schema('generate_response.json')
play_response_schema = load_schema('play_response.json')
simulate_schema = load_schema('simulate_request.json')
simulate_response_schema = load_schema('simulate_response.json')