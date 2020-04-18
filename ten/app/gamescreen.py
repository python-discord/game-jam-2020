from arcade import *
import arcade


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
