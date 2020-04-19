import arcade
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

SETTINGS = yaml.load(open('settings.yaml', 'r'), Loader=Loader)

class Hecate(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Set up your game here
        pass

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass


def main():
    game = Hecate(SETTINGS['window']['width'], SETTINGS['window']['height'])
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
