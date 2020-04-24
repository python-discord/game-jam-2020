import arcade


class AdventuresGame(arcade.Window):
    """Adventures of 3 Balls main game class."""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.APPLE_GREEN)

    def setup(self) -> None:
        """Setup/reset game state."""
        pass

    def on_draw(self) -> None:
        """Render game screen."""
        arcade.start_render()
