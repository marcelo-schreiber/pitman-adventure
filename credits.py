import pygame
from cutscene import Cutscene
import sys
from settings import *


class Credits(Cutscene):
    def __init__(self):
        super().__init__()
        texts = [
            "Made by Binder & Marcelo",
            "Programming: Binder & Marcelo",
            "The Amazing Text box System: Binder",
            "The ugly part of the code: Marcelo",
            "Art: Marcos Sketches & Catharina Sketches",
            "Npcs: Catharina Sketches",
            "Icons: Marcos Sketches",
            "Daniel Npc: Tango lanches",
            "Made with 1276 lines of code",
            "21y bday boy: Arthur pitman",
        ]

        for i in range(len(texts)):
            self.create_text(texts[i], WIDTH / 2, HEIGHT + i * (HEIGHT) / 2, "white")
        self.create_text(
            "THE END", WIDTH / 2, HEIGHT + (len(texts) + 2) * (HEIGHT) / 2, "white"
        )

        self.y = 0

    def update(self):
        for text in self.texts:
            text.y -= 2

        self.y += 1

        if self.y > 2600:
            self.is_running = False
            pygame.quit()
            sys.exit()
