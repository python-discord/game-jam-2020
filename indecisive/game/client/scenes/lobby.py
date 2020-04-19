import arcade


class Lobby:
    def __init__(self):
        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.timeAlive = 0

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
                center_y=635
            )
        }
        self.spritelist.extend(self.spritedict.values())

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.spritelist.draw()