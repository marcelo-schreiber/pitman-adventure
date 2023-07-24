import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type  # enemy, invisible, etc

        self.image = surface
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

        if sprite_type == 'object':
            self.image = pygame.transform.scale(self.image, (TILESIZE*2, TILESIZE*2))
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, -0.12 * TILESIZE)
