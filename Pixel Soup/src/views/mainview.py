import arcade
from pyglet.input.base import Joystick

from ..gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT
from .mainmenuview import MainMenuView

from textwrap import dedent


class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None

    def on_show(self) -> None:
        """Called when MainView should draw."""
        if self.window.joystick:
            self.window.joystick.set_handler(
                "on_joybutton_release", self.on_joybutton_release
            )

    def on_draw(self) -> None:
        """Show the widgets."""
        arcade.start_render()

        # Draw the background
        arcade.draw_lrwh_rectangle_textured(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background
        )

        arcade.draw_text(
            dedent(
                f"""
            Welcome to {self.window.caption}!
            Press any key/button to start
            """
            ),
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
        )

    def setup(self) -> None:
        """Setup the view and initialize the variables."""
        self.background = arcade.load_texture(
            ":resources:images/backgrounds/abstract_1.jpg"
        )

    def _to_main_menu(self) -> None:
        """Switch to the Main Menu View."""
        main_menu_view = MainMenuView()
        self.window.show_view(main_menu_view)
        main_menu_view.setup()

        if self.window.joystick:
            self.window.joystick.remove_handler(
                "on_joybutton_release", self.on_joybutton_release
            )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Move to the next view when any key is pressed."""
        self._to_main_menu()

    def on_joybutton_release(self, joystick: Joystick, button: int) -> None:
        """Move to the next view when any joystick button is pressed."""
        self._to_main_menu()
