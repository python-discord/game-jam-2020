import arcade

from triple_vision.constants import TITLE, WINDOW_SIZE
from triple_vision.triple_vision import TripleVision


def main() -> None:
    window = arcade.Window(*WINDOW_SIZE, TITLE)
    game = TripleVision()

    window.show_view(game)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
