import arcade
from .base import Base

class Options(Base):
    def __init__(self, display):
        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.timeAlive = 0
        self.display = display
        self.sprite_setup()

    def sprite_setup(self):
        self.spritedict = {
            "exit": arcade.Sprite(
                "./assets/Exit.png",
                scale=0.25,
                center_x=640,
                center_y=120
            ),

            "title": arcade.Sprite(
                "./assets/Options.png",
                scale=0.5,
                center_x=770,
                center_y=580
            ),
            "music": arcade.Sprite(
                "./assets/music.png",
                scale=0.5,
                center_x=650,
                center_y= 400
            ),

        }
        self.spritelist.extend(self.spritedict.values())

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.spritelist.draw()
        self.display.button_list.draw()

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        print((x, y))
        if self.spritedict["exit"].collides_with_point((x, y)) is True:
            self.display.change_scenes("mainMenu")


        if self.spritedict["music"].collide_with_point((x, y)) is True:
            pass

