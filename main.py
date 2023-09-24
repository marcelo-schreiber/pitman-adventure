import pygame
import sys

from level import Level
from settings import *


class Game:
    def __init__(self):
        pygame.mixer.music.set_volume(0.7)

        pygame.display.set_caption("Pitman adventure: finding eevee")
        pygame.display.set_icon(pygame.image.load("images/down.png"))

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((80, 167, 232))
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
