import arcade

from constants import BACKGROUND, WIDTH, HEIGHT, ASSETS
from game import Game


class View(arcade.View):
    def __init__(self):
        super().__init__()
        self.theme = arcade.gui.Theme()
        image = ASSETS + 'button_{}.png'
        self.theme.add_button_textures(
            image.format('normal'), image.format('hover'),
            image.format('active'), image.format('locked')
        )

    def on_show(self):
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)


class PlayButton(arcade.gui.TextButton):
    def __init__(self, window, x, y, theme=None):
        super().__init__(x, y, 100, 40, 'Play', theme=theme)
        self.window = window

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.window.show_view(Game())


class Instructions(View):
    def on_show(self):
        self.button_list.append(
            PlayButton(self.window, WIDTH/2, HEIGHT/2-75, self.theme)
        )

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'Instructions', WIDTH/2, HEIGHT/2,
            arcade.color.WHITE, font_size=50, anchor_x='center',
        )


class Menu(View):
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            'Menu', WIDTH/2, HEIGHT/2,
            arcade.color.WHITE, font_size=50, anchor_x='center'
        )
        arcade.draw_text(
            'Click anywhere to continue', WIDTH/2, HEIGHT/2-75,
            arcade.color.GRAY, font_size=20, anchor_x='center'
        )

    def on_mouse_release(self, x, y, button, modifiers):
        self.window.show_view(Instructions())


class GameOver(View):
    def __init__(self, message):
        self.message = message
        super().__init__()

    def on_draw(self):
        arcade.start_render()
        # won't work without this for some reason
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.draw_text(
            'Game Over:', WIDTH/2, HEIGHT/2,
            arcade.color.RED, font_size=50, anchor_x='center'
        )
        arcade.draw_text(
            self.message, WIDTH/2, HEIGHT/2-50,
            arcade.color.RED, font_size=30, anchor_x='center'
        )
        arcade.draw_text(
            'Click anywhere to continue', WIDTH/2, HEIGHT/2-100,
            arcade.color.GRAY, font_size=20, anchor_x='center'
        )

    def on_mouse_release(self, x, y, button, modifiers):
        self.window.show_view(Menu())