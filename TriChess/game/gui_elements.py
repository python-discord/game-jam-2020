import arcade
from arcade.gui import TextButton
from arcade import Theme
import os
from os.path import join, dirname, realpath
from TriChess.game.trigrid import TriGrid

data_dir = join(dirname(realpath(__file__)).rsplit(os.sep, 1)[0], 'data')
button_click = arcade.Sound(os.path.join(data_dir, "button_click.mp3"))


class PlayHex2Btn(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40):
        theme = Theme()
        clicked = join(data_dir, '2player_normal.png')
        normal = join(data_dir, '2player_pressed.png')
        theme.add_button_textures(normal, normal, clicked, clicked)
        super().__init__(x, y, width, height, "", theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            button_click.play()
            self.game.game_type = "hex2"
            self.game.trigrid = TriGrid(self.game.width,  self.game.height, self.game.game_type)
            self.pressed = False
            self.game.on_draw()


class PlayTri3Btn(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40):
        theme = Theme()
        clicked = join(data_dir, '3player_normal.png')
        normal = join(data_dir, '3player_pressed.png')
        theme.add_button_textures(normal, normal, clicked, clicked)
        super().__init__(x, y, width, height, '', theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            button_click.play()
            self.game.game_type = "tri3"
            self.game.trigrid = TriGrid(self.game.width,  self.game.height, self.game.game_type)
            self.pressed = False
            self.game.on_draw()


class SkipTurnBtn(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40):
        theme = Theme()
        clicked = join(data_dir, 'skip_normal.png')
        normal = join(data_dir, 'skip_pressed.png')
        theme.add_button_textures(normal, normal, clicked, clicked)
        super().__init__(x, y, width, height, '', theme=theme)
        self.game = game
        self.active = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            button_click.play()
            self.game.trigrid.clear_selection()
            self.game.trigrid.next_player()
            self.pressed = False
