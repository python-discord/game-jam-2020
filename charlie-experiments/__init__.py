"""
2048 Clone
Paul Vincent Craven
"""


import arcade

from main import MyGame


def main():
    my_game = MyGame()
    my_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()