import json
import os

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'schemas')

def load_schema(filename):
    with open(os.path.join(SCHEMA_DIR, filename), 'r') as f:
        return json.load(f)

generate_game_schema = load_schema('generate_game_schema.json')
play_schema = load_schema('play_schema.json')
generate_game_response_schema = load_schema('generate_game_response_schema.json')
play_response_schema = load_schema('play_response_schema.json')
simulate_schema = load_schema('simulate_schema.json')
simulate_response_schema = load_schema('simulate_response_schema.json')