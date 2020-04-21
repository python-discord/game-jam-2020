import arcade
from .scenes import *
from typing import Union, Optional


class Display(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Three of a king")
        self.title = arcade.sprite_list
        arcade.set_background_color((255, 255, 255))
        self.scene = "loading"
        self.scenes = dict()

    def setup(self):
        self.scenes["loading"] = LoadingScreen(self)
        self.scenes["lobby"] = Lobby(self)
        self.scenes["mainMenu"] = MainMenu(self)
        self.scenes["options"] = Options(self)
        self.scenes["playClient"] = PlayAsClient(self)
        self.scenes["playServer"] = PlayAsServer(self)

    def change_scenes(self, scene: str, *args, **kwargs):
        print(self.scene)
        self.scenes[scene].reset(*args, **kwargs)
        self.scene = scene
        print(self.scene)

    def on_draw(self):

        arcade.start_render()
        self.scenes[self.scene].draw()

    def on_update(self, delta_time: float):
        self.scenes[self.scene].update(delta_time)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.scenes[self.scene].mouse_release(x, y, button, modifiers)

    def on_key_press(self, key, modifiers):
        self.scenes[self.scene].key_press(key, modifiers)


def main():
    display1 = Display()
    display1.setup()
    arcade.run()
