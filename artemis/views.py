import arcade
from PIL import Image

from constants import (
    BACKGROUND, WIDTH, HEIGHT, ASSETS, INSTRUCTIONS, ABOUT, FONT
)
from game import Game
from ui import ViewButton, IconButton, View


class Paused(View):
    reset_viewport = False

    def __init__(self, game):
        self.game = game
        super().__init__()

    def on_show(self):
        super().on_show()
        y = HEIGHT/2 - 50
        x = self.game.left + WIDTH/2
        self.buttons.append(IconButton(self, x-70, y, 'home', self.home))
        self.buttons.append(IconButton(self, x, y, 'play', self.play))
        self.buttons.append(
            IconButton(self, x+70, y, 'restart', self.restart)
        )

    def home(self):
        self.window.show_view(Menu())

    def play(self):
        self.game.pauseplay.go()

    def restart(self):
        self.window.show_view(Game())

    def on_draw(self):
        arcade.start_render()
        self.game.on_draw()
        arcade.draw_text(
            'Paused', self.game.left + WIDTH/2, HEIGHT/2 + 50,
            arcade.color.BLACK, font_size=50, anchor_x='center',
            font_name=FONT.format('b')
        )
        super().on_draw()

    def on_mouse_press(self, x, y, button, modifiers):
        print('!?')
        for view in (super(), self.game):
            view.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        print('?!')
        for view in (super(), self.game):
            view.on_mouse_release(x, y, button, modifiers)


class Instructions(View):
    def on_show(self):
        self.buttons.append(ViewButton(self, WIDTH/2-75, 50, 'back', Menu))
        self.buttons.append(ViewButton(self, WIDTH/2+75, 50, 'play', Game))

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'Instructions', WIDTH/2, HEIGHT-75,
            arcade.color.WHITE, font_size=50, anchor_x='center',
            font_name=FONT.format('b')
        )
        arcade.draw_text(
            INSTRUCTIONS, WIDTH/2,  HEIGHT/2, arcade.color.WHITE,
            font_size=20, anchor_x='center', anchor_y='center',
            align='center', font_name=FONT.format('r')
        )


class About(View):
    def on_show(self):
        super().on_show()
        self.buttons.append(ViewButton(self, WIDTH/2, 200, 'home', Menu))

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'About', WIDTH/2, HEIGHT-200,
            arcade.color.WHITE, font_size=50, anchor_x='center',
            font_name=FONT.format('b')
        )
        arcade.draw_text(
            ABOUT, WIDTH/2,  HEIGHT/2, arcade.color.WHITE,
            font_size=20, anchor_x='center', anchor_y='center',
            align='center', font_name=FONT.format('r')
        )


class Tutorial(View):
    def get_textures(self, file):
        gif = Image.open(file)
        n = 0
        while True:
            image = gif.resize((WIDTH, HEIGHT))
            texture = arcade.Texture(f'tutorial-{n}', image)
            yield texture, getattr(gif, 'duration', 100) / 1000
            n += 1
            try:
                gif.seek(n)
            except EOFError:
                break

    def on_show(self):
        super().on_show()
        self.textures = self.get_textures(ASSETS + 'tutorial.gif')
        self.texture = None
        self.time_till_change = 0
        self.done = False
        self.buttons.append(
            IconButton(self, WIDTH-70, HEIGHT-70, 'home', self.home)
        )

    def home(self):
        self.window.show_view(Menu())

    def on_update(self, timedelta):
        super().on_update(timedelta)
        self.time_till_change -= timedelta
        if self.time_till_change <= 0:
            try:
                self.texture, self.time_till_change = next(self.textures)
            except StopIteration:
                self.done = True
                self.buttons = []
                self.buttons.append(
                    ViewButton(self, WIDTH/2-35, HEIGHT/2, 'home', Menu)
                )
                self.buttons.append(
                    ViewButton(self, WIDTH/2+35, HEIGHT/2, 'play', Game)
                )

    def on_draw(self):
        arcade.start_render()
        if self.texture and not self.done:
            self.texture.draw_scaled(WIDTH/2, HEIGHT/2)
        super().on_draw()


class Menu(View):
    def on_show(self):
        super().on_show()
        self.buttons.append(
            ViewButton(self, WIDTH/2, HEIGHT/2-50, 'play', Game)
        )
        self.buttons.append(ViewButton(
            self, WIDTH/2-70, HEIGHT/2-50, 'help', Tutorial
        ))
        self.buttons.append(ViewButton(
            self, WIDTH/2+70, HEIGHT/2-50, 'about', About
        ))

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'Artemis: Gem Matcher', WIDTH/2, HEIGHT/2,
            arcade.color.WHITE, font_size=50, anchor_x='center',
            anchor_y='bottom', font_name=FONT.format('b')
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
            arcade.color.RED, font_size=50, anchor_x='center',
            font_name=FONT.format('b')
        )
        arcade.draw_text(
            self.message, WIDTH/2, HEIGHT/2-50,
            arcade.color.RED, font_size=30, anchor_x='center',
            font_name=FONT.format('m')
        )
        arcade.draw_text(
            'Click anywhere to continue', WIDTH/2, HEIGHT/2-100,
            arcade.color.GRAY, font_size=20, anchor_x='center',
            font_name=FONT.format('ri')
        )

    def on_mouse_release(self, x, y, button, modifiers):
        self.window.show_view(Game())

    def on_key_release(self, key, modifiers):
        self.window.show_view(Game())