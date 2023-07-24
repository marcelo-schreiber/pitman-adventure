import pygame
from settings import *
from tile import Tile
from player import Player
from utils import import_csv_layout, import_folder
import random


class Level:
    def __init__(self):

        # get the display surface
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.initialize_player()
        self.create_map()

    def initialize_player(self):
        player_initial_x = 2000
        player_initial_y = 1430
        self.player = Player((player_initial_x, player_initial_y), [self.visible_sprites], self.obstacle_sprites)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_LargeObjects.csv'),
        }

        graphics = {
            'grass': import_folder('graphics/grass'),
        }

        for style, layout in layouts.items():
            for row_idx, row in enumerate(layout):
                for col_idx, cell in enumerate(row):
                    if cell == '-1':
                        continue

                    x = col_idx * TILESIZE
                    y = row_idx * TILESIZE

                    if style == 'boundary':
                        Tile((x, y), [self.obstacle_sprites], 'boundary')

                    if style == 'grass':
                        random_grass_surface = random.choice(graphics['grass'])
                        Tile((x, y), [self.visible_sprites], 'grass', random_grass_surface)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # create floor
        self.floor_surface = pygame.image.load('tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw the floor
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
