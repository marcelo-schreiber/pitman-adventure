import pygame
from settings import *
from tile import Tile
from player import Player
from utils import import_csv_layout, import_folder
import random

from textbox import *
from npc import Npc
from messages import *


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.grass_sprites = pygame.sprite.Group()  # for random encounter
        self.npc_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        self.player = None
        self.initialize_player()
        
        self.s1 = Textbox()
        self.s1.start_text(intro)

        self.create_npc()

    def initialize_player(self):
        player_initial_x = TILESIZE * 11
        player_initial_y = TILESIZE * 11

        self.player = Player((player_initial_x, player_initial_y),
                             [self.visible_sprites], self.obstacle_sprites, self.grass_sprites, self.npc_sprites)
    
    def create_npc(self):
        groups = [self.visible_sprites, self.npc_sprites]
        Npc(groups, (9, 10), 'spirit', villager_1)

    def create_map(self):
        layouts = {  # list of layouts (collision, visuals, etc)
            'boundary': import_csv_layout('map/map_Collision.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_LargeObjects.csv'),
            'details': import_csv_layout('map/map_Details.csv')
        }

        graphics = {  # list of images
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
                    # if style == 'object':
                    #     Tile((x, y), [self.obstacle_sprites], 'object')

                    # if style == 'grass':
                    #     random_grass_surface = random.choice(graphics['grass'])
                    #     Tile((x, y), [self.visible_sprites, self.grass_sprites], 'grass', random_grass_surface)

                    # if style == 'npcs':
                    #     Npc([self.visible_sprites, self.npc_sprites], (x, y))

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)

        if self.s1.active:
            self.s1.draw()
            self.s1.update()
        else:
            self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        layout = import_csv_layout('map/map_FloorBlocks.csv')
        # create floor
        self.floor_surface = pygame.image.load('tilemap/pitman-map.png').convert()
        # scale to layout size * TILE_SIZE
        self.floor_surface = pygame.transform.scale(self.floor_surface,
                                                    (len(layout[0]) * TILESIZE, len(layout) * TILESIZE))

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
