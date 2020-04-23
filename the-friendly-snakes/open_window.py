import arcade

# help-phosphorus
# game-development

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "3 of a kind"

CHARACTER_SCALING = 1

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 1

LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
BOTTOM_VIEWPORT_MARGIN = 128
TOP_VIEWPORT_MARGIN = 0

class Maths():

    @classmethod
    def clamp(cls, x: float, lowerlimit: float, upperlimit: float):
        if x < lowerlimit:
            x = lowerlimit
        if x > upperlimit:
            x = upperlimit
        return x

    @classmethod
    def smoothstep(cls, edge0: float, edge1: float, amount: float):
        x = Maths.clamp(amount, 0.0, 1.0)
        return x * x * (3.0 - 2.0 * x) * (edge1 - edge0)


class Player(arcade.Sprite):

    def update(self):
        pass
        # if self.left < 0:
        #     self.left = 0
        # elif self.right > SCREEN_WIDTH - 1:
        #     self.right = SCREEN_WIDTH - 1
        #
        # if self.bottom < 0:
        #     self.bottom = 0
        # elif self.top > SCREEN_HEIGHT - 1:
        #     self.top = SCREEN_HEIGHT - 1

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        self.player_list = None
        self.wall_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.old_view_bottom = 0
        self.old_view_left = 0
        self.view_bottom = 0
        self.view_left = 0
        self.smooth_view_left = 0
        self.smooth_view_bottom = 0

        self.collect_coin_sound = arcade.load_sound('sounds/coin.wav')

        arcade.set_background_color(arcade.color.VIVID_SKY_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        image_source = 'images/player_1/player_look_right.png'
        self.player_sprite = Player(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 240
        self.player_list.append(self.player_sprite)

        for x in range(0, SCREEN_WIDTH, 64):
            wall = arcade.Sprite('images/tiles/grass.png')
            wall.center_x = x
            wall.center_y = 64
            self.wall_list.append(wall)

        coords = [
            [256, 128 + 40],
            [256 * 2, 128 * 2 + 40],
            [256 * 3, 128 * 3 + 40],
            [256 * 4, 128 * 4 + 40],
        ]

        for coordinate in coords:
            wall = arcade.Sprite('images/tiles/crate.png')
            wall.position = coordinate
            self.wall_list.append(wall)

        for x in range(128, SCREEN_WIDTH, 256):
            wall = arcade.Sprite('images/tiles/crate.png')
            wall.center_x = x
            wall.center_y = 128 + 40
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()

        self.wall_list.draw()
        self.player_list.draw()


    # https://arcade.academy/examples/sprite_move_keyboard_better.html#sprite-move-keyboard-better
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                # self.up_pressed = True
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # if key == arcade.key.UP:
        #     self.up_pressed = False
        # elif key == arcade.key.DOWN:
        #     self.down_pressed = False
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False



    def on_update(self, delta_time):

        self.player_sprite.change_x = 0
        # self.player_sprite.change_y = 0

        # if self.up_pressed and not self.down_pressed:
        #     self.player_sprite.change_y = PLAYER_JUMP_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        self.physics_engine.update()
        self.player_list.update()

        changed = False
        math = Maths()

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed + True

        right_boundary = self.view_left + RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT / 2
        if self.player_sprite.top > top_boundary:
            if self.view_bottom + (self.player_sprite.top - top_boundary) > 0:
                self.view_bottom += self.player_sprite.top - top_boundary
                changed = True
            else:
                self.view_bottom = 0

        bottom_boundary = self.view_bottom + SCREEN_HEIGHT / 2
        if self.player_sprite.bottom < bottom_boundary:
            if self.view_bottom - (bottom_boundary - self.player_sprite.bottom) > 0:
                self.view_bottom -= bottom_boundary - self.player_sprite.bottom
                changed = True
            else:
                self.view_bottom = 0


        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            # arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, self.view_bottom + SCREEN_HEIGHT)
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, self.view_bottom + SCREEN_HEIGHT)

        self.old_view_left = self.view_left
        self.old_view_bottom = self.view_bottom


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()