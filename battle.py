from random import random

from cutscene import Cutscene
import pygame
import time
from settings import moves, FPS, WIDTH


class BattleCutscene(Cutscene):
    def __init__(self, player: pygame.sprite.Sprite, player_img: str, enemy_img: str, enemy_hp: int) -> None:
        super().__init__()
        self.player_sprite = player

        self.player = self.create_actor(player_img, 350, 500, 100, 100, player.hp)
        self.enemy = self.create_actor(enemy_img, 820, 285, 100, 100, enemy_hp)
        self.turn = 0
        self.moves = moves

        self.create_text("Choose your move:", 1000, 450, 'white')
        self.create_text("1. Weak", 1000, 500, 'white')
        self.create_text("2. Medium", 1000, 550, 'white')
        self.create_text("3. Strong", 1000, 600, 'white')
        self.create_text("4. Heal", 1000, 650, 'white')
        self.action_text: str = ""
        self.timer = 1 * FPS

        self.displaying_specific_text = False
        self.specific_text = ""
        self.winner = None

        self.background_text = self.create_actor('images/background-text.png', -1, -1, WIDTH, 180)

        self.curr_actor_talking = None

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

        chance = random()
        is_heal = self.moves[move]['damage'] < 0

        if chance < self.moves[move]['accuracy']:
            if is_heal:
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
            self.winner = 'enemy'
            print('You lose!')

        elif self.enemy.hp <= 0:
            self.is_running = False
            self.winner = 'player'
            print('You win!')

    def update_action_text(self, text: str):
        # remove old text
        self.texts = [text for text in self.texts if text.text != self.action_text]
        self.action_text = text
        self.draw_action_text()

    def draw_action_text(self):
        action_text_x = self.background_text.rect.x + 200
        action_text_y = self.background_text.rect.y + self.background_text.rect.height // 2
        # draw white rectangle around text

        # draw image

        if 'Enemy' in self.action_text:
            self.remove_curr_actor_talking()

            self.curr_actor_talking = self.create_actor('images/leo.png', 15, 15, 150, 150)
            self.display_specific_text_slowly(self.action_text, action_text_x, action_text_y, 'red', 20)
        else:
            self.remove_curr_actor_talking()

            self.curr_actor_talking = self.create_actor('images/danites1.png', 15, 15, 150, 150)
            self.display_specific_text_slowly(self.action_text, action_text_x, action_text_y, 'black', 20)

    def remove_curr_actor_talking(self):
        for actor in self.actors:
            if actor == self.curr_actor_talking:
                self.actors.remove(actor)

    def draw(self):
        for i in self.actors:
            if i.type == "image_file":
                self.screen.blit(i.image, i.rect)
            else:
                pygame.draw.rect(self.screen, i.image, i.rect)

        self.draw_hp_hud()  # Add this line to draw the HP bars

    @staticmethod
    def hp_color_from_ratio(ratio: float):
        if ratio > 0.6:
            return 'green'
        elif ratio > 0.3:
            return 'yellow'
        else:
            return 'red'

    def draw_hp_hud(self):
        player_hp_ratio = self.player.hp / self.player.max_hp
        enemy_hp_ratio = self.enemy.hp / self.enemy.max_hp

        # Draw player's HP bar
        self.draw_hp_bars(player_hp_ratio, self.player.rect.x, self.player.rect.y)

        # Create text for player's HP
        player_hp = self.font.render(f'{self.player.hp}/{self.player.max_hp}', True, 'white')

        # Draw enemy's HP bar
        self.draw_hp_bars(enemy_hp_ratio, self.enemy.rect.x, self.enemy.rect.y)

        # Create text for enemy's HP
        enemy_hp = self.font.render(f'{self.enemy.hp}/{self.enemy.max_hp}', True, 'white')

        # Blit the text onto the screen
        self.screen.blit(player_hp, (self.player.rect.x - 40, self.player.rect.y - 70))  # Player HP text
        self.screen.blit(enemy_hp, (self.enemy.rect.x - 40, self.enemy.rect.y - 70))  # Enemy HP text

    def draw_hp_bars(self, ratio: float, x: int, y: int):
        bar_width = int(ratio * 100)

        pygame.draw.rect(self.screen, self.hp_color_from_ratio(ratio),
                         pygame.Rect(x - 40, y - 40, bar_width * 2, 20))

    def enemy_attack(self):
        move = self.enemy.attack()  # returns a random move from the moves dict

        # random float between 0 and 1
        chance = random()

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
        self.turn += 1  # why a function for this? IDK but it's here now
