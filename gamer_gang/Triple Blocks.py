import random
import math
import arcade
import os
import itertools
import copy

SCALE = 1
OFFSCREEN_SPACE = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Triple Blocks"
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE
SCREEN_DIST = math.sqrt(SCREEN_HEIGHT ** 2 + SCREEN_WIDTH ** 2) / 2
SCREEN_MARGIN = 200


class GroundSprite(arcade.Sprite):
    def __init__(self, textures, scale, x, y):
        super().__init__()
        self.textures = textures
        self.texture = self.textures[0]
        self.scaling = scale
        self.center_x = x
        self.center_y = y

    def update(self):
        """ Move the sprite """
        super().update()


class PlayerSprite(arcade.Sprite):
    def __init__(self, textures, scale, x, y, name):
        super().__init__()
        self.textures = textures
        self.texture = self.textures[0]
        self.scaling = scale
        self.name = name

        self.acc_x = 0  # acceleration
        self.acc_y = 0

        self.center_x = x
        self.center_y = y
        self.og_x = self.center_x  # original x, which is x in the prev frame
        self.og_y = self.center_y

    def update(self):
        super().update()
        self.og_x = self.center_x
        self.og_y = self.center_y
        # self.center_x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):  # TODO: remember to add back the third sprite
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # set up the actual game
        self.frame_count = 0
        self.total_time = 0
        self.game_over = False
        self.debug_mode = False
        self.set_location(0, 0)
        self.camera_zoom = 1
        self.camera_x = SCREEN_WIDTH / -2
        self.camera_y = SCREEN_HEIGHT / -2
        self.gravity = 0.5
        self.key_pressed = [0, 0, 0]  # controllable

        self.ground_sprite_list = arcade.SpriteList()
        self.players = []
        self.view_left = 0
        self.view_bottom = 0

        self.controlled = 0

        self.ground_texture_list = [arcade.load_texture("images/ground/debug.png")]
        self.player_texture_list = [[arcade.load_texture("images/player/player1.jpg")],
                                    [arcade.load_texture("images/player/player2.jpg")],
                                    [arcade.load_texture("images/player/player3.jpg")]]

        for i in range(1, 4):  # TODO: make sprites
            object = PlayerSprite(self.player_texture_list[i - 1], SCALE, i * 32, 32 * 1, str(i))  # create the players
            self.players.append(object)

        a = arcade.SpriteList()
        b = arcade.SpriteList()
        c = arcade.SpriteList()
        a.append(self.players[1])
        a.append(self.players[2])
        b.append(self.players[0])
        b.append(self.players[2])
        c.append(self.players[0])
        c.append(self.players[1])

        for i in range(1, 30):  # make the ground
            object = GroundSprite(self.ground_texture_list, 1, (i - 10) * 32, 0)
            self.ground_sprite_list.append(object)
            a.append(object)
            b.append(object)
            c.append(object)

        self.physics_engines = []  # make the physics engines
        self.physics_engines.append(
            arcade.PhysicsEnginePlatformer(self.players[0], a, gravity_constant=self.gravity))
        self.physics_engines.append(
            arcade.PhysicsEnginePlatformer(self.players[1], b, gravity_constant=self.gravity))
        self.physics_engines.append(
            arcade.PhysicsEnginePlatformer(self.players[2], c, gravity_constant=self.gravity))

    def on_draw(self):  # simple rendering
        arcade.start_render()

        self.ground_sprite_list.draw()
        for p in self.players:
            p.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_pressed[1] = -0.3
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_pressed[0] = 0.3
        elif key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed[2] = 8
        # these are for when the player wants the switch
        elif key == arcade.key.NUM_1 or key == arcade.key.KEY_1:
            self.controlled = 0
        elif key == arcade.key.NUM_2 or key == arcade.key.KEY_2:
            self.controlled = 1
        elif key == arcade.key.NUM_3 or key == arcade.key.KEY_3:
            self.controlled = 2

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_pressed[1] = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_pressed[0] = 0
        elif key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed[2] = 0

    def camera_shift(self):
        changed = False
        left_boundary = self.view_left + SCREEN_MARGIN
        if self.players[self.controlled].left < left_boundary:
            self.view_left -= left_boundary - self.players[self.controlled].left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - SCREEN_MARGIN
        if self.players[self.controlled].right > right_boundary:
            self.view_left += self.players[self.controlled].right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - SCREEN_MARGIN
        if self.players[self.controlled].top > top_boundary:
            self.view_bottom += self.players[self.controlled].top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + SCREEN_MARGIN
        if self.players[self.controlled].bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.players[self.controlled].bottom
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom - 1)

    def check_stack(self):  # tests if one character is on top of another- if so, join
        for up, down in itertools.permutations(self.players, 2):
            # print(abs(up.left - down.left) < 20, abs(up.left - down.left))
            if up.bottom == down.top and abs(up.left - down.left) < 20:
                topList = []
                bottomList = []
                for v, p in enumerate(self.players):
                    if p.name == up.name:
                        topList.append(v)
                    elif p.name == down.name:
                        bottomList.append(v)
                print(topList, bottomList)
                stackName = f'{self.players[topList[0]].name}on{self.players[bottomList[0]].name}'
                for i in topList + bottomList:
                    self.players[i] = PlayerSprite([arcade.load_texture(f'images/player/{stackName}.png')],
                                                   SCALE, (up.left + up.right) // 2, up.bottom, stackName)

                    newEnginePlayers = copy.deepcopy(self.ground_sprite_list)
                    for v, p in enumerate(self.players):  # make a new engine
                        if v not in topList + bottomList:
                            newEnginePlayers.append(p)
                    self.physics_engines[i] = arcade.PhysicsEnginePlatformer(self.players[i], newEnginePlayers)

                print(self.players)
                break

    def movement(self):
        controlledSprite = self.players[self.controlled].name
        for v, p in enumerate(self.players):
            if p.name == controlledSprite:  # probs not the best implementation
                p.acc_x = self.key_pressed[0] + self.key_pressed[1]
                # accelerate the controlled sprite to a maximum speed of 3.5
                if abs(p.change_x) < 3.5:
                    p.change_x += p.acc_x

                p.change_y = self.key_pressed[2] if self.physics_engines[v].can_jump() else p.change_y

                if self.key_pressed[0] + self.key_pressed[1] == 0:  # if left AND right keys are pressed, cancel it
                    if abs(p.change_x) < 0.4:
                        p.change_x = 0
                    elif p.change_x < 0:  # these two serve deceleration
                        p.change_x += 0.3
                    else:
                        p.change_x = -0.3

    def on_update(self, x):
        self.frame_count += 1
        self.players[self.controlled].acc_x = self.key_pressed[0] + self.key_pressed[1]
        self.movement()
        self.camera_shift()
        self.check_stack()

        for s in self.players:
            if s.top < -500:
                self.game_over = True

        if not self.game_over:
            for i in self.ground_sprite_list:
                i.update()
            for i in self.players:
                i.update()
            for i in self.physics_engines:
                i.update()
        else:
            self.close()


def main():
    actualGame = MyGame()
    arcade.run()


main()
