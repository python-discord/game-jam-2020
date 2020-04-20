import random
import math
import arcade
import os
import pymunk
import pymunk.pygame_util

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
    def __init__(self, pymunk_shape, textures, scale, x, y):
        super().__init__()
        self.pymunk_shape = pymunk_shape

        self.textures = textures
        self.texture = self.textures[0]

        self.scaling = scale

        self.center_x = x
        self.center_y = y

    def update(self):
        """ Move the sprite """
        super().update()


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

        self.center_x = self.pymunk_shape.body.position.x
        self.center_y = self.pymunk_shape.body.position.y

        self.og_x = self.center_x
        self.og_y = self.center_y

    def update(self):
        self.og_x = self.center_x
        self.og_y = self.center_y


def make_player_sprite(mass, space, textures, scale, x, y):
    pos_x, pos_y = x, y

    width, height = textures[0].width, textures[0].height
    mass = mass
    # moment = pymunk.moment_for_box(mass, (width, height))
    body = pymunk.Body(mass, pymunk.inf)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    space.add(body, shape)
    sprite = PlayerSprite(shape, textures, scale, pos_x, pos_y)
    return sprite, body


def make_ground_sprite(space, textures, scale, x, y):
    pos_x, pos_y = x, y

    width, height = textures[0].width, textures[0].height
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    space.add(body, shape)
    sprite = GroundSprite(shape, textures, scale, pos_x, pos_y)
    return sprite


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):
        self.frame_count = 0
        self.total_time = 0
        self.game_over = False
        self.debug_mode = False
        # self.set_location(0, 0)
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.view_left = self.view_bottom = 0

        self.key_pressed = [0, 0, 0]  # controllable

        self.floorList = arcade.SpriteList()
        self.players = arcade.SpriteList()

        self.controlled = 0

        self.ground_texture_list = [arcade.load_texture("images/ground/debug.png")]
        self.player_texture_list = [arcade.load_texture("images/player/debug.png")]

        self.bodies = []
        self.joints = [None, None, None]
        for i in range(1, 4):
            object, body = make_player_sprite(1, self.space, self.player_texture_list, 1, 32, 32 * i)
            self.bodies.append(body)
            object.set_hit_box([[object.width / -2, object.height / -2 - 1], [object.width / 2, object.height / -2 - 1],
                                [object.width / 2, object.height / 2], [object.width / -2, object.height / 2]])
            object.color = (i * 100 - 50, i * 100 - 50, i * 100 - 50)
            self.players.append(object)

        for i in range(1, 30):
            object = make_ground_sprite(self.space, self.ground_texture_list, 1, i * 32, 32 * 0)
            self.floorList.append(object)

    def on_draw(self):
        arcade.start_render()

        self.floorList.draw()
        self.players.draw()
        if self.debug_mode:
            for i in self.players:
                i.draw_hit_box((100, 100, 100), 3)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_pressed[1] = -30
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_pressed[0] = 30
        elif key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed[2] = 450
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
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom, SCREEN_HEIGHT + self.view_bottom - 1)

    def on_update(self, x):
        self.frame_count += 1
        # self.players[self.controlled].pymunk_shape.body.rotation_vector = pymunk.Vec2d((0,0))
        for i in range(10):
            self.space.step(1 / 600.0)
        # self.players[self.controlled].pymunk_shape.body.angle = 0

        self.players[self.controlled].pymunk_shape.body.velocity += pymunk.Vec2d((sum(self.key_pressed[:2]), 0))
        if self.players[self.controlled].can_jump:
            self.players[self.controlled].pymunk_shape.body.velocity += pymunk.Vec2d((0, self.key_pressed[2]))
            self.players[self.controlled].can_jump = False

        if self.players[self.controlled].pymunk_shape.body.velocity.x > 300:
            self.players[self.controlled].pymunk_shape.body.velocity = pymunk.Vec2d(
                (150, self.players[self.controlled].pymunk_shape.body.velocity.y))

        if self.players[self.controlled].pymunk_shape.body.velocity.x < -300:
            self.players[self.controlled].pymunk_shape.body.velocity = pymunk.Vec2d(
                (-150, self.players[self.controlled].pymunk_shape.body.velocity.y))

        self.camera_shift()

        if not self.game_over:
            for i in self.floorList:
                i.update()
            for p in self.players:
                p.update()
                boxes = arcade.check_for_collision_with_list(p, self.floorList)
                if_collide = [True for pl in self.players if arcade.check_for_collision(p, pl) and pl != p]

                if (boxes != [] or True in if_collide) and abs(p.pymunk_shape.body.velocity.y) < 3:
                    p.can_jump = True

            for i in self.players:
                i.center_x = i.pymunk_shape.body.position.x
                i.center_y = i.pymunk_shape.body.position.y
                i.angle = math.degrees(i.pymunk_shape.body.angle)
                # print(i.pymunk_shape.body.angle)
                # print(i.pymunk_shape.body.rotation_vector)
            # for x, i in enumerate(self.players):
            #   if x != self.controlled:
            #     i.change_y = 0
            #     i.change_x = 0
            # for i in [self.players[self.controlled]]:
            #   i.x += i.center_x - i.og_x
            #   i.y += i.center_y - i.og_y
            #   i.center_x,i.center_y = i.og_x,i.og_y


def main():
    """ Start the game """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
