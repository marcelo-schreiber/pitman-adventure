from settings import *
from cutscene import Cutscene
import pygame
import sys


class MainMenu(Cutscene):
    def __init__(self):
        super().__init__()
        self.press_key_to_start = self.create_text(
            "Press any key to start", 1000, 650, "white"
        )

        self.title = self.create_text(
            "Pitman Adventure: Finding Eevee", WIDTH // 2, HEIGHT // 2, "white"
        )
        self.title.alpha = 0

        self.arthur = self.create_actor(
            "images/eevee.png", WIDTH // 2 - 25, HEIGHT - 200, 200, 200
        )

        self.song = pygame.mixer.Sound("sounds/mainmenu.mp3")
        self.song.play(-1)

    def background(self, image: str):
        new_img = pygame.image.load("images/mainmenu.jpg").convert_alpha()
        new_img = pygame.transform.scale(new_img, (WIDTH, HEIGHT))
        self.screen.blit(new_img, (0, 0))

    def update(self):
        if self.title.alpha < 255:
            self.title.alpha += 5

        self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.is_running = False
                self.song.stop()
