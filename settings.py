WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 90

moves = {
    "weak": {"name": "Fox swipes", "damage": 10, "accuracy": 0.90},
    "medium": {"name": "Nouveau slash", "damage": 15, "accuracy": 0.75},
    "strong": {"name": "Fuckery", "damage": 20, "accuracy": 0.52},
    "heal": {"name": "Healing spit", "damage": -20, "accuracy": 0.55},
}

default_moves = moves.copy()

player_specific_moves = {
    "leo": {
        "weak": {"name": "Blue", "damage": 15, "accuracy": 0.90},
        "strong": {"name": "Dinosaur", "damage": 20, "accuracy": 0.7},
        "heal": {"name": "Autism", "damage": -20, "accuracy": 0.7},
    },
    "daniel": {
        "weak": {"name": "Sketch", "damage": 10, "accuracy": 0.95},
        "strong": {"name": "Full render", "damage": 20, "accuracy": 0.75},
        "heal": {"name": "Sleep", "damage": -20, "accuracy": 0.7},
    },
    "fenoxer_muie" : {
        "weak": {"name": "Femboy hips", "damage": 10, "accuracy": 0.95},
        "strong": {"name": "Dwarven might", "damage": 45, "accuracy": 0.5},
        "heal": {"name": "Ruacutan", "damage": -20, "accuracy": 0.75},
    }
}

player_specific_hp = {
    "leo": 60,
    "daniel": 120,
    "fenoxer_muie": 45,
}