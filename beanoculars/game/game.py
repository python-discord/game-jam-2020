import arcade

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
WINDOW_TITLE = 'MyPythonGame'

# Scaling constants
PLAYER_SCALING = 1

# TODO find ideas

# Class defining
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, windowTitle):
        super(MyGame, self).__init__(width, height, windowTitle, resizable=True)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """ Renders the screen. """
        pass

    def on_update(self, delta_time: float):
        """ On Update method"""
        pass



    def on_key_press(self, symbol: int, modifiers: int):
        """ Get keyboard's presses. """
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        """ Get keyboards releases. """
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Get mouse presses. """
        pass

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Get mouse releases. """
        pass

    arcade.draw_text()



# Code
MyGame(WINDOW_WIDTH,WINDOW_HEIGHT,WINDOW_TITLE)
arcade.run()