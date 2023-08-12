from cutscene import Cutscene
import pygame
from settings import *
import sys


class WinCutscene(Cutscene):
    def __init__(self):
        super().__init__()
        self.create_text("You found Eevee !!", 1055, 300, "white")
        self.create_text("Thanks for playing", 1055, 350, "white")
        self.song = pygame.mixer.Sound("sounds/final.mp3")
        self.song.set_volume(0.3)
        self.song.play(-1)

    def background(self, image: str):
        new_img = pygame.image.load("images/final.png").convert_alpha()
        new_img = pygame.transform.scale(new_img, (WIDTH, WIDTH))
        self.screen.blit(new_img, (0, 0))

    def update(self):
        self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.is_running = False
