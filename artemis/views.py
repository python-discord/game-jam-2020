import arcade

from constants import BACKGROUND, WIDTH, HEIGHT, ASSETS, INSTRUCTIONS
from game import Game


class Button(arcade.gui.TextButton):
    def __init__(self, view, x, y, text, switch_to, width=100, height=40):
        super().__init__(x, y, width, height, text, theme=view.theme)
        self.window = view.window
        self.switch_to = switch_to

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.window.show_view(self.switch_to())


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


class Instructions(View):
    def on_show(self):
        self.button_list.append(Button(self, WIDTH/2-75, 50, 'Back', Menu))
        self.button_list.append(Button(self, WIDTH/2+75, 50, 'Play', Game))

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'Instructions', WIDTH/2, HEIGHT-75,
            arcade.color.WHITE, font_size=50, anchor_x='center',
        )
        arcade.draw_text(
            INSTRUCTIONS, WIDTH/2,  HEIGHT/2, arcade.color.WHITE,
            font_size=20, anchor_x='center', anchor_y='center',
            align='center'
        )


class Menu(View):
    def on_show(self):
        self.button_list.append(
            Button(self, WIDTH/2, HEIGHT/2-50, 'Play', Game)
        )
        self.button_list.append(Button(
            self, WIDTH/2, HEIGHT/2-100, 'Help', Instructions
        ))

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'Menu', WIDTH/2, HEIGHT/2,
            arcade.color.WHITE, font_size=50, anchor_x='center'
        )


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
        self.window.show_view(Game())

    def on_key_release(self, key, modifiers):
        self.window.show_view(Game())