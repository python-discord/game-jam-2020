# setup
import arcade
# from arcade.gui import *
from submission.gameConstants import *
from submission.loadAnimatedChars import *
from submission.tileMapLoader import *
from submission.spell import pickUp
from submission.sounds import loadSounds
from submission.motion import *
from submission.waveManager import getSpawnList, manageEnemySpawn, EnemyGroup
from random import randint
import math


def getGridCase(position, offset_x, offset_y):
    case = [math.floor((position[0] - offset_x) / 32), math.floor((position[1] - offset_y) / 32)]
    return case


# Class defining
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, windowTitle):
        if FULLSCREEN:
            super(MyGame, self).__init__(width, height, windowTitle, fullscreen=True)
        else:
            super(MyGame, self).__init__(width, height, windowTitle, fullscreen=False)

        self.ground_list = None
        self.path_list = None
        self.player_list = None
        self.entity_list = None
        self.turret_list = None

        self.player_sprite = None

        self.game_mode = None

        self.mouse_x = 0
        self.mouse_y = 0

        self.mouse_click = [0, 0]
        self.destination = [-1, -1]
        self.order_list = []

        self.sound_dict = {}

        self.window_offset_x = 0
        self.window_offset_y = 0

        self.screen_x = 0
        self.screen_y = 0

        self.mosquito = None

        self.newOrder = None
        self.currentOrder = None
        self.orderCount = None

        self.betweenRounds = True  # mettre à false
        self.roundNumber = 0
        self.spawnList = None

        arcade.set_background_color((94, 132, 63))

    def setup(self):
        """ Set up the test here. Call this function to restart the test. """
        if FULLSCREEN:
            self.screen_x, self.screen_y = self.get_size()
            self.window_offset_x = (self.screen_x / 2) - WINDOW_WIDTH / 2
            self.window_offset_y = (self.screen_y / 2) - WINDOW_HEIGHT / 2

        self.player_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList(is_static=True)
        self.path_list = arcade.SpriteList(is_static=True)
        self.entity_list = arcade.SpriteList()
        self.turret_list = arcade.SpriteList()

        self.player_sprite = AnimatedPlayer('player', 4)
        self.player_sprite.center_x = BP_PLAYER[0] * 32 + 16
        self.player_sprite.center_y = BP_PLAYER[1] * 32 + 16
        self.player_list.append(self.player_sprite)

        self.turret_list.append(AnimatedEntity(T_SPRAY, 2, BP_SPRAY))
        self.turret_list.append(AnimatedEntity(T_LAMP, 2, BP_LAMP))
        self.turret_list.append(AnimatedEntity(T_VACUUM, 2, BP_VACUUM))

        self.path_list = loadPathTilemap()

        for i in range(len(self.path_list)):
            self.path_list[i].center_x += self.window_offset_x
            self.path_list[i].center_y += self.window_offset_y

        for x in range(0, WINDOW_WIDTH, TILE_SIZE):  # Crée le fond à l'aide des grasstiles
            for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
                if x >= 29 * TILE_SIZE:
                    if x == 29 * TILE_SIZE:
                        ground = arcade.Sprite(PATH['img'] / "tiles\\townTile1.png", TILE_SCALING)
                    else:
                        ground = arcade.Sprite(PATH['img'] / "tiles\\townTile2.png", TILE_SCALING)

                else:
                    randomNum = randint(1, 3)
                    ground = arcade.Sprite(PATH['img'] / f"tiles\\grassTile{randomNum}.png", TILE_SCALING)

                ground.center_x = x + TILE_SIZE * TILE_SCALING / 2 + self.window_offset_x
                ground.center_y = y + TILE_SIZE * TILE_SCALING / 2 + self.window_offset_y
                self.ground_list.append(ground)

        loadSounds(self.sound_dict)

    def on_draw(self):
        """ Renders the screen. """

        arcade.start_render()
        # Ground layer
        self.ground_list.draw()
        self.path_list.draw()
        # Entity layer
        self.turret_list.draw()
        self.entity_list.draw()
        # Turrets layer

        # Player layer
        self.player_list.draw()

        # GUI layer

    def on_update(self, delta_time: float):
        """ On Update method"""
        updateActualPos(self.player_sprite)
        movePlayer(self.player_sprite, delta_time)

        if self.betweenRounds:
            self.spawnList = getSpawnList(self.roundNumber)
            self.betweenRounds = False

        self.player_list.update_animation()
        self.entity_list.update_animation()
        self.turret_list.update_animation()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Get keyboard's presses. """
        if symbol == arcade.key.Q:
            pickUp(self.player_sprite, self.player_list, self.path_list, self.turret_list)

        if symbol == arcade.key.D:
            self.entity_list.append(AnimatedEntity(E_ANT, 2, [0, 0]))
            self.entity_list.append(AnimatedEntity(E_MOSQUITO, 4, [1, 0]))
            self.entity_list.append(AnimatedEntity(E_SPIDER, 2, [2, 0]))

        if symbol == arcade.key.F:
            self.betweenRounds = True
            self.roundNumber += 1

    def on_key_release(self, symbol: int, modifiers: int):
        """ Get keyboard's releases. """
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Get mouse's presses. """
        if not self.player_sprite.is_moving:
            if FULLSCREEN:
                if self.mouse_x > self.screen_x / 2 + WINDOW_WIDTH / 2 or self.mouse_x < self.screen_x / 2 - WINDOW_WIDTH / 2:
                    print('Cannot move')
                elif self.mouse_y > self.screen_y / 2 + WINDOW_HEIGHT / 2 or self.mouse_y < self.screen_y / 2 - WINDOW_HEIGHT / 2:
                    print('Cannot move')

                else:
                    self.mouse_click = [self.mouse_x, self.mouse_y]
                    self.player_sprite.destination = getGridCase(self.mouse_click, self.window_offset_x, self.window_offset_y)

            else:
                self.mouse_click = [self.mouse_x, self.mouse_y]
                self.player_sprite.destination = getGridCase(self.mouse_click, self.window_offset_x, self.window_offset_y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Get mouse's releases. """
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_x = x
        self.mouse_y = y
