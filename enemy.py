import pygame
from settings import *
from random import choice


class Enemy:
    def __init__(self, hp, name):
        self.hp = hp
        self.max_hp = hp
        self.moves = player_specific_moves[name] if name in player_specific_moves else default_moves
        self.name = name

    def attack(self) -> str:
        # pick random move
        move = choice(list(self.moves.keys()))
        return move
