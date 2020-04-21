import arcade
from .base import Base

class MainMenu(Base):
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
            "options": arcade.Sprite(
                "./assets/Mainmenu_options.png",
                scale=0.25,
                center_x=640,
                center_y=220
            ),
            "title": arcade.Sprite(
                "./assets/PlaceholderTitle.png",
                scale=0.5,
                center_x=640,
                center_y=580
            ),
            "playClient": arcade.Sprite(
                "./assets/PlayAsClient.png",
                scale=0.25,
                center_x=640,
                center_y=320
            ),
            "playHost": arcade.Sprite(
                "./assets/PlayAsHost.png",
                scale=0.25,
                center_x=640,
                center_y=420
            ),

        }
        self.spritelist.extend(self.spritedict.values())

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.spritelist.draw()

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass