# Main fuck file
import arcade
import os

from submission.game import MyGame
from submission.gameConstants import WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_TITLE

def main() -> None:
    """ Main method """
    print('cwd: '+os.getcwd())
    if os.getcwd().endswith('beanoculars\\'):
        os.chdir(''.join(os.getcwd() + '\\submission'))
        print('new cwd: ' + os.getcwd())
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    print('Window created')
    window.setup()
    print('Game set up')
    arcade.run()


if __name__ == "__main__":
    main()