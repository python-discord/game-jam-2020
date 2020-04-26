import arcade

from .gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from .views.mainview import MainView

import logging
import multiprocessing


def main() -> None:
    """Entry point of the game."""
    logging.basicConfig(level=logging.INFO)

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    joysticks = arcade.get_joysticks()
    """
    Add support for the first joystick found, it can be changed later
    in settings.
    """
    window.joystick = None
    if joysticks:
        window.joystick = joysticks[0]
        window.joystick.open()

    main_view = MainView()
    window.show_view(main_view)
    main_view.setup()
    arcade.run()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
