from tile import Tile
from textbox import Textbox


class Item(Tile):
    def __init__(self, pos, groups, sprite_type, surface, name, apply_effect):
        super().__init__(pos, groups, sprite_type, surface)
        self.name = name
        self.apply_effect = apply_effect
        self.textbox = Textbox()
        self.hitbox = self.rect.inflate_ip(-26, -26)

    def show_text(self):
        self.textbox.start_text(
            messages=[f"You found a {self.name}!"], func=self.apply_effect
        )
