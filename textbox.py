# Introdução:
# A classe textbox é um Singleton, ou seja, qualquer instância do objeto será
# uma referência a um mesmo objeto.
#
# Como Usar:
# Instancie a classe Textbox e chame start_text com uma lista de strings.
# Isso irá pausar o jogo e começar a mostrar o texto.
# Quando o texto acabar, o jogo irá despausar.
from pathlib import Path
import pygame
from settings import WIDTH, HEIGHT

example_message = [
    "Hello!",
    "This is an example text message.",
    "This Singleton helps making textboxes!",
]


class TSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Textbox(metaclass=TSingletonMeta):
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font("font/PressStart2P-Regular.ttf", 20)
        self.text_background = pygame.image.load(
            "images/background-text.png"
        ).convert_alpha()
        self.text_background = pygame.transform.scale(
            self.text_background, (WIDTH, HEIGHT / 5)
        )

        self.iterator = 0
        self.messages = []
        self.current_text = ""

        self.active = False
        self.icon = ""

        self.pressed = False

        self.character_speed = 0.4
        self.char_idx: float = 0

        self.handle_talking_end = lambda: None  # function that returns nothing
        self.sound = pygame.mixer.Sound("sounds/text.mp3")
        self.sound.set_volume(0.3)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if self.pressed:
                return
            if self.char_idx < len(self.current_text) - 1:
                self.char_idx = len(self.current_text) - 1
                self.pressed = True
                return
            self.iterator += 1
            self.sound.play()
            if self.iterator == len(self.messages):
                self.active = False
                if self.handle_talking_end is not None:
                    self.handle_talking_end()
            else:
                self.current_text = self.messages[self.iterator]
                self.char_idx = 0
            self.pressed = True
        else:
            self.pressed = False

    def start_text(self, messages: [str], func=lambda: None, icon=""):
        self.active = True
        self.iterator = 0
        self.messages = messages
        self.handle_talking_end = func

        self.current_text = self.messages[self.iterator]
        self.char_idx = 0
        self.icon = icon

    def after_fire(self):
        self.handle_talking_end()

    def draw(self):
        if not self.active:
            return

        text_to_draw = self.current_text[: int(self.char_idx)]
        text_surface = self.font.render(text_to_draw, True, "Black")
        self.display_surface.blit(self.text_background, (0, 0))

        # update character index
        self.char_idx = min(
            self.char_idx + self.character_speed, len(self.current_text)
        )


        is_icon_a_file = Path(self.icon).is_file()

        if is_icon_a_file:
            name = self.icon.split("/")[-1].split(".")[0]
            talking_names = self.current_text.split(":")
            talking_name = talking_names[0].lower()
            if name != talking_name and len(talking_names) == 2:
                self.icon = f"graphics/icons/{talking_name}_icon.png" # dumb way to do it

            icon = pygame.image.load(self.icon).convert_alpha()
            icon = pygame.transform.scale(icon, (144, 144))
            self.display_surface.blit(icon, (0, 0))
            self.display_surface.blit(text_surface, (165, 60))
        else:
            self.display_surface.blit(text_surface, (100, 60))

    def update(self):
        if self.active:
            self.draw()
            self.input()
