import pygame
import math

from settings import *
import time
from enemy import Enemy
import random


class Cutscene:
    def __init__(self):
        self.is_running = True
        self.screen = pygame.display.get_surface()
        self.actors = []
        self.texts = []
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)

    class Actor(Enemy):
        def __init__(self, name: str, x: int, y: int, width: int, height: int, enemy_hp=100):
            super().__init__(enemy_hp)
            try:
                self.image = pygame.image.load(name).convert_alpha()
                self.image = pygame.transform.scale(self.image, (width, height))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.type = "image_file"
            except FileNotFoundError:
                self.image = name
                self.rect = pygame.Rect(x, y, width, height)
                self.type = "solid_color"

    class Text:
        def __init__(self, string: str, x: int, y: int, color: str):
            self.text = string
            self.x = x
            self.y = y
            self.color = color

    def create_actor(self, name: str, x: int, y: int, width: int, height: int, enemy_hp=100):
        actor = self.Actor(name, x, y, width, height, enemy_hp)
        self.actors.append(actor)
        return actor

    def create_text(self, string, x: int, y: int, color: str):
        text = self.Text(string, x, y, color)
        self.texts.append(text)
        return text

    def background(self, image: str):
        new_img = pygame.image.load(image).convert_alpha()
        new_img = pygame.transform.scale(new_img, (WIDTH, HEIGHT))
        self.screen.blit(new_img, (0, 0))

    @staticmethod
    def move_to(rect, x, y, percentage):
        if abs(x - rect.x) < percentage and abs(y - rect.y) < percentage:
            return True

        hip = math.sqrt((x - rect.x) ** 2 + (y - rect.y) ** 2)

        rect.x += percentage * (x - rect.x) / hip
        rect.y += percentage * (y - rect.y) / hip

        return False

    @staticmethod
    def rotate(surface, angle):
        return pygame.transform.rotate(surface, angle)

    def draw(self):
        for i in self.actors:
            if i.type == "image_file":
                self.screen.blit(i.image, i.rect)
            else:
                pygame.draw.rect(self.screen, i.image, i.rect)

    def write_texts(self):
        for i in self.texts:
            self.screen.blit(
                self.font.render(i.text, True, i.color),
                self.calculate_text_position(i.text, i.x, i.y),
            )

    def calculate_text_position(self, text, x, y):
        text_width, text_height = self.font.size(text)
        return x - text_width / 2, y - text_height / 2

    def get_text_size(self, text):
        return self.font.size(text)

    def update_screen(self):
        self.clock.tick(FPS)
        pygame.display.update()

    def play(self):
        while self.is_running:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if (
                            event.key == pygame.K_ESCAPE
                            or event.key == pygame.K_SPACE
                            or event.key == pygame.K_RETURN
                    ):
                        self.is_running = False

            self.screen.fill("black")
            self.background('images/background_battle.png')
            self.draw()
            self.write_texts()
            self.update_screen()

    def update(self):
        raise NotImplementedError("You need to implement this method in your cutscene class")


class BattleCutscene(Cutscene):
    def __init__(self, player: pygame.sprite.Sprite, player_img: str, enemy_img: str, enemy_hp: int) -> None:
        super().__init__()
        self.player_sprite = player

        self.player = self.create_actor(player_img, 350, 550, 100, 100, player.hp)
        self.enemy = self.create_actor(enemy_img, 900, 220, 100, 100, enemy_hp)
        self.turn = 0
        self.moves = moves

        self.create_text("Choose your move:", 150, 100, 'white')
        self.create_text("1. Weak", 150, 150, 'white')
        self.create_text("2. Medium", 150, 200, 'white')
        self.create_text("3. Strong", 150, 250, 'white')
        self.create_text("4. Heal", 150, 300, 'white')
        self.action_text: str = ""
        self.timer = 1 * FPS

    @staticmethod
    def get_player_input():
        keys = pygame.key.get_pressed()

        if keys[pygame.K_1]:
            return 'weak'
        elif keys[pygame.K_2]:
            return 'medium'
        elif keys[pygame.K_3]:
            return 'strong'
        elif keys[pygame.K_4]:
            return 'heal'
        else:
            return None

    def player_attack(self, move=None):
        if move is None:
            return

        chance = random.random()

        if chance < self.moves[move]['accuracy']:
            if self.moves[move]['damage'] < 0:
                self.player.hp -= self.moves[move]['damage']
                self.update_action_text(f'You used {self.moves[move]["name"]} for {-self.moves[move]["damage"]} hp!')
            else:
                self.enemy.hp -= self.moves[move]['damage']
                self.update_action_text(f'You used {self.moves[move]["name"]} for {self.moves[move]["damage"]} damage!')
        else:
            self.update_action_text(f'Your attack {self.moves[move]["name"]} missed!')

        self.next_turn()

    def update(self):

        move = self.get_player_input()

        if self.turn % 2 == 0:
            self.player_attack(move)
        else:
            time.sleep(1.5)
            self.enemy_attack()

        if self.player.hp <= 0:
            self.is_running = False
            print('You lose!')
        elif self.enemy.hp <= 0:
            self.is_running = False
            print('You win!')

    def update_action_text(self, text: str):
        # remove old text
        self.texts = [text for text in self.texts if text.text != self.action_text]
        self.action_text = text
        self.draw_action_text()

    def draw_action_text(self):
        # if text contains enemy, draw red
        if 'Enemy' in self.action_text:
            self.create_text(self.action_text, 600, 400, 'red')
        else:
            self.create_text(self.action_text, 200, 400, 'white')

    def draw(self):
        for i in self.actors:
            if i.type == "image_file":
                self.screen.blit(i.image, i.rect)
            else:
                pygame.draw.rect(self.screen, i.image, i.rect)

        self.draw_hp_bars()  # Add this line to draw the HP bars

    def draw_hp_bars(self):
        player_hp_ratio = self.player.hp / self.player.max_hp
        enemy_hp_ratio = self.enemy.hp / self.enemy.max_hp

        player_bar_width = int(player_hp_ratio * 200)
        enemy_bar_width = int(enemy_hp_ratio * 200)

        # Draw player's HP bar
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.player.rect.x - 40, self.player.rect.y - 40, player_bar_width, 20))

        # Draw enemy's HP bar
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.enemy.rect.x - 40, self.enemy.rect.y - 40, enemy_bar_width, 20))

    def enemy_attack(self):
        move = self.enemy.attack()  # returns a random move from the moves dict

        # random float between 0 and 1
        chance = random.random()

        if chance < move['accuracy']:
            # hit
            if move['damage'] < 0:
                # heal
                self.enemy.hp -= move['damage']
                self.update_action_text(f'Enemy used {move["name"]} healing for {-move["damage"]} health!')
            else:
                self.player.hp -= move['damage']
                self.update_action_text(f'Enemy used {move["name"]} for {move["damage"]} damage!')
        else:
            # miss
            self.update_action_text(f'Enemy attack {move["name"]} missed!')

        self.next_turn()

    def next_turn(self):
        print(f'Player HP: {self.player.hp}')
        print(f'Enemy HP: {self.enemy.hp}')
        self.turn += 1
