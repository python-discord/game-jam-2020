import arcade

from triple_vision import Settings as s
from triple_vision.triple_vision import TripleVision


def main() -> None:
    window = arcade.Window(*s.WINDOW_SIZE, s.TITLE)
    game = TripleVision()

    window.show_view(game)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
