import arcade

from game.constants import TITLE, WINDOW_SIZE
from game.game import Game


def main() -> None:
    window = arcade.Window(*WINDOW_SIZE, TITLE)
    game = Game()

    window.show_view(game)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
