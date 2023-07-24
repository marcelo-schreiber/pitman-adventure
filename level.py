import pygame


class Level:
    def __init__(self):
        self.visible_sprites = pygame.sprite.Group()  # non collide sprites
        self.obstacle_sprites = pygame.sprite.Group()  # collide sprites

    def run(self):
        pass