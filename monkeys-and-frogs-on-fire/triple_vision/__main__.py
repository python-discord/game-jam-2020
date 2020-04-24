import arcade

from triple_vision import Settings as s
from triple_vision.main_menu import MainMenu


def main() -> None:
    window = arcade.Window(*s.WINDOW_SIZE, s.TITLE)
    game = MainMenu()

    window.show_view(game)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
