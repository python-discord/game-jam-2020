import random
import math
import arcade
import os
import pymunk
from PIL import Image
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


class GroundSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, textures, scale, x, y):
        super().__init__()
        self.pymunk_shape = pymunk_shape

        self.textures = textures
        self.texture = self.textures[0]

        self.scaling = scale

        self.center_x = x
        self.center_y = y

    def update(self, zoom, cx, cy):
        """ Move the sprite """
        super().update()

        self.scale = zoom * self.scaling
        #
        # self.center_x = self.pymunk_shape.body.position.x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
        # self.center_y = self.pymunk_shape.body.position.y = (self.y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2


class PlayerSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, textures, scale, x, y):
        super().__init__()
        self.pymunk_shape = pymunk_shape
        self.can_jump = True

        self.textures = textures
        self.texture = self.textures[0]

        self.scaling = scale

        self.acc_x = 0
        self.acc_y = 0

        self.center_x = x
        self.center_y = y

        self.og_x = self.center_x
        self.og_y = self.center_y

    def update(self, zoom, cx, cy):
        self.scale = zoom * self.scaling
        self.og_x = self.center_x
        self.og_y = self.center_y


def make_player_sprite(mass, space, textures, scale, x, y, zoom, cx, cy):
    pos_x = (x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
    pos_y = (y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2

    width, height = textures[0].width, textures[0].height
    mass = mass
    body = pymunk.Body(mass, pymunk.inf)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    space.add(body, shape)
    sprite = PlayerSprite(shape, textures, scale, pos_x, pos_y)
    return sprite, body


def make_ground_sprite(space, textures, scale, x, y, zoom, cx, cy):
    pos_x = (x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
    pos_y = (y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2

    width, height = textures[0].width, textures[0].height
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    space.add(body, shape)
    sprite = GroundSprite(shape, textures, scale, pos_x, pos_y)
    return sprite


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.path = {0: 1, 1: 2, 2: 0, 4: 0, 5: 1, 3: 2}
        self.key = list(self.path.keys())

    def start_new_game(self):
        """ Set up the game and initialize the variables. """
        self.frame_count = 0
        self.total_time = 0
        self.game_over = False
        self.debug_mode = False
        self.set_location(0, 0)
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

        self.camera_zoom = 1
        self.camera_x = SCREEN_WIDTH / -2
        self.camera_y = SCREEN_HEIGHT / -2

        self.key_pressed = [0, 0, 0]  # controllable

        self.ground_sprite_list = arcade.SpriteList()
        self.player_sprite_list = arcade.SpriteList()

        self.selected_player = 0

        self.ground_texture_list = [arcade.load_texture("images/ground/debug.png")]
        self.player_texture_list = [arcade.load_texture("images/player/debug.png")]

        self.bodies = []
        self.joints = [None, None, None, None, None, None]
        for i in range(1, 4):
            object, body = make_player_sprite(1, self.space, self.player_texture_list, 1, i * 32, 32 * 1,
                                              self.camera_zoom, self.camera_x, self.camera_y)
            self.bodies.append(body)
            object.set_hit_box([[object.width / -2, object.height / -2 - 1], [object.width / 2, object.height / -2 - 1],
                                [object.width / 2, object.height / 2], [object.width / -2, object.height / 2]])
            object.color = (i * 100 - 50, i * 100 - 50, i * 100 - 50)
            self.player_sprite_list.append(object)

        for i in range(1, 10):
            object = make_ground_sprite(self.space, self.ground_texture_list, 1, i * 32, 32 * -5, self.camera_zoom,
                                        self.camera_x, self.camera_y)
            self.ground_sprite_list.append(object)

    def on_draw(self):
        arcade.start_render()

        self.ground_sprite_list.draw()
        self.player_sprite_list.draw()
        if self.debug_mode:
            for i in self.player_sprite_list:
                i.draw_hit_box((100, 100, 100), 3)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_pressed[1] = -30
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_pressed[0] = 30
        elif key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed[2] = 400
        elif key == arcade.key.NUM_1 or key == arcade.key.KEY_1:
            self.selected_player = 0
        elif key == arcade.key.NUM_2 or key == arcade.key.KEY_2:
            self.selected_player = 1
        elif key == arcade.key.NUM_3 or key == arcade.key.KEY_3:
            self.selected_player = 2

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_pressed[1] = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_pressed[0] = 0
        elif key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed[2] = 0

    def on_update(self, x):
        self.frame_count += 1
        for i in range(10):
            self.player_sprite_list[self.selected_player].pymunk_shape.body.position.y += 2
            self.space.step(1 / 600.0)
            self.player_sprite_list[self.selected_player].pymunk_shape.body.position.y -= 2

        if sum(self.key_pressed[:2]) == 0:
            for x, i in enumerate(self.joints):
                if i != None:
                    self.space.remove(i)  # [0],i[1])
                    self.joints[x] = None

        if sum(self.key_pressed[:2]) != 0 or self.key_pressed[2] != 0:
            if 31.5 <= (self.bodies[1].position.y - self.bodies[0].position.y) <= 32.5 and abs(
                    self.bodies[1].position.x - self.bodies[0].position.x) <= 32 and self.joints[
                0] == None and self.selected_player != 1:
                delta = pymunk.Vec2d((self.bodies[1].position.x - self.bodies[0].position.x, 0))
                joint = pymunk.PinJoint(self.bodies[0], self.bodies[1], self.bodies[0].position + delta,
                                        self.bodies[0].position + delta)
                self.joints[0] = joint
                self.space.add(joint)  # ,joint2)
            if 31.5 <= (self.bodies[2].position.y - self.bodies[1].position.y) <= 32.5 and abs(
                    self.bodies[2].position.x - self.bodies[1].position.x) <= 32 and self.joints[
                1] == None and self.selected_player != 2:
                delta = pymunk.Vec2d((self.bodies[2].position.x - self.bodies[1].position.x, 0))
                joint = pymunk.PinJoint(self.bodies[1], self.bodies[2], self.bodies[1].position + delta,
                                        self.bodies[1].position + delta)
                self.joints[1] = joint
                self.space.add(joint)
            if 31.5 <= (self.bodies[0].position.y - self.bodies[2].position.y) <= 32.5 and abs(
                    self.bodies[0].position.x - self.bodies[2].position.x) <= 32 and self.joints[
                2] == None and self.selected_player != 0:
                delta = pymunk.Vec2d((self.bodies[0].position.x - self.bodies[2].position.x, 0))
                joint = pymunk.PinJoint(self.bodies[2], self.bodies[0], self.bodies[2].position + delta,
                                        self.bodies[2].position + delta)
                self.joints[2] = joint
                self.space.add(joint)
            if 31.5 <= (self.bodies[0].position.y - self.bodies[1].position.y) <= 32.5 and abs(
                    self.bodies[0].position.x - self.bodies[1].position.x) <= 32 and self.joints[
                3] == None and self.selected_player != 0:
                delta = pymunk.Vec2d((self.bodies[0].position.x - self.bodies[1].position.x, 0))
                joint = pymunk.PinJoint(self.bodies[1], self.bodies[0], self.bodies[1].position + delta,
                                        self.bodies[1].position + delta)
                self.joints[3] = joint
                self.space.add(joint)
            if 31.5 <= (self.bodies[1].position.y - self.bodies[2].position.y) <= 32.5 and abs(
                    self.bodies[1].position.x - self.bodies[2].position.x) <= 32 and self.joints[
                4] == None and self.selected_player != 1:
                delta = pymunk.Vec2d((self.bodies[1].position.x - self.bodies[2].position.x, 0))
                joint = pymunk.PinJoint(self.bodies[2], self.bodies[1], self.bodies[2].position + delta,
                                        self.bodies[2].position + delta)
                self.joints[4] = joint
                self.space.add(joint)
            if 31.5 <= (self.bodies[2].position.y - self.bodies[0].position.y) <= 32.5 and abs(
                    self.bodies[2].position.x - self.bodies[0].position.x) <= 32 and self.joints[
                5] == None and self.selected_player != 2:
                delta = pymunk.Vec2d((self.bodies[2].position.x - self.bodies[1].position.x, 0))
                joint = pymunk.PinJoint(self.bodies[0], self.bodies[2], self.bodies[0].position + delta,
                                        self.bodies[0].position + delta)
                self.joints[5] = joint
                self.space.add(joint)

        if self.joints[0] != None and self.joints[4] != None:
            if self.selected_player == 0:
                self.space.remove(self.joints[4])
                self.joints[4] = None
            else:
                self.space.remove(self.joints[0])
                self.joints[0] = None
        elif self.joints[1] != None and self.joints[5] != None:
            if self.selected_player == 0:
                self.space.remove(self.joints[1])
                self.joints[1] = None
            else:
                self.space.remove(self.joints[5])
                self.joints[5] = None
        elif self.joints[2] != None and self.joints[3] != None:
            if self.selected_player == 2:
                self.space.remove(self.joints[3])
                self.joints[3] = None
            else:
                self.space.remove(self.joints[2])
                self.joints[2] = None

        self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity += pymunk.Vec2d(
            (sum(self.key_pressed[:2]), 0))
        if self.player_sprite_list[self.selected_player].can_jump == True:
            multiplier = 1
            if (self.joints[self.key.index(self.selected_player)] != None or self.joints[
                self.key.index(self.selected_player + 3)] != None):
                multiplier += 1
                if (self.joints[self.key.index(self.selected_player)] != None and self.joints[
                    self.key.index(self.selected_player + 3)] != None):
                    multiplier += 1
                else:
                    topper = self.path[self.selected_player] if self.joints[
                                                                    self.key.index(self.selected_player)] != None else \
                    self.path[self.selected_player + 3]
                    if (self.joints[self.key.index(topper)] != None or self.joints[self.key.index(topper + 3)] != None):
                        multiplier += 1
            self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity += pymunk.Vec2d(
                (0, self.key_pressed[2])) * multiplier
            self.player_sprite_list[self.selected_player].can_jump = False
        if self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity.x > 300:
            self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity = pymunk.Vec2d(
                (300, self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity.y))
        if self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity.x < -300:
            self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity = pymunk.Vec2d(
                (-300, self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity.y))

        if not self.game_over:
            for i in self.ground_sprite_list:
                i.update(self.camera_zoom, self.camera_x, self.camera_y)
            for i in self.player_sprite_list:
                i.update(self.camera_zoom, self.camera_x, self.camera_y)
                boxes = arcade.check_for_collision_with_list(i, self.ground_sprite_list)
                topper1 = self.path[self.selected_player] if self.joints[self.key.index(
                    self.selected_player)] != None else self.selected_player
                topper2 = self.path[self.selected_player + 3] if self.joints[self.key.index(
                    self.selected_player + 3)] != None else self.selected_player
                if_collide = [True for char in self.player_sprite_list if
                              arcade.check_for_collision(i, char) == True and char != i and char !=
                              self.player_sprite_list[topper1] and char != self.player_sprite_list[topper2]]
                if (boxes != [] or True in if_collide) and abs(i.pymunk_shape.body.velocity.y) < 3:
                    i.can_jump = True
            for i in self.player_sprite_list:
                # i.pymunk_shape.body.position.y += 1
                if i == self.player_sprite_list[0]:
                    print(i.pymunk_shape.body.position.y - i.center_y)
                i.center_x = i.pymunk_shape.body.position.x
                i.center_y = i.pymunk_shape.body.position.y
                i.angle = math.degrees(i.pymunk_shape.body.angle)


def main():
    """ Start the game """
    window = MyGame()
    window.start_new_game()
    arcade.run()


main()
