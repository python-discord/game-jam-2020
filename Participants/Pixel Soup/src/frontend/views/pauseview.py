import arcade

from ..gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT

from textwrap import dedent


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self) -> None:
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self) -> None:
        arcade.start_render()

        arcade.draw_text(
            dedent(
                """
        Game paused.
        Press ESC to resume.
        """
            ),
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center",
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Resume the paused game when pressing ESC."""
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
