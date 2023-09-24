import pygame
pygame.init()

# command to generate .exe file:
# python -m PyInstaller --onefile --windowed --noconsole main.py

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 90

moves = {
    "weak": {"name": "Fox swipes", "damage": 10, "accuracy": 0.90},
    "medium": {"name": "Earth bending", "damage": 15, "accuracy": 0.75},
    "strong": {"name": "Fuckery", "damage": 20, "accuracy": 0.52},
    "heal": {"name": "Healing spit", "damage": -20, "accuracy": 0.55},
}

main_song = pygame.mixer.Sound("sounds/battle.mp3")

default_moves = moves.copy()

player_specific_moves = {
    "leo": {
        "weak": {"name": "Blue", "damage": 15, "accuracy": 0.92},
        "strong": {"name": "Dinosaur", "damage": 20, "accuracy": 0.7},
        "heal": {"name": "Autism", "damage": -20, "accuracy": 0.7},
    },
    "daniel": {
        "weak": {"name": "Sketch", "damage": 10, "accuracy": 0.95},
        "strong": {"name": "Full render", "damage": 20, "accuracy": 0.75},
        "heal": {"name": "Sleep", "damage": -20, "accuracy": 0.7},
    },
    "fenoxer_muie": {
        "weak": {"name": "Femboy hips", "damage": 10, "accuracy": 0.95},
        "strong": {"name": "Dwarven might", "damage": 65, "accuracy": 0.5},
        "heal": {"name": "Ruacutan", "damage": -20, "accuracy": 0.75},
    },
}

player_specific_hp = {
    "leo": 65,
    "daniel": 115,
    "fenoxer_muie": 45,
}
