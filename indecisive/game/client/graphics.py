import arcade
from .scenes import *


class Display(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Three of a king")
        self.title = arcade.sprite_list
        arcade.set_background_color((255, 255, 255))
        self.scene = "loading"
        self.scenes = dict()

    def setup(self):
        self.scenes["loading"] = LoadingScreen()
        self.scenes["lobby"] = Lobby

    def on_draw(self):

        arcade.start_render()
        self.scenes[self.scene].draw()

    def on_update(self, delta_time: float):
        self.scenes[self.scene].update(delta_time)


def main():
    display1 = Display()
    display1.setup()
    arcade.run()
