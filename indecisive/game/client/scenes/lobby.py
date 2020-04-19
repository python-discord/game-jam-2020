import arcade
from .base import Base
import string
from .util import arcade_int_to_string


class Lobby(Base):
    def __init__(self, display):
        self.display = display

        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.sceneTime = 0
        self.name = ""
        self.focus = None

        self.sprite_setup()

    def sprite_setup(self):
        self.spritedict = {
            "back": arcade.Sprite(
                "./assets/simple_button.png",
                scale=0.25,
                center_x=160,
                center_y=687.5
            ),
            "name": arcade.Sprite(
                "./assets/simple_button.png",
                scale=0.25,
                center_x=160,
                center_y=622.5
            )
        }
        self.spritelist.extend(self.spritedict.values())

    def update(self, delta_time: float) -> None:
        self.sceneTime += delta_time

    def draw(self):
        self.spritelist.draw()
        arcade.draw_text(self.name, 15, 600, color=(255, 255, 255), font_size=35)

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        print((x, y))
        if self.spritedict["back"].collides_with_point((x, y)) is True:
            self.display.change_scenes("loading", startup=False)
        elif self.spritedict["name"].collides_with_point((x, y)) is True:
            self.focus = "name"

    def key_press(self, key, modifiers):
        if len(self.name) < 8:
            self.name += arcade_int_to_string(key, modifiers)
        else:
            self.name = self.name[1:] + arcade_int_to_string(key, modifiers)
