# setup
import arcade
from arcade.gui import TextButton  # don't use textbox
from submission.gameConstants import *
from submission.loadAnimatedChars import *
from submission.tileMapLoader import *
from submission.spell import pickUp
from submission.sounds import loadSounds
from submission.motion import moveEntities, updateActualPos, movePlayer
from submission.waveManager import getSpawnList, manageEnemySpawn, decomposeSpawnList, generateASpawn, \
    EnemyGroup, SpawnOrder
from submission.get_farthest_sprite import get_farthest_sprite
from submission.gameOver import GameOverView
from submission.turretAttack import turretAttack
from random import randint
import math


def getGridCase(position, offset_x, offset_y):
    case = [math.floor((position[0] - offset_x) / 32), math.floor((position[1] - offset_y) / 32)]
    return case


# Class defining
class GameView(arcade.View):
    """
    Game View
    """

    def __init__(self):
        super().__init__()

        self.ground_list = None
        self.path_list = None
        self.player_list = None
        self.entity_list = None
        self.turret_list = None
        self.dmg_list = None

        self.player_sprite = None

        self.game_mode = None

        self.mouse_x = None
        self.mouse_y = None

        self.mouse_click = None
        self.destination = None
        self.order_list = None

        self.sound_dict = None

        self.window_offset_x = None
        self.window_offset_y = None

        self.screen_x = None
        self.screen_y = None

        self.mosquito = None

        self.newOrder = None
        self.currentOrder = None
        self.orderCount = None

        self.betweenRounds = True
        self.roundNumber = None
        self.spawnList = None
        self.roundTime = None
        self.firstRound = True

        self.shownRoundNumber = None

        self.animationDeltaTime = None

        self.game_over = False

        self.generatedTimeSinceFirst = None

        arcade.set_background_color((94, 132, 63))

    def setup(self):
        """ Set up the test here. Call this function to restart the test. """
        self.roundNumber = 0
        self.roundTime = 0
        self.shownRoundNumber = 1
        self.animationDeltaTime = 0
        self.generatedTimeSinceFirst = 0

        self.screen_x = 0
        self.screen_y = 0
        self.window_offset_x = 0
        self.window_offset_y = 0
        self.mouse_click = [0, 0]
        self.destination = [-1, -1]
        self.order_list = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.sound_dict = {}

        self.player_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList(is_static=True)
        self.path_list = arcade.SpriteList(is_static=True)
        self.entity_list = arcade.SpriteList()
        self.turret_list = arcade.SpriteList()
        self.dmg_list = arcade.SpriteList()

        self.player_sprite = AnimatedPlayer('player', 4)
        self.player_sprite.center_x = BP_PLAYER[0] * 32 + 16
        self.player_sprite.center_y = BP_PLAYER[1] * 32 + 16
        self.player_list.append(self.player_sprite)

        self.turret_list.append(AnimatedEntity(T_SPRAY, BP_SPRAY))
        self.turret_list.append(AnimatedEntity(T_LAMP, BP_LAMP))
        self.turret_list.append(AnimatedEntity(T_VACUUM, BP_VACUUM))

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
        self.dmg_list.draw()
        # Turrets layer

        # Player layer
        self.player_list.draw()

        # GUI layer

        if self.betweenRounds:
            arcade.draw_rectangle_filled(96, 484, 204, 54, (70, 92, 32))
            arcade.draw_rectangle_filled(99, 484, 192, 48, arcade.csscolor.DARK_OLIVE_GREEN)

        elif not self.betweenRounds:
            arcade.draw_rectangle_filled(96, 484, 204, 54, (75, 0, 0))
            arcade.draw_rectangle_filled(99, 484, 192, 48, arcade.csscolor.DARK_RED)

        if self.shownRoundNumber < 99:
            arcade.draw_text("Wave number: " + str(self.shownRoundNumber), 10, 512 - 44, arcade.csscolor.WHITE, 18,
                             font_name='arial', bold=True)

        elif self.shownRoundNumber < 999:
            arcade.draw_text("Wave number: " + str(self.shownRoundNumber), 10, 512 - 44, arcade.csscolor.WHITE, 16,
                             font_name='arial', bold=True)

    def on_update(self, delta_time: float):
        """ On Update method"""
        self.animationDeltaTime += 1

        updateActualPos(self.player_sprite)
        movePlayer(self.player_sprite, delta_time)
        self.game_over = moveEntities(self.entity_list, self.path_list, delta_time)

        if self.game_over:
            gameOver_view = GameOverView(self)
            self.window.show_view(gameOver_view)

        if not self.betweenRounds:
            if self.spawnList:
                self.roundTime = manageEnemySpawn(self.entity_list, self.spawnList, self.roundTime, delta_time, [0, 13],
                                                  [0, 8], [0, 3])

            if not self.spawnList:
                if not self.entity_list:
                    self.betweenRounds = True
                    self.roundNumber += 1

            if len(self.entity_list) > 0 and len(self.turret_list) > 0:
                for i in range(len(self.turret_list)):
                    turretAttack(self.turret_list[i], self.entity_list, delta_time, self.dmg_list)

        self.player_list.update_animation()
        self.dmg_list.update_animation()
        if self.animationDeltaTime >= 10:
            self.animationDeltaTime = 0
            self.entity_list.update_animation()
            self.turret_list.update_animation()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Get keyboard's presses. """
        if symbol == arcade.key.Q:
            pickUp(self.player_sprite, self.player_list, self.path_list, self.turret_list)

        if symbol == arcade.key.D:
            self.entity_list.append(AnimatedEntity(E_ANT, [0, 13]))
            self.entity_list.append(AnimatedEntity(E_MOSQUITO, [0, 8]))
            self.entity_list.append(AnimatedEntity(E_SPIDER, [0, 3]))

        if symbol == arcade.key.F:
            for i in range(len(self.entity_list)):
                self.entity_list[0].kill()

        if symbol == arcade.key.S:
            self.sound_dict['test1.wav'].play()

        if symbol == arcade.key.ENTER:
            if self.firstRound:
                self.roundTime = 0
                self.roundNumber = 0
                self.spawnList = decomposeSpawnList(getSpawnList(self.roundNumber, self.generatedTimeSinceFirst))
                self.betweenRounds = False
                self.firstRound = False

            elif self.betweenRounds:
                self.roundTime = 0
                self.shownRoundNumber += 1
                self.spawnList = decomposeSpawnList(getSpawnList(self.roundNumber, self.generatedTimeSinceFirst))
                self.betweenRounds = False

    def on_key_release(self, symbol: int, modifiers: int):
        """ Get keyboard's releases. """
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Get mouse's presses. """
        # if not self.player_sprite.is_moving:

        self.mouse_click = [self.mouse_x, self.mouse_y]
        self.player_sprite.destination = getGridCase(self.mouse_click, self.window_offset_x, self.window_offset_y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Get mouse's releases. """
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_x = x
        self.mouse_y = y
