import pygame
from settings import *
from random import randint
from enemy import Enemy
from cutscene import BattleCutscene


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, grass_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('images/tile.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.hp = 100
        self.max_hp = 100
        self.grass_sprites = grass_sprites
        self.direction = pygame.math.Vector2()
        self.speed = 7

        self.obstacle_sprites = obstacle_sprites
        self.chance_of_encounter_per_tick = 1 / (3 * FPS)  # 1 encounter per 3 seconds moving (60 FPS)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def random_encounter(self):
        is_colliding = pygame.sprite.spritecollideany(self, self.grass_sprites)
        is_moving = self.direction.magnitude() != 0

        if is_colliding and is_moving:
            range_of_numbers = 1 / self.chance_of_encounter_per_tick
            random_encounter = randint(1, range_of_numbers)

            if random_encounter == 1:
                self.battle()

    def battle(self):
        print('battle')
        enemy = Enemy(100)
        cutscene = BattleCutscene(self, 'images/tile.png', 'graphics/monsters/bamboo/attack/0.png', enemy.hp)
        cutscene.play()

    def update(self):
        self.input()
        self.move(self.speed)
        self.random_encounter()
