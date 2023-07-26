import pygame
from settings import *
from random import choice


class Enemy:
    def __init__(self, hp):
        self.hp = hp
        self.max_hp = hp
        self.moves = moves

    def attack(self):
        # pick random move
        move = choice(list(self.moves.values()))

        return move
