"""

'Insane Irradiated Insects'
A game of the python-discord game jam 2020, made
in 10 days, using the Arcade library and based on
the theme : Three of a kind
Author: sachapomme (or Sacha#8175)

"""
import arcade

from submission.game import MyGame
from submission.gameConstants import WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_TITLE, GM_MENU, GM_GAME

def main() -> None:
    """ Main method """
    gameMode = GM_GAME
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    print('Window created')
    window.setup()
    print('Game set up')
    arcade.run()


if __name__ == "__main__":
    main()