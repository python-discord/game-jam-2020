import arcade
from .util import make_colour_valid
from .base import Base


class LoadingScreen(Base):
    def __init__(self, display):
        self.display = display

        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.sceneTime = 0
        self.startup = True

        self.sprite_setup()

    def reset(self, startup=True):
        self.sceneTime = 0
        self.startup = startup

    def sprite_setup(self):
        self.spritelist.extend([
            arcade.Sprite(
                "./assets/title.png",
                scale=0.5,
                center_x=640,
                center_y=360
            ),
            arcade.Sprite(
                "./assets/Adith.png",
                scale=0.15,
                center_x=640,
                center_y=300
            ),
            arcade.Sprite(
                "./assets/TheLordOfTartarus.png",
                scale=0.15,
                center_x=640,
                center_y=260
            ),
            arcade.Sprite(
                "./assets/xedre.png",
                scale=0.15,
                center_x=640,
                center_y=220
            )
        ])

    def update(self, delta_time: float) -> None:
        self.sceneTime += delta_time

        if self.startup is True:
            fade = make_colour_valid(255 - (self.sceneTime - 2) * 100)

            for x in self.spritelist:
                x.alpha = fade

        if self.sceneTime < 2:
            fade_in = make_colour_valid((self.sceneTime - 0.5) * 200)
            for x in self.spritelist[1:]:
                x.alpha = fade_in

        if self.sceneTime > 5 and self.startup is True:
            self.display.change_scenes("lobby")

    def draw(self):
        self.spritelist.draw()

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.display.change_scenes("lobby")
