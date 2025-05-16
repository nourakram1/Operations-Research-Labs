generate_game_schema = {
    "type": "object",
    "properties": {
        "n": {"type": "integer"},
        "m": {"type": "integer", "default": 1}
    },
    "required": ["n"],
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
                "type": "array",
                "items": {
                    "type": "number"
                }
            }
        }
    },
    "required": ["n", "m", "probabilities"],
    "additionalProperties": False,
}


    