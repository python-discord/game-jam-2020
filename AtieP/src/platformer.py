import arcade
import pyglet.gl as gl

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 150

class CoinCollectorMain(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Coin Collector by Atie")

    def setup(self):

        # setting up the graphical things
        self.ground = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.coin_bronze_list = arcade.SpriteList()
        self.coin_silver_list = arcade.SpriteList()
        self.coin_gold_list = arcade.SpriteList()
        self.spikes_list = arcade.SpriteList()
        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

        # loading the map
        tilemap = arcade.tilemap.read_tmx("assets/map.tmx")

        # load the ground from the map
        self.ground = arcade.tilemap.process_layer(tilemap, "Ground", 2)

        # load the coins from the map
        self.coin_bronze_list = arcade.tilemap.process_layer(tilemap, "CoinBronze", 2)
        self.coin_silver_list = arcade.tilemap.process_layer(tilemap, "CoinSilver", 2)
        self.coin_gold_list = arcade.tilemap.process_layer(tilemap, "CoinGold", 2)

        # load the spikes from the map
        self.spikes_list = arcade.tilemap.process_layer(tilemap, "Spikes", 2)

        # the player sprite
        self.player = arcade.Sprite("assets/player_right.png", 1)
        self.player.position = [100, 130]
        self.player_list.append(self.player)

        # necessary for the scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.ground, 1)

    def on_update(self, delta):

        self.physics_engine.update()

        # check if the player touched the spikes
        # this function return an empty list if the player doesn't touch the spikes
        spike_touch_list = arcade.check_for_collision_with_list(self.player, self.spikes_list)
        for i in spike_touch_list:
            self.setup()

        # change viewport depending of where's the player sprite
        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw(filter=gl.GL_NEAREST)
        self.ground.draw(filter=gl.GL_NEAREST)
        self.spikes_list.draw(filter=gl.GL_NEAREST)

        # draw coins
        self.coin_bronze_list.draw(filter=gl.GL_NEAREST)
        self.coin_silver_list.draw(filter=gl.GL_NEAREST)
        self.coin_gold_list.draw(filter=gl.GL_NEAREST)
        arcade.set_background_color(arcade.csscolor.LIGHT_CYAN)

    def on_key_press(self, key, modifier):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -10
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 10
        elif key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = 20
                arcade.play_sound(arcade.load_sound("assets/jump.wav"))

    def on_key_release(self, key, modifier):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

def platformer_main():
    app = CoinCollectorMain()
    app.setup()
    arcade.run()