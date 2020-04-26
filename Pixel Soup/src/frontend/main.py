import arcade

from .gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from .views.mainview import MainView

import os
import logging
from .networking import net_interface
import socket
import multiprocessing


def main() -> None:
    """Entry point of the game."""
    logging.basicConfig(level=logging.INFO)

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    window.pl = net_interface.Pipe(
        server=socket.gethostname(), port=int(os.getenv("PORT"))
    )
    print(window.pl.login(entry="create", room_name="game3", username="David"))
    for _ in range(3):
        print(window.pl.await_response())

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
    main_view.setup()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
