import arcade

# help-phosphorus
# game-development

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "3 of a kind"

CHARACTER_SCALING = 1

PLAYER_MOVEMENT_SPEED = 10
PLAYER_JUMP_SPEED = 30
GRAVITY = 1.5

LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
BOTTOM_VIEWPORT_MARGIN = 128
TOP_VIEWPORT_MARGIN = 0

CAMERA_FOLLOW_SPEED = 0.2

class Maths():

    @classmethod
    def lerp(cls, v1: float, v2: float, u: float):
        return v1 + ((v2 - v1) * u)

    @classmethod
    def clamp(cls, x: float, lowerlimit: float, upperlimit: float):
        if x < lowerlimit:
            x = lowerlimit
        if x > upperlimit:
            x = upperlimit
        return x

    @classmethod
    def smoothstep(cls, edge0: float, edge1: float, x: float):
        x = Maths.clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return x * x * x * (x * (x * 6 - 15) + 10)

    @classmethod
    def lowlimit(cls, x, lowerlimit):
        if x < lowerlimit:
            x = lowerlimit
        return x

    @classmethod
    def maxlimit(cls, x, upperlimit):
        if x > upperlimit:
            x = upperlimit
        return x

# class PauseView(arcade.View)

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        self.player_list = None
        self.background_list = None
        self.wall_list = None
        self.coin_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.left_pressed = False
        self.right_pressed = False

        self.view_bottom = 0
        self.view_left = 0

        self.coin_counter = 0

        self.collect_coin_sound = arcade.load_sound('sounds/coin2.wav')
        self.jump_sound = arcade.load_sound('sounds/jump.wav')

        self.draw_shop_tip = False

        arcade.set_background_color(arcade.color.VIVID_SKY_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        self.view_bottom = 0
        self.view_left = 0

        self.coin_counter = 0

        self.draw_shop_tip = False

        image_source = 'images/player_1/player_look_right.png'
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 600
        self.player_list.append(self.player_sprite)

        map_name = 'tmx_maps/map2.tmx'
        background_layer_name = 'Background'
        platforms_layer_name = 'Platforms'
        coins_layer_name = 'Coins'

        my_map = arcade.tilemap.read_tmx(map_name)

        self.background_list = arcade.tilemap.process_layer(my_map, background_layer_name)
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name)
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name)

        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()

        self.background_list.draw()
        self.wall_list.draw()

        if self.draw_shop_tip:
            shop_tip = 'Press E to open the shop'
            arcade.draw_text(shop_tip, 50, 1350, arcade.csscolor.BLACK, 32)

        self.player_list.draw()
        self.coin_list.draw()

        coin_text = f'Coins: {self.coin_counter}'
        arcade.draw_text(coin_text, self.view_left + 10, self.view_bottom + SCREEN_HEIGHT - 50, arcade.csscolor.BLACK, 32)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = True

        if key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = False

        if key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time):

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.coin_counter += 1

        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        if self.player_sprite.left <= 600.0:
            self.draw_shop_tip = True
        else:
            self.draw_shop_tip = False

        self.view_left = int(arcade.lerp(self.view_left, self.player_sprite.center_x - SCREEN_WIDTH / 2, CAMERA_FOLLOW_SPEED))
        self.view_bottom = int(arcade.lerp(self.view_bottom, self.player_sprite.center_y - SCREEN_HEIGHT / 2, CAMERA_FOLLOW_SPEED))

        self.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom, self.view_bottom + SCREEN_HEIGHT)


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()