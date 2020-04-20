import arcade

from .pauseview import PauseView


class GameView(arcade.View):
    def on_show(self) -> None:
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self) -> None:
        arcade.start_render()

    def setup(self) -> None:
        pass

    def pause_game(self) -> None:
        """Switch to a Pause view."""
        pause = PauseView(self)
        self.window.show_view(pause)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Catch key events."""
        if key == arcade.key.ESCAPE:
            self.pause_game()
