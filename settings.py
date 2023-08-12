WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 90

moves = {
    "weak": {"name": "Weak", "damage": 10, "accuracy": 0.95},
    "medium": {"name": "Medium", "damage": 15, "accuracy": 0.8},
    "strong": {"name": "Strong", "damage": 20, "accuracy": 0.7},
    "heal": {"name": "Heal", "damage": -20, "accuracy": 0.7},
}

default_moves = moves.copy()

player_specific_moves = {
    "leo": {
        "weak": {"name": "Blue", "damage": 10, "accuracy": 0.95},
        "strong": {"name": "Dinosaur", "damage": 20, "accuracy": 0.7},
        "heal": {"name": "Autism", "damage": -20, "accuracy": 0.7},
    },
    "daniel": {
        "weak": {"name": "Sketch", "damage": 10, "accuracy": 0.95},
        "strong": {"name": "Full render", "damage": 20, "accuracy": 0.7},
        "heal": {"name": "Sleep", "damage": -20, "accuracy": 0.7},
    },
    "fenoxer_muie" : {
        "weak": {"name": "Femboy hips", "damage": 10, "accuracy": 0.95},
        "strong": {"name": "Dwarven might", "damage": 20, "accuracy": 0.7},
        "heal": {"name": "Ruacutan", "damage": -20, "accuracy": 0.7},
    }
}