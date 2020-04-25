"""All the views other than Game."""
from PIL import Image
import arcade
import typing

from achievements import get_achievements
from constants import ABOUT, ASSETS, FONT, HEIGHT, MULTIPLAYER_HELP, WIDTH
from game import Game
from multiplayer import MultiplayerGame
from scores import add_award, get_awards
from settings import (
    get_sfx_volume, get_music_volume, set_sfx_volume, set_music_volume
)
from ui import Achievement, Award, IconButton, View, ViewButton, Slider


# keep track of restarts for award "The perfect spawn"
restarts = 0


class Paused(View):
    """Game paused view."""

    reset_viewport = False

    def __init__(self, game: Game, new: typing.Callable):
        """Store game state."""
        self.game = game
        self.create_new = new
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
        self.game.save()
        self.window.show_view(Menu())

    def play(self):
        """Go back to the game."""
        self.game.pauseplay.go()

    def restart(self):
        """Start a new game."""
        global restarts
        if isinstance(self.game, Game):
            restarts += 1
            if restarts == 4:
                add_award(1)
        self.game.save()
        self.window.show_view(self.create_new())

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

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Check own buttons and game buttons."""
        super().on_mouse_press(x, y, button, modifiers)
        self.game.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """Check own buttons and game buttons."""
        super().on_mouse_release(x, y, button, modifiers)
        self.game.on_mouse_release(x, y, button, modifiers)


class About(View):
    """View for the info text."""

    def on_show(self):
        """Create back button."""
        super().on_show()
        self.buttons.append(ViewButton(
            self, WIDTH / 2, HEIGHT / 2 - 150, 'home', Menu
        ))

    def on_draw(self):
        """Draw text and back button."""
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'About', WIDTH / 2, HEIGHT / 2 + 100,
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

    def get_textures(self, file: str
                     ) -> typing.Iterable[typing.Tuple[arcade.Texture,
                                                       float]]:
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

    def on_update(self, timedelta: float):
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
            self, WIDTH / 2 - 70, HEIGHT / 2 - 50,
            'multiplayer', MultiplayerMenu
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2, HEIGHT / 2 - 50, 'play', Game
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2 + 70, HEIGHT / 2 - 50, 'help', Tutorial
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2 - 70, HEIGHT / 2 - 120, 'about', About
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2, HEIGHT / 2 - 120,
            'achievements', Achievements
        ))
        self.buttons.append(IconButton(
            self, WIDTH / 2 + 70, HEIGHT / 2 - 120, 'quit', self.window.close
        ))
        # self.buttons.append(ViewButton(
        #     self, WIDTH / 2, HEIGHT / 2 - 190, 'settings', Settings
        # ))

    def on_draw(self):
        """Display the buttons and title."""
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'Artemis: Gem Matcher', WIDTH / 2, HEIGHT / 2,
            arcade.color.WHITE, font_size=50, anchor_x='center',
            anchor_y='bottom', font_name=FONT.format(type='b')
        )


class Settings(View):
    """Change game settings."""

    def __init__(self):
        """Create the buttons."""
        super().__init__()
        sfx_vol = get_sfx_volume()
        x = WIDTH / 2
        y = HEIGHT / 2 - 160
        self.sfx_slider = Slider(self, x, y, sfx_vol, self.set_sfx)
        self.buttons.append(self.sfx_slider)
        music_vol = get_music_volume()
        y -= 50
        self.music_slider = Slider(self, x, y, music_vol, self.set_music)
        self.buttons.append(self.music_slider)

    def set_sfx(self):
        value = self.sfx_slider.value
        set_sfx_volume(value)

    def set_music(self):
        value = self.music_slider.value
        set_music_volume(value)
        # update currently running music


class MultiplayerMenu(View):
    """View to select a multiplayer game."""

    def on_show(self):
        """Create the buttons."""
        super().on_show()
        self.buttons.append(ViewButton(
            self, WIDTH / 2 - 35, HEIGHT / 2 - 50, 'two_player',
            lambda: MultiplayerGame(2)
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2 + 35, HEIGHT / 2 - 50, 'three_player',
            lambda: MultiplayerGame(3)
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2 - 35, HEIGHT / 2 - 120, 'help', MultiplayerHelpOne
        ))
        self.buttons.append(ViewButton(
            self, WIDTH / 2 + 35, HEIGHT / 2 - 120, 'home', Menu
        ))

    def on_draw(self):
        """Display the buttons and title."""
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            'Multiplayer', WIDTH / 2, HEIGHT / 2,
            arcade.color.WHITE, font_size=50, anchor_x='center',
            anchor_y='bottom', font_name=FONT.format(type='b')
        )


class MultiplayerHelpOne(View):
    """Display the textual help for multiplayer mode."""

    def on_show(self):
        """Create the 'next' button."""
        super().on_show()
        self.buttons.append(ViewButton(
            self, WIDTH - 110, HEIGHT - 40, 'back', MultiplayerMenu
        ))
        self.buttons.append(ViewButton(
            self, WIDTH - 40, HEIGHT - 40, 'next', MultiplayerHelpTwo
        ))

    def on_draw(self):
        """Draw text and back button."""
        super().on_draw()
        arcade.draw_text(
            'Multiplayer', WIDTH / 2, HEIGHT / 2 + 100,
            arcade.color.WHITE, font_size=50, anchor_x='center',
            font_name=FONT.format(type='b')
        )
        arcade.draw_text(
            MULTIPLAYER_HELP, WIDTH / 2, HEIGHT / 2, arcade.color.WHITE,
            font_size=20, anchor_x='center', anchor_y='center',
            align='center', font_name=FONT.format(type='r')
        )


class MultiplayerHelpTwo(View):
    """Display the accompanying help image for multiplayer mode."""

    def on_show(self):
        """Create buttons and image."""
        super().on_show()
        self.buttons.append(ViewButton(
            self, WIDTH - 110, HEIGHT - 40, 'back', MultiplayerHelpOne
        ))
        self.buttons.append(ViewButton(
            self, WIDTH - 40, HEIGHT - 40, 'next', MultiplayerMenu
        ))
        x_scale = WIDTH / 1280
        y_scale = HEIGHT / 640
        scale = min((x_scale, y_scale))
        self.main = arcade.Sprite(
            ASSETS + 'multiplayer_help.png', scale=scale,
            center_x=WIDTH / 2, center_y=HEIGHT / 2
        )

    def on_draw(self):
        """Draw image and buttons."""
        arcade.start_render()
        self.main.draw()
        super().on_draw(start_render=False)


class GameOver(View):
    """View for the game over screen."""

    def __init__(self, message: str, scores: typing.List[int],
                 new: typing.Callable):
        """Store parameters."""
        self.message = message
        self.scores = scores
        self.create_new = new
        super().__init__()

    def on_draw(self):
        """Draw text."""
        global restarts
        arcade.start_render()
        restarts = 0
        # won't work without this for some reason
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        y = HEIGHT / 2 + 80
        arcade.draw_text(
            'Game Over:', WIDTH / 2, y,
            (255, 0, 0), font_size=50, anchor_x='center',
            font_name=FONT.format(type='b')
        )
        y -= 50
        arcade.draw_text(
            self.message, WIDTH / 2, y,
            (255, 0, 0), font_size=30, anchor_x='center',
            font_name=FONT.format(type='m')
        )
        y -= 60
        if len(self.scores) == 1:
            arcade.draw_text(
                f'Score: {self.scores[0]}', WIDTH / 2, y,
                (255, 255, 255), font_size=30, anchor_x='center',
                font_name=FONT.format(type='m')
            )
            y -= 30
        else:
            for n, score in enumerate(self.scores):
                arcade.draw_text(
                    f'Player {n + 1}: {score}', WIDTH / 2, y,
                    (255, 255, 255), font_size=30, anchor_x='center',
                    font_name=FONT.format(type='m')
                )
                y -= 40
            y -= 10
        arcade.draw_text(
            'Click anywhere to continue', WIDTH / 2, y,
            arcade.color.GRAY, font_size=20, anchor_x='center',
            font_name=FONT.format(type='ri')
        )

    def on_mouse_release(self, _x: float, _y: float, _button: int,
                         _modifiers: int):
        """Start a new game on any mouse click."""
        self.window.show_view(self.create_new())


class Achievements(View):
    """View to display achievements."""

    def on_show(self):
        """Create displays for all the achievements."""
        super().on_show()
        achievements = get_achievements()
        x = WIDTH / 2 - 140
        y = HEIGHT / 2 + 175
        for row in achievements:
            for data in row:
                x += 70
                self.buttons.append(Achievement(
                    self, x, y, data['type'], data['level'], data['name'],
                    data['description'], data['achieved']
                ))
            y -= 70
            x = WIDTH / 2 - 140
        awards = get_awards()
        x = WIDTH / 2 - 140
        for n, award in enumerate(awards):
            x += 70
            self.buttons.append(Award(
                self, x, y, n, award['name'], award['description'],
                award['achieved']
            ))
            if not (n + 1) % 3:
                y -= 70
                x = WIDTH / 2 - 140
        self.buttons.append(
            ViewButton(self, WIDTH / 2, HEIGHT / 2 - 260, 'home', Menu)
        )

    def on_draw(self):
        """Draw the text and buttons to the screen."""
        super().on_draw()
        arcade.draw_text(
            'Achievements', WIDTH / 2, HEIGHT / 2 + 225,
            arcade.color.WHITE, font_size=30, anchor_x='center',
            font_name=FONT.format(type='b')
        )
