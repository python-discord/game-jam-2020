import arcade
from .base import Base
import json

class Help(Base):
    def __init__(self, display):
        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.timeAlive = 0
        self.sprite_setup()
        self.display = display

    def sprite_setup(self):
        self.spritedict = {
            "exit": arcade.Sprite(
                "./assets/Exit.png",
                scale=0.25,
                center_x=640,
                center_y=120
            ),
            "title": arcade.Sprite(
                "./assets/help.png",
                scale=0.5,
                center_x=640,
                center_y=580
            ),
        }
        self.spritelist.extend(self.spritedict.values())
    def load_text(self):
        pass

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.spritelist.draw()
        arcade.draw_text("Simple line of text in 12 point", 50, 60, arcade.color.BLACK, 12)

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        print((x, y))
        if self.spritedict["exit"].collides_with_point((x, y)) is True:
            self.display.change_scenes("options")
        if self.spritedict["title"].collides_with_point((x, y)) is True:
            arcade.gui.TextBox("Hello", 50, 100)










