import arcade

from submission.gameConstants import *
from submission.game import GameView


class MenuView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()

        self.x = None
        self.y = None
        self.image_list = None
        self.keyText = None
        self.text_ur = None
        self.frames = None

    def on_show(self):
        path = PATH['img'] / 'icons' / 'titleScreen'
        self.x, self.y = self.window.get_size()

        self.image_list = arcade.SpriteList(is_static=True)

        src = path / 'beanWhite.png'
        imageSprite = arcade.Sprite(src, center_x=80, center_y=450)
        self.image_list.append(imageSprite)

        src = path / 'pythonArcadeWhite.png'
        imageSprite = arcade.Sprite(src, center_x=950, center_y=35)
        self.image_list.append(imageSprite)

        src = path / 'title.png'
        imageSprite = arcade.Sprite(src, center_x=self.x / 2, center_y=self.y / 2 + 60)
        self.image_list.append(imageSprite)

        self.keyText = 'press any key to continue'
        self.text_ur = 60
        self.frames = 0

        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):

        arcade.start_render()
        self.image_list.draw()
        arcade.draw_text(self.keyText, self.x / 2, 110, arcade.csscolor.WHITE, 16,
                         font_name='arial', anchor_x='center', bold=True)
        arcade.draw_text("press 'esc' to exit", self.x / 2, 80, arcade.csscolor.WHITE, 14,
                         font_name='arial', anchor_x='center', bold=True)

    def on_update(self, delta_time: float):
        self.frames += 1
        if self.frames < self.text_ur:
            self.keyText = 'press any key to play'

        elif self.frames < 2 * self.text_ur:
            self.keyText = 'press any key to play.'

        elif self.frames < 3 * self.text_ur:
            self.keyText = 'press any key to play..'

        elif self.frames < 4 * self.text_ur:
            self.keyText = 'press any key to play...'

        else:
            self.frames = 0

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            quit()

        else:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
