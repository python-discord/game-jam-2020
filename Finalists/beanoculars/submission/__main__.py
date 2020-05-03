"""

'Insane Irradiated Insects'
A game of the python-discord game jam 2020, made
in 10 days, using the Arcade library and based on
the theme : Three of a kind
Author: sachapomme (or Sacha#8175)

"""
import arcade

from submission.game import GameView
from submission.menu import MenuView
from submission.gameOver import GameOverView
from submission.gameConstants import WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_TITLE


def main() -> None:
    """ Main """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    print('Window created')
    menu_view = MenuView()
    window.show_view(menu_view)
    print('Game view on screen')
    arcade.run()


if __name__ == "__main__":
    main()