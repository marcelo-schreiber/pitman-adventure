import pygame
from settings import *
from random import randint
from enemy import Enemy
from battle import BattleCutscene


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, grass_sprites, npc_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("images/danites3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.hp = 100
        self.max_hp = 100
        self.name = "Arthur"
        self.grass_sprites = grass_sprites
        self.direction = pygame.math.Vector2()
        self.speed = 7

        self.obstacle_sprites = obstacle_sprites
        self.chance_of_encounter_per_tick = 1 / (
            3 * FPS
        )  # 1 encounter per 3 seconds moving (60 FPS)

        self.npc_sprites = npc_sprites
        self.can_interact = True

        self.images = {
            "down": pygame.transform.scale(
                pygame.image.load("images/danites1.png").convert_alpha(),
                (TILESIZE, TILESIZE),
            ),
            "left": pygame.transform.scale(
                pygame.image.load("images/danites3.png").convert_alpha(),
                (TILESIZE, TILESIZE),
            ),
            "up": pygame.transform.scale(
                pygame.image.load("images/danites2.png").convert_alpha(),
                (TILESIZE, TILESIZE),
            ),
            "right": pygame.transform.scale(
                pygame.transform.flip(
                    pygame.image.load("images/danites3.png").convert_alpha(),
                    True,
                    False,
                ),
                (TILESIZE, TILESIZE),
            ),
        }

        self.talking_image = pygame.image.load("images/danites3.png").convert_alpha()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.image = self.images["up"]
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.image = self.images["down"]
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.image = self.images["right"]
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.image = self.images["left"]
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def random_encounter(self):
        is_colliding = pygame.sprite.spritecollideany(self, self.npc_sprites)
        is_moving = self.direction.magnitude() != 0

        if is_colliding and is_moving:
            range_of_numbers = 1 / self.chance_of_encounter_per_tick
            random_encounter = randint(1, range_of_numbers)

            if random_encounter == 1:
                self.battle()

    def npc_interaction(self):
        npcs_collided = pygame.sprite.spritecollide(self, self.npc_sprites, False)

        if npcs_collided:
            if self.can_interact:
                for npc in npcs_collided:
                    npc.begin_interaction()
                self.can_interact = False
        else:
            if not self.can_interact:
                self.can_interact = True

    def battle(self):
        print("battle")
        enemy = Enemy(100, "Bamboo")
        cutscene = BattleCutscene(
            self,
            "images/danites2.png",
            "graphics/monsters/bamboo/attack/0.png",
            enemy,
        )
        cutscene.play()
        print(cutscene.winner)

    def update(self):
        self.input()
        self.move(self.speed)
        self.random_encounter()
        self.npc_interaction()
