# setup
import arcade
# from arcade.gui import *
from submission.gameConstants import *
from submission.loadAnimatedChars import *
from submission.tileMapLoader import *
import math


def getGridCase(position):
    case = [math.floor(position[0]/32),math.floor(position[1]/32)]
    return case

# Class defining
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, windowTitle):
        super(MyGame, self).__init__(width, height, windowTitle, resizable=False)

        self.ground_list = None
        self.path_list = None
        self.player_list = None

        self.player_sprite = None

        self.game_mode = ''

        self.mouse_x = 0
        self.mouse_y = 0

        self.mouse_click = [0,0]
        self.destination = [-1,-1]

        self.grid = None

        arcade.set_background_color(arcade.csscolor.PURPLE)

    def setup(self):
        """ Set up the test here. Call this function to restart the test. """
        self.player_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.path_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(PATH_ADD + "images\\sprite\\player.png", PLAYER_SCALING)
        self.player_sprite.center_x = WINDOW_WIDTH/2
        self.player_sprite.center_y = WINDOW_HEIGHT/2
        self.player_list.append(self.player_sprite)

        self.path_list = loadPathTilemap()

        for x in range(0, WINDOW_WIDTH, TILE_SIZE):  # Crée le fond à l'aide de grassTile.png
            for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
                ground = arcade.Sprite(PATH_ADD+"images\\tiles\\grassTile.png", TILE_SCALING)
                ground.center_x = x + TILE_SIZE * TILE_SCALING / 2
                ground.center_y = y + TILE_SIZE * TILE_SCALING / 2
                self.ground_list.append(ground)

    def on_draw(self):
        """ Renders the screen. """

        arcade.start_render()
        # Ground layer
        self.ground_list.draw()
        self.path_list.draw()
        # Player layer
        self.player_sprite.draw()

        # GUI layer

    def on_update(self, delta_time: float):
        """ On Update method"""
        if self.destination != [-1,-1]:
            self.player_sprite.center_x = self.destination[0] * TILE_SIZE + TILE_SIZE/2
            self.player_sprite.center_y = self.destination[1] * TILE_SIZE + TILE_SIZE/2
            self.destination = [-1,-1]

    def on_key_press(self, symbol: int, modifiers: int):
        """ Get keyboard's presses. """
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        """ Get keyboard's releases. """
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Get mouse's presses. """
        self.mouse_click = [self.mouse_x, self.mouse_y]
        self.destination = getGridCase(self.mouse_click)
        if button == 1: # Si clique gauche
            pass
        elif button == 4: # Si clique droit
            pass
    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Get mouse's releases. """
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_x = x
        self.mouse_y = y