import pygame
from textbox import *
from settings import TILESIZE


class Npc(pygame.sprite.Sprite):
    def __init__(self, groups, pos, name, messages):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/npcs/" + name + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        pos = (pos[0] * TILESIZE, pos[1] * TILESIZE)
        self.rect = self.image.get_rect(topleft=pos)

        self.messages = messages

        self.textbox = Textbox()

    def begin_interaction(self):
        self.textbox.start_text(messages=self.messages)

    def update(self):
        pass


class GymTrainer(Npc):
    def __init__(self, groups, pos, name, messages, player):
        super().__init__(groups, pos, name, messages)

        self.player = player
        self.start_fight = False
        self.conv_end = False

        self.defeated = False

    def begin_interaction(self):
        self.textbox.start_text(messages=self.messages, func=self.player.battle)
