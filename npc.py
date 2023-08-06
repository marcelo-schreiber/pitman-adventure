import pygame
from textbox import *
from settings import TILESIZE

class Npc(pygame.sprite.Sprite):

    def __init__(self, groups, pos, name, messages):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/npcs/' + name + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        pos = (pos[0] * TILESIZE, pos[1] * TILESIZE)
        self.rect.topleft = pos

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
        if not self.defeated:
            self.textbox.start_text(messages=self.messages)
            self.start_fight = True

    def update(self):
        if self.defeated:
            return

        if not self.textbox.active and self.start_fight:
            self.conv_end = True

        if self.conv_end:
            self.player.battle()
            self.conv_end = False
            self.defeated = True
