import arcade


class Options:
    def __init__(self, display):
        self.display = display
        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.timeAlive = 0

        self.sprite_setup()

    def sprite_setup(self):
        self.spritedict = {
            "exit": arcade.Sprite(
                "./assets/ESC.png",
                scale=0.25,
                center_x=160,
                center_y=620
            ),
            "title": arcade.Sprite(
                "./assets/Options.png",
                scale=0.25,
                center_x=160,
                center_y=620
            ),
            "ESC": arcade.Sprite(
                "./assets/ESC.png",
                scale=0.25,
                center_x= 560,
                center_y=620
            ),
        }
        self.spritelist.extend(self.spritedict.values())

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.spritelist.draw()