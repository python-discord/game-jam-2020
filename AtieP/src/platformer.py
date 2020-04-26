import arcade
import pyglet.gl as gl

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 150

class CoinCollectorMain(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Coin Collector by Atie", True)

        self.deaths = 0
        self.restarts = 0


    def setup(self):

        # some "constants"
        self.SPRITE_SPEED = 10
        self.JUMP_SPEED = 20
        self.GRAVITY = 1

        # setting up the graphical things
        self.ground = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.coin_bronze_list = arcade.SpriteList()
        self.coin_silver_list = arcade.SpriteList()
        self.coin_gold_list = arcade.SpriteList()
        self.spikes_list = arcade.SpriteList()
        self.ladders_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.speed_list = arcade.SpriteList()
        self.end_list = arcade.SpriteList()
        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

        # score
        self.score = 0

        # loading the map
        tilemap = arcade.tilemap.read_tmx("assets/map.tmx")

        # load the ground from the map
        self.ground = arcade.tilemap.process_layer(tilemap, "Ground", 2)

        # load the stairs
        self.ladders_list = arcade.tilemap.process_layer(tilemap, "Ladders", 2)

        # load the background tiles
        self.background_list = arcade.tilemap.process_layer(tilemap, "Background", 2)

        # load the coins from the map
        self.coin_bronze_list = arcade.tilemap.process_layer(tilemap, "CoinBronze", 2)
        self.coin_silver_list = arcade.tilemap.process_layer(tilemap, "CoinSilver", 2)
        self.coin_gold_list = arcade.tilemap.process_layer(tilemap, "CoinGold", 2)

        # the speed bonus
        self.speed_list = arcade.tilemap.process_layer(tilemap, "Speed", 2)

        # load the spikes from the map
        self.spikes_list = arcade.tilemap.process_layer(tilemap, "Spikes", 2)

        # and the end flag
        self.end_list = arcade.tilemap.process_layer(tilemap, "End", 2)

        # the player sprite
        self.player = arcade.Sprite("assets/player_right.png", 1)
        self.player.position = [250, 1000]
        self.player_list.append(self.player)

        # necessary for the scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.end_flag = False

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.ground, self.GRAVITY, self.ladders_list)


    def on_draw(self):
        arcade.start_render()

        # background
        arcade.set_background_color(arcade.csscolor.LIGHT_CYAN)

        # draw the tiles
        self.background_list.draw(filter=gl.GL_NEAREST)
        self.player_list.draw(filter=gl.GL_NEAREST)
        self.ground.draw(filter=gl.GL_NEAREST)
        self.spikes_list.draw(filter=gl.GL_NEAREST)
        self.ladders_list.draw(filter=gl.GL_NEAREST)
        self.end_list.draw(filter=gl.GL_NEAREST)

        # draw the speed bonus
        self.speed_list.draw(filter=gl.GL_NEAREST)

        # draw coins
        self.coin_bronze_list.draw(filter=gl.GL_NEAREST)
        self.coin_silver_list.draw(filter=gl.GL_NEAREST)
        self.coin_gold_list.draw(filter=gl.GL_NEAREST)
        
        arcade.draw_text("Score: " + str(int(self.score)), self.view_left + 5, self.view_bottom + 5, arcade.csscolor.BLACK, 14)
        arcade.draw_text("Deaths: " + str(int(self.deaths)), self.view_left + 5, self.view_bottom + 20, arcade.csscolor.BLACK, 14)
        arcade.draw_text("Restarts: " + str(int(self.restarts)), self.view_left + 5, self.view_bottom + 35, arcade.csscolor.BLACK, 14)
        arcade.draw_text("Made by Atie", self.view_left + SCREEN_WIDTH / 2 - 100, self.view_bottom + 1040, arcade.csscolor.BLACK, 30)

        if self.end_flag:
            arcade.draw_text("You finished Coin Collector! Congratulations!", self.view_left + SCREEN_WIDTH / 2 - 220, self.view_bottom + 1000, arcade.csscolor.BLACK, 20)

    def on_update(self, delta):

        self.physics_engine.update()

        # check if the player touched the spikes
        # this function return an empty list if the player doesn't touch the spikes
        spike_touch_list = arcade.check_for_collision_with_list(self.player, self.spikes_list)
        for i in spike_touch_list:
            arcade.play_sound(arcade.load_sound("assets/died.wav"))
            self.deaths += 1
            self.setup()
            break

        # check if player touched the end flag
        end_touch_list = arcade.check_for_collision_with_list(self.player, self.end_list)
        for i in end_touch_list:
            i.remove_from_sprite_lists()
            arcade.play_sound(arcade.load_sound("assets/end.wav"))
            self.end_flag = True
            self.player.position = [250, 1000]
            

        # check for speed
        speed_touch_list = arcade.check_for_collision_with_list(self.player, self.speed_list)
        for i in speed_touch_list:
            self.SPRITE_SPEED += 5
            self.JUMP_SPEED += 3
            arcade.play_sound(arcade.load_sound("assets/speed.wav"))
            i.remove_from_sprite_lists()

        # check for coins
        # gold
        gold_coin_touch_list = arcade.check_for_collision_with_list(self.player, self.coin_gold_list)
        for i in gold_coin_touch_list:
            self.score += 20
            i.remove_from_sprite_lists()
            arcade.play_sound(arcade.load_sound("assets/coin_sound.wav"))

        # silver
        silver_coin_touch_list = arcade.check_for_collision_with_list(self.player, self.coin_silver_list)
        for i in silver_coin_touch_list:
            self.score += 10
            i.remove_from_sprite_lists()
            arcade.play_sound(arcade.load_sound("assets/coin_sound.wav"))

        # bronze
        bronze_coin_touch_list = arcade.check_for_collision_with_list(self.player, self.coin_bronze_list)
        for i in bronze_coin_touch_list:
            self.score += 5
            i.remove_from_sprite_lists()
            arcade.play_sound(arcade.load_sound("assets/coin_sound.wav"))

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




    def on_key_press(self, key, modifier):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -self.SPRITE_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = self.SPRITE_SPEED
        elif key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = self.JUMP_SPEED
                arcade.play_sound(arcade.load_sound("assets/jump.wav"))
        elif key == arcade.key.ESCAPE:
            quit()
        elif key == arcade.key.DELETE:
            self.restarts += 1
            self.setup()

    def on_key_release(self, key, modifier):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0





def platformer_main():
    app = CoinCollectorMain()
    app.setup()
    arcade.run()