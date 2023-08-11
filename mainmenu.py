from cutscene import Cutscene
import pygame


class MainMenu(Cutscene):
    def __init__(self):
        super().__init__()
        self.background("images/danites2.png")
        self.create_text("Press any key to start", 1000, 650, "white")

    def update(self):
        self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.is_running = False
