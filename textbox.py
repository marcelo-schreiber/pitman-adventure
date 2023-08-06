# Introdução:
# A classe textbox é um Singleton, ou seja, qualquer instância do objeto será
# uma referência a um mesmo objeto.
#
# Como Usar:
# Instancie a classe Textbox e chame start_text com uma lista de strings.
# Isso irá pausar o jogo e começar a mostrar o texto.
# Quando o texto acabar, o jogo irá despausar.

import pygame

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
        self.font = pygame.font.Font("font/PressStart2P-Regular.ttf", 22)

        self.iterator = 0
        self.messages = []
        self.current_text = ""

        self.active = False

        self.pressed = False

        self.character_speed = 0.5
        self.char_idx: float = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if self.pressed:
                return
            self.iterator += 1
            if self.iterator == len(self.messages):
                self.active = False
            else:
                self.current_text = self.messages[self.iterator]
                self.char_idx = 0
            self.pressed = True
        else:
            self.pressed = False

    def start_text(self, messages: [str]):
        self.active = True
        self.iterator = 0
        self.messages = messages

        self.current_text = self.messages[self.iterator]

    def draw(self):
        if not self.active:
            return

        text_to_draw = self.current_text[: int(self.char_idx)]
        text_surface = self.font.render(text_to_draw, True, "White")
        self.display_surface.blit(text_surface, (10, 10))

        # update character index
        self.char_idx = min(
            self.char_idx + self.character_speed, len(self.current_text)
        )

    def update(self):
        if self.active:
            self.draw()
            self.input()
