from random import random
import time
from utils import import_folder

from cutscene import Cutscene
import pygame
from settings import moves, TILESIZE
from textbox import Textbox


class BattleCutscene(Cutscene):
    def __init__(
        self,
        player: pygame.sprite.Sprite,
        player_img: str,
        enemy_img: str,
        enemy: pygame.sprite.Sprite,
    ) -> None:
        super().__init__()
        self.player_sprite = player

        self.player = self.create_actor(
            player_img, 350, 500, 100, 100, player.hp, player.name
        )
        self.enemy = self.create_actor(
            enemy_img, 820, 285, 100, 100, enemy.hp, enemy.name
        )
        self.turn = 0

        self.moves_text_initial()

        self.winner = None
        self.text_box = Textbox()
        self.action_text = ""

    def moves_text_initial(self):
        self.create_text("Choose your move:", 1000, 450, "white")
        self.create_text("1. Weak", 1000, 500, "white")
        self.create_text("2. Medium", 1000, 550, "white")
        self.create_text("3. Strong", 1000, 600, "white")
        self.create_text("4. Heal", 1000, 650, "white")

    @staticmethod
    def get_player_input():
        keys = pygame.key.get_pressed()

        if keys[pygame.K_1]:
            return "weak"
        elif keys[pygame.K_2]:
            return "medium"
        elif keys[pygame.K_3]:
            return "strong"
        elif keys[pygame.K_4]:
            return "heal"
        else:
            return None

    def background(self, image: str):
        new_img = pygame.image.load(image).convert_alpha()
        new_img = pygame.transform.scale(new_img, (WIDTH, HEIGHT))
        self.screen.blit(new_img, (0, 0))
        
    def attack(
        self,
        move: str ,
        attacker: pygame.sprite.Sprite,
        defender: pygame.sprite.Sprite,
    ) -> str:
        accuracy = random()

        move = attacker.moves[
            move
        ]  # get the move from the attacker, so in the future we can have different moves for different enemies and players

        is_heal = move["damage"] < 0

        if accuracy < move["accuracy"]:
            # hit
            if is_heal:
                # heal
                attacker.hp -= move["damage"]

                self.animate_move_and_stop_text(
                    "heal", (attacker.rect.centerx, attacker.rect.centery), 50
                )
                return f'{attacker.name} used {move["name"]} healing for {-move["damage"]} health!'
            else:
                defender.hp -= move["damage"]
                self.animate_move_and_stop_text(
                    move["name"], (defender.rect.centerx, defender.rect.centery), 50
                )
                return (
                    f'{attacker.name} used {move["name"]} for {move["damage"]} damage!'
                )
        else:
            # miss
            return f'{attacker.name} attack {move["name"]} missed!'

    @staticmethod
    def hp_color_from_ratio(ratio: float):
        if ratio > 0.6:
            return "green"
        elif ratio > 0.3:
            return "yellow"
        else:
            return "red"

    def animate_move_and_stop_text(
        self,
        move: str,
        pos: tuple[int, int],
        delay: int,
        width=2 * TILESIZE,
        height=2 * TILESIZE,
    ):
        sprites = import_folder(
            f"graphics/particles/{move.lower()}"
        )  # lowercase the move name, only works on windows

        pygame.mixer.music.load(f"sounds/{move.lower()}.mp3")
        pygame.mixer.music.play()

        time.sleep(0.05)

        for sprite in sprites:
            sprite = pygame.transform.scale(sprite, (width, height))

            self.screen.blit(sprite, (pos[0] - width / 2, pos[1] - height / 2))
            pygame.display.update()
            pygame.time.delay(delay)
            self.full_update()

    def make_a_move(self, move: str):
        is_player_turn = self.turn % 2 == 0

        if is_player_turn:
            if move is None:  # return early while not moving
                return

            self.action_text = self.attack(move, self.player, self.enemy)
            self.next_turn()

        else:
            if self.text_box.active:
                return

            move = self.enemy.attack()

            self.action_text = self.attack(move, self.enemy, self.player)
            self.next_turn()

    def update(self):
        move = self.get_player_input()

        self.make_a_move(move)

        if self.player.hp <= 0:
            self.is_running = False
            self.winner = "enemy"
            print("You lose!")

        elif self.enemy.hp <= 0:
            self.is_running = False
            self.winner = "player"
            print("You win!")

    def draw(self):
        for i in self.actors:
            if i.type == "image_file":
                self.screen.blit(i.image, i.rect)
            else:
                pygame.draw.rect(self.screen, i.image, i.rect)

        self.text_box.draw()
        self.text_box.update()

        self.draw_hp_hud()  # Add this line to draw the HP bars

    def draw_hp_hud(self):
        player_hp_ratio = self.player.hp / self.player.max_hp
        enemy_hp_ratio = self.enemy.hp / self.enemy.max_hp

        # Draw player's HP bar
        self.draw_hp_bars(player_hp_ratio, self.player.rect.x, self.player.rect.y)

        # Create text for player's HP
        player_hp = self.font.render(
            f"{self.player.hp}/{self.player.max_hp}", True, "white"
        )

        # Draw enemy's HP bar
        self.draw_hp_bars(enemy_hp_ratio, self.enemy.rect.x, self.enemy.rect.y)

        # Create text for enemy's HP
        enemy_hp = self.font.render(
            f"{self.enemy.hp}/{self.enemy.max_hp}", True, "white"
        )

        # Blit the text onto the screen
        self.screen.blit(
            player_hp, (self.player.rect.x - 40, self.player.rect.y - 70)
        )  # Player HP text
        self.screen.blit(
            enemy_hp, (self.enemy.rect.x - 40, self.enemy.rect.y - 70)
        )  # Enemy HP text

    def draw_hp_bars(self, ratio: float, x: int, y: int):
        bar_width = int(ratio * 100)

        pygame.draw.rect(
            self.screen,
            self.hp_color_from_ratio(ratio),
            pygame.Rect(x - 40, y - 40, bar_width * 2, 20),
        )

    def next_turn(self):
        print(f"Player HP: {self.player.hp}")
        print(f"Enemy HP: {self.enemy.hp}")

        self.turn += 1  # why a function for this? IDK but it's here now
        self.text_box.start_text(messages=[self.action_text])
        self.text_box.char_idx = 0
