import time
from tile import Tile
from textbox import Textbox
import pygame

class Item(Tile):
    def __init__(self, pos, groups, sprite_type, surface, name, apply_effect):
        super().__init__(pos, groups, sprite_type, surface)
        self.name = name
        self.apply_effect = apply_effect
        self.textbox = Textbox()
        self.hitbox = self.rect.inflate_ip(-26, -26)

        self.sound = pygame.mixer.Sound("sounds/item.mp3")

    def show_text(self):
        self.sound.play()
        time.sleep(0.1)
        self.textbox.start_text(
            messages=[f"You found a {self.name}!"], func=self.apply_effect
        )

