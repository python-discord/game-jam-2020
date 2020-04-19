import random
import math
import arcade
import os
from typing import cast

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
SCREEN_MARGIN = 50


class GroundSprite(arcade.Sprite):
    def __init__(self, textures, scale, x, y):
        super().__init__()
        self.textures = textures
        self.texture = self.textures[0]
        self.scaling = scale
        self.x = x
        self.y = y

    def update(self, zoom, cx, cy):
        """ Move the sprite """
        super().update()
        self.scale = zoom * self.scaling
        self.center_x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
        self.center_y = (self.y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2


class PlayerSprite(arcade.Sprite):
    def __init__(self, textures, scale, x, y, zoom, cx, cy):
        super().__init__()
        self.textures = textures
        self.texture = self.textures[0]
        self.scaling = scale
        self.x = x
        self.y = y

        self.acc_x = 0  # acceleration
        self.acc_y = 0

        self.center_x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
        self.center_y = (self.y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2
        self.og_x = self.center_x  # original x, which is x in the prev frame
        self.og_y = self.center_y

    def update(self, zoom, cx, cy):
        self.scale = zoom * self.scaling
        self.og_x = self.center_x
        self.og_y = self.center_y
        # self.center_x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
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
        self.player_sprite_list = arcade.SpriteList()
        self.view_left = 0
        self.view_bottom = 0

        self.controlled = 0

        self.ground_texture_list = [arcade.load_texture("images/ground/debug.png")]
        self.player_texture_list = [arcade.load_texture("images/player/debug.png")]

        for i in range(1, 4):  # TODO: make sprites
            object = PlayerSprite(self.player_texture_list, 1, i * 32, 32 * 1, self.camera_zoom, self.camera_x,
                                  self.camera_y)  # create the players
            self.player_sprite_list.append(object)

            # so the players can interact with each other and not just give the game a seizure
        a = arcade.SpriteList()
        b = arcade.SpriteList()
        c = arcade.SpriteList()
        a.append(self.player_sprite_list[1])
        a.append(self.player_sprite_list[2])
        b.append(self.player_sprite_list[0])
        b.append(self.player_sprite_list[2])
        c.append(self.player_sprite_list[0])
        c.append(self.player_sprite_list[1])

        for i in range(1, 30):  # make the ground
            object = GroundSprite(self.ground_texture_list, 1, (i - 10) * 32, 0)
            self.ground_sprite_list.append(object)
            a.append(object)
            b.append(object)
            c.append(object)

        self.physics_engines = []  # make the physics engines
        self.physics_engines.append(
            arcade.PhysicsEnginePlatformer(self.player_sprite_list[0], a, gravity_constant=self.gravity))
        self.physics_engines.append(
            arcade.PhysicsEnginePlatformer(self.player_sprite_list[1], b, gravity_constant=self.gravity))
        self.physics_engines.append(
            arcade.PhysicsEnginePlatformer(self.player_sprite_list[2], c, gravity_constant=self.gravity))

    def on_draw(self):  # simple rendering
        arcade.start_render()

        self.ground_sprite_list.draw()
        self.player_sprite_list.draw()

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
        if self.player_sprite_list[self.controlled].left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite_list[self.controlled].left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - SCREEN_MARGIN
        if self.player_sprite_list[self.controlled].right > right_boundary:
            self.view_left += self.player_sprite_list[self.controlled].right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - SCREEN_MARGIN
        if self.player_sprite_list[self.controlled].top > top_boundary:
            self.view_bottom += self.player_sprite_list[self.controlled].top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + SCREEN_MARGIN
        if self.player_sprite_list[self.controlled].bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite_list[self.controlled].bottom
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom - 1)

    def on_update(self, x):
        """ Move everything """

        self.frame_count += 1
        self.player_sprite_list[self.controlled].acc_x = self.key_pressed[0] + self.key_pressed[1]
        if self.player_sprite_list[self.controlled].top < -1000:
            self.game_over = True
        # accelerate the controlled sprite to a maximum speed of 3.5
        if abs(self.player_sprite_list[self.controlled].change_x) < 3.5:
            self.player_sprite_list[self.controlled].change_x += self.player_sprite_list[self.controlled].acc_x

        self.player_sprite_list[self.controlled].change_y = self.key_pressed[2] if self.physics_engines[
            self.controlled].can_jump() else self.player_sprite_list[self.controlled].change_y

        if self.key_pressed[0] + self.key_pressed[1] == 0:  # if left AND right keys are pressed, cancel it
            if abs(self.player_sprite_list[self.controlled].change_x) < 0.4:
                self.player_sprite_list[self.controlled].change_x = 0
            elif self.player_sprite_list[self.controlled].change_x < 0:  # these two serve deceleration
                self.player_sprite_list[self.controlled].change_x += 0.3
            else:
                self.player_sprite_list[self.controlled].change_x = -0.3

        self.camera_shift()

        for s in self.player_sprite_list:
            if s.top < -500:
                self.game_over = True

        if not self.game_over:
            for i in self.ground_sprite_list:
                i.update(self.camera_zoom, self.camera_x, self.camera_y)
            for i in self.player_sprite_list:
                i.update(self.camera_zoom, self.camera_x, self.camera_y)
            for i in self.physics_engines:
                i.update()
        else:
            self.close()

def main():
    actualGame = MyGame()
    arcade.run()

main()
