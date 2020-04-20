import arcade
from arcade.gui import Theme

from ..gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT
from .gameview import GameView


class NewGameButton(arcade.TextButton):
    def __init__(
        self,
        view_reference,
        x=0,
        y=0,
        width=100,
        height=40,
        text="New Game",
        theme=None,
    ):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view_reference = view_reference

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.view_reference.clear_buttons()

            game_view = GameView()
            game_view.setup()
            self.view_reference.window.show_view(game_view)


class LoadGameButton(arcade.TextButton):
    def __init__(
        self,
        view_reference,
        x=0,
        y=0,
        width=100,
        height=40,
        text="Load Game",
        theme=None,
    ):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view_reference = view_reference

    def on_press(self) -> None:
        self.pressed = True

    def on_release(self) -> None:
        if self.pressed:
            self.pressed = False


class SettingsButton(arcade.TextButton):
    def __init__(
        self,
        view_reference,
        x=0,
        y=0,
        width=100,
        height=40,
        text="Settings",
        theme=None,
    ):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view_reference = view_reference

    def on_press(self) -> None:
        self.pressed = True

    def on_release(self) -> None:
        if self.pressed:
            self.pressed = False


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.theme = None

    def on_show(self) -> None:
        pass

    def on_draw(self) -> None:
        arcade.start_render()

    def set_button_textures(self) -> None:
        """Give the same style to all the buttons using self.theme."""
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self) -> None:
        """Create a theme to be used by the Main Menu buttons."""
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.BLACK)
        self.set_button_textures()

    def set_buttons(self):
        """Initialize all the Main Menu buttons."""
        self.window.button_list.append(
            NewGameButton(
                self,
                0.5 * SCREEN_WIDTH,
                0.62 * SCREEN_HEIGHT,
                int(0.3 * SCREEN_WIDTH),
                int(0.1 * SCREEN_HEIGHT),
                theme=self.theme,
            )
        )

        self.window.button_list.append(
            LoadGameButton(
                self,
                0.5 * SCREEN_WIDTH,
                0.5 * SCREEN_HEIGHT,
                int(0.3 * SCREEN_WIDTH),
                int(0.1 * SCREEN_HEIGHT),
                theme=self.theme,
            )
        )

        self.window.button_list.append(
            SettingsButton(
                self,
                0.5 * SCREEN_WIDTH,
                0.38 * SCREEN_HEIGHT,
                int(0.3 * SCREEN_WIDTH),
                int(0.1 * SCREEN_HEIGHT),
                theme=self.theme,
            )
        )

    def clear_buttons(self) -> None:
        """
        Used to remove all the buttons in Main Menu while switching to
        another view.
        """
        self.window.button_list = []

    def setup(self) -> None:
        """Initialize the menu."""
        self.setup_theme()
        self.set_buttons()
