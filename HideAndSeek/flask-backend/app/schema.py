generate_game_schema = {
    "type": "object",
    "properties": {
        "n": {"type": "integer"},
        "m": {"type": "integer", "default": 1}
    },
    "required": ["n"],
    "additionalProperties": False
}

generate_game_response_schema = {
    "type": "object",
    "properties": {
        "valid": {"type": "boolean"},
        "game_board": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "game_matrix": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "number"}
            }
        },
        "seeker_probabilities": {
            "type": "array",
            "items": {"type": "number"}
        },
        "hider_probabilities": {
            "type": "array",
            "items": {"type": "number"}
        }
    },
    "required": ["valid", "game_board", "game_matrix", "seeker_probabilities", "hider_probabilities"],
    "additionalProperties": False
}

play_schema = {
    "type": "object",
    "properties": {
        "n": {"type": "integer"},
        "m": {"type": "integer", "default": 1},
        "probabilities": {
            "type": "array",
            "items": {
                "type": "number"
            }
        }
    },
    "required": ["n", "m", "probabilities"],
    "additionalProperties": False,
}

play_response_schema = {
    "type": "object",
    "properties": {
        "valid": {"type": "boolean"},
        "row": {"type": "integer"},
        "col": {"type": "integer"}
    },
    "required": ["valid", "row", "col"],
    "additionalProperties": False
}