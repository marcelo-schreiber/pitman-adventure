import pygame
import math

from settings import *
from enemy import Enemy


class Cutscene:
    def __init__(self):
        self.displaying_specific_text = None
        self.specific_text = None
        self.is_running = True
        self.screen = pygame.display.get_surface()
        self.actors = []
        self.texts = []
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font/PressStart2P-Regular.ttf", 22)

    class Actor(Enemy):
        def __init__(
            self,
            name: str,
            x: int,
            y: int,
            width: int,
            height: int,
            enemy_hp: int,
            character_name: str,
        ):
            super().__init__(enemy_hp, character_name)
            try:
                self.image = pygame.image.load(name).convert_alpha()
                self.image = pygame.transform.scale(self.image, (width, height))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.type = "image_file"
            except:
                self.image = name
                self.rect = pygame.Rect(x, y, width, height)
                self.type = "solid_color"

    class Text:
        def __init__(self, string: str, x: int, y: int, color: str, alpha=255):
            self.text = string
            self.x = x
            self.alpha = alpha
            self.y = y
            self.color = color
        

    def create_actor(
        self,
        name: str,
        x: int,
        y: int,
        width: int,
        height: int,
        enemy_hp=100,
        character_name: str = "enemy",
    ):
        actor = self.Actor(name, x, y, width, height, enemy_hp, character_name)
        self.actors.append(actor)
        return actor

    def full_update(self):
        self.screen.fill("black")
        self.background("images/background_battle_image.jpg")
        self.draw()
        self.write_texts()
        self.update_screen()

    def display_specific_text_slowly(
        self, text: str, x: int, y: int, color: str, speed=50
    ):
        text_obj = self.create_text("", x, y, color)
        self.specific_text = text
        self.displaying_specific_text = True

        for char in text:
            text_obj.text += char
            text_obj.x += self.get_text_size(char)[0] // 2
            self.full_update()
            pygame.time.delay(speed)
        self.displaying_specific_text = False

    def write_texts(self):
        for i in self.texts:
            if self.displaying_specific_text and i.text == self.specific_text:
                continue  # Skip drawing the specific text if displaying_specific_text is True
            
            text_surf = self.font.render(i.text, True, i.color)
            text_surf.set_alpha(i.alpha)

            self.screen.blit(
                text_surf,
                self.calculate_text_position(i.text, i.x, i.y),
            )
    
    def create_text(self, string, x: int, y: int, color: str):
        text = self.Text(string, x, y, color)
        self.texts.append(text)
        return text

    def background(self, image: str):
        pass

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
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.is_running = False

            self.full_update()

    def update(self):
        raise NotImplementedError(
            "You need to implement this method in your cutscene class"
        )
