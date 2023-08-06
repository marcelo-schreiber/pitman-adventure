import pygame
from textbox import *
from settings import TILESIZE

class Npc(pygame.sprite.Sprite):

    def __init__(self, groups, pos, name, messages):
        super().__init__(groups)

        self.image = pygame.image.load('graphics/npcs/' + name + '.png').convert_alpha()
        self.rect = self.image.get_rect()
        pos = (pos[0] * TILESIZE, pos[1] * TILESIZE)
        self.rect.topleft = pos

        self.messages = messages

        self.textbox = Textbox()

    def begin_interaction(self):
        self.textbox.start_text(messages=self.messages)