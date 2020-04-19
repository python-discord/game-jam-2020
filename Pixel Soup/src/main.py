import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Game"


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.WHITE)

    def setup(self) -> None:
        """Inital settings. Useful when restarting the game."""

    def on_draw(self) -> None:
        """Render the screen."""
        arcade.start_render()


def main() -> None:
    """Entry point of the game."""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
