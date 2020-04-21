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
            "credits": arcade.Sprite(
                "./assets/Credits.png",
                scale=0.2,
                center_x=80,
                center_y=30
            ),

        }
        self.spritelist.extend(self.spritedict.values())

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.spritelist.draw()

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        print((x, y))
        if self.spritedict["exit"].collides_with_point((x, y)) is True:
            arcade.close_window()
        elif self.spritedict["credits"].collides_with_point((x, y)) is True:
            self.display.change_scenes("loading", startup=False)
#        elif self.spritedict["options"].collides_with_point((x, y)) is True:
#            self.display.change_scenes("options")
        elif self.spritedict["playClient"].collides_with_point((x, y)) is True:
            self.display.change_scenes("playClient", startup=False)
        elif self.spritedict["playHost"].collides_with_point((x, y)) is True:
            self.display.change_scenes("playServer", startup=False)
