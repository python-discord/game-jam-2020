"""All the views other than Game."""
from PIL import Image
import arcade
import typing

from achievements import get_achievements
from constants import ABOUT, ASSETS, FONT, HEIGHT, WIDTH
from game import Game
from ui import Achievement, IconButton, View, ViewButton


class Paused(View):
    """Game paused view."""

    reset_viewport = False

    def __init__(self, game: Game):
        """Store game state."""
        self.game = game
        super().__init__()

    def on_show(self):
        """Create buttons."""
        super().on_show()
        y = HEIGHT / 2 - 50
        x = self.game.left + WIDTH / 2
        self.buttons.append(IconButton(self, x - 70, y, 'home', self.home))
        self.buttons.append(IconButton(self, x, y, 'play', self.play))
        self.buttons.append(
            IconButton(self, x + 70, y, 'restart', self.restart)
        )

    def home(self):
        """Show the menu view."""
        self.window.show_view(Menu())

    def play(self):
        """Go back to the game."""
        self.game.pauseplay.go()

    def restart(self):
        """Start a new game."""
        self.window.show_view(Game())

    def on_draw(self):
        """Draw buttons, game and title."""
        arcade.start_render()
        self.game.on_draw()
        arcade.draw_text(
            'Paused', self.game.left + WIDTH / 2, HEIGHT / 2 + 50,
            arcade.color.BLACK, font_size=50, anchor_x='center',
            font_name=FONT.format(type='b')
        )
        super().on_draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Check own buttons and game buttons."""
        for view in (super(), self.game):
            view.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """Check own buttons and game buttons."""
        for view in (super(), self.game):
            view.on_mouse_release(x, y, button, modifiers)


class About(View):
    """View for the info text."""

    def on_show(self):
        """Create back button."""
        super().on_show()
        self.buttons.append(ViewButton(self, WIDTH / 2, 200, 'home', Menu))

    def on_draw(self):
        """Draw text and back button."""
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'About', WIDTH / 2, HEIGHT - 200,
            arcade.color.WHITE, font_size=50, anchor_x='center',
            font_name=FONT.format(type='b')
        )
        arcade.draw_text(
            ABOUT, WIDTH / 2, HEIGHT / 2, arcade.color.WHITE,
            font_size=20, anchor_x='center', anchor_y='center',
            align='center', font_name=FONT.format(type='r')
        )


class Tutorial(View):
    """View to display animated tutorial."""

    def __init__(self):
        """Begin loading textures, set up counters and create home button."""
        super().__init__()
        self.textures = self.get_textures(ASSETS + 'tutorial.gif')
        self.texture = None
        self.time_till_change = 0
        self.done = False
        self.buttons.append(
            IconButton(self, WIDTH - 70, HEIGHT - 70, 'home', self.home)
        )

    def get_textures(self, file: str) -> typing.Iterable[arcade.Texture]:
        """Open a GIF and yield a texture for each frame."""
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

    def home(self):
        """Switch to the menu view."""
        self.window.show_view(Menu())

    def on_update(self, timedelta: int):
        """Switch to the next frame."""
        super().on_update(timedelta)
        self.time_till_change -= timedelta
        if self.time_till_change <= 0 and not self.done:
            try:
                self.texture, self.time_till_change = next(self.textures)
            except StopIteration:
                self.done = True
                self.buttons = []
                self.on_top = []
                self.buttons.append(
                    ViewButton(self, WIDTH / 2 - 35, HEIGHT / 2, 'home', Menu)
                )
                self.buttons.append(
                    ViewButton(self, WIDTH / 2 + 35, HEIGHT / 2, 'play', Game)
                )

    def on_draw(self):
        """Display the current frame."""
        arcade.start_render()
        if self.texture and not self.done:
            self.texture.draw_scaled(WIDTH / 2, HEIGHT / 2)
        super().on_draw(start_render=False)


class Menu(View):
    """View for the main menu/home screen."""

    def on_show(self):
        """Create the buttons."""
        super().on_show()
        self.buttons.append(ViewButton(
            self, WIDTH / 2, HEIGHT / 2 - 50, 'play', Game
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2 - 70, HEIGHT / 2 - 50, 'help', Tutorial
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2 + 70, HEIGHT / 2 - 50, 'about', About
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2, HEIGHT / 2 - 120, 'achievements', Achievements
        ))

    def on_draw(self):
        """Display the buttons and title."""
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'Artemis: Gem Matcher', WIDTH / 2, HEIGHT / 2,
            arcade.color.WHITE, font_size=50, anchor_x='center',
            anchor_y='bottom', font_name=FONT.format(type='b')
        )


class GameOver(View):
    """View for the game over screen."""

    def __init__(self, message: str):
        """Store an explanatory message to display."""
        self.message = message
        super().__init__()

    def on_draw(self):
        """Draw text."""
        arcade.start_render()
        # won't work without this for some reason
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.draw_text(
            'Game Over:', WIDTH / 2, HEIGHT / 2,
            arcade.color.RED, font_size=50, anchor_x='center',
            font_name=FONT.format(type='b')
        )
        arcade.draw_text(
            self.message, WIDTH / 2, HEIGHT / 2 - 50,
            arcade.color.RED, font_size=30, anchor_x='center',
            font_name=FONT.format(type='m')
        )
        arcade.draw_text(
            'Click anywhere to continue', WIDTH / 2, HEIGHT / 2 - 100,
            arcade.color.GRAY, font_size=20, anchor_x='center',
            font_name=FONT.format(type='ri')
        )

    def on_mouse_release(self, _x: int, _y: int, _button: int,
                         _modifiers: int):
        """Start a new game on any mouse click."""
        self.window.show_view(Game())

    def on_key_release(self, key: int, modifiers: int):
        """Start a new game on any keyboard click."""
        self.window.show_view(Game())


class Achievements(View):
    """View to display achievements."""

    def on_show(self):
        """Create displays for all the achievements."""
        super().on_show()
        achievements = get_achievements()
        x = WIDTH / 2 - 140
        y = HEIGHT / 2 + 105
        for row in achievements:
            for data in row:
                x += 70
                self.buttons.append(Achievement(
                    self, x, y, data['type'], data['level'], data['name'],
                    data['description'], data['achieved']
                ))
            y -= 70
            x = WIDTH / 2 - 140
        self.buttons.append(
            ViewButton(self, WIDTH / 2, HEIGHT / 2 - 190, 'home', Menu)
        )

    def on_draw(self):
        """Draw the text and buttons to the screen."""
        super().on_draw()
        arcade.draw_text(
            'Achievements', WIDTH / 2, HEIGHT / 2 + 155,
            arcade.color.WHITE, font_size=30, anchor_x='center',
            font_name=FONT.format(type='b')
        )
