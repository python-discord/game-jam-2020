import arcade
from .util import make_colour_valid


class LoadingScreen:
    def __init__(self):
        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.sceneTime = 0

        self.sprite_setup()

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
        fade = make_colour_valid(255 - (self.sceneTime - 2) * 100)

        for x in self.spritelist:
            x.alpha = fade

        if self.sceneTime < 2:
            fade_in = make_colour_valid((self.sceneTime - 0.5) * 200)
            for x in self.spritelist[1:]:
                x.alpha = fade_in

    def draw(self):
        self.spritelist.draw()
