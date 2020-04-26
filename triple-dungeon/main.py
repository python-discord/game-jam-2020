"""
main.py
The main class used to load the game.
Holds the main game window, as well as manages basic functions for organizing the game.
"""

import collections
import math
import random
import time
from typing import Tuple, List

import arcade
from config import Config
from map import Dungeon
from mobs import Player, MobHandler
from projectiles import Temp
from recipe import ActiveRecipe


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, Config.SCREEN_TITLE)

        # Sprite Lists
        self.enemy_list = None
        self.active_enemies = []
        self.bullet_list = None
        self.player = None
        # Game Objects
        self.dungeon = None
        self.prev_keypress = []  # A list that assists with tracking keypress events
        # Used to keep track of our scrolling
        self.view_bottom = self.view_left = 0
        self.Recipe = []

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.fps = FPSCounter()
        self.bullet_list = arcade.SpriteList()

        # Create the dungeon
        self.dungeon = Dungeon(0, 3)

        # Set up recipes
        self.Recipe = ActiveRecipe()
        self.Recipe.set_ghosts()

        # Set up the player, specifically placing it at these coordinates.
        self.player = Player(self.dungeon)
        self.player.scale = 1
        level = random.choice(self.dungeon.levelList)
        self.player.center_x, self.player.center_y = level.center()
        self.player.cur_recipe = self.Recipe.active
        self.player.collisions = arcade.PhysicsEngineSimple(self.player, self.dungeon.getWalls())

        # Set up monsters
        self.Mobs = MobHandler()
        self.enemy_list = self.Mobs.setup(Config.MONSTER_COUNT, Config.MONSTER_COUNT, self.player, self.dungeon)

        # Setup viewport
        self.view_bottom = self.player.center_x - (0.5 * Config.SCREEN_WIDTH) + 300
        self.view_left = self.player.center_x - (0.5 * Config.SCREEN_WIDTH)
        arcade.set_viewport(self.view_left,
                            Config.SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            Config.SCREEN_HEIGHT + self.view_bottom)

    def on_draw(self):
        """ Render the screen. """
        try:
            # Clear the screen to the background color
            arcade.start_render()

            # Draw our sprites
            self.dungeon.render()
            self.Mobs.render()
            #self.active_enemies.draw()
            self.bullet_list.draw()
            self.Recipe.render()

            # Draw stats
            arcade.draw_text("Health:"+str(self.player.health)+"/"+str(self.player.max_health), self.view_left+100, self.view_bottom+60, arcade.color.RED, 15, font_name='Arial')
            arcade.draw_text("Armor:"+str(self.player.armor), self.view_left+100, self.view_bottom+90, arcade.color.BLUE, 15, font_name='Arial')
            arcade.draw_text("Speed:"+str(self.player.speed), self.view_left+100, self.view_bottom+120, arcade.color.YELLOW, 15, font_name='Arial')
            
            if Config.DEBUG:
                x, y = self.player.position
                arcade.draw_rectangle_outline(round(x / Config.TILE_SIZE) * Config.TILE_SIZE,
                                              round(y / Config.TILE_SIZE) * Config.TILE_SIZE,
                                              Config.TILE_SIZE, Config.TILE_SIZE, arcade.color.RED)
                self.player.draw_hit_box()
                arcade.draw_text(str((x, y)), x - 40, y + 50, arcade.color.WHITE, 15, font_name='Arial')
                arcade.draw_text(f"FPS: {self.fps.get_fps():3.0f}", self.view_left + 50, self.view_bottom + 30,
                                arcade.color.WHITE, 16, font_name='Arial')

                # Draw paths for all mobs
                for mob in self.active_enemies:
                    if mob.target is not None:
                        t1 = time.time()
                        path = mob.get_path()
                        t2 = time.time()
                        print(f'Path acquired in {round(t2 - t1, 4)}s')
                        self.draw_path(path)
                        mob.tick(path)

                self.fps.tick()
        except Exception:
            import traceback
            traceback.print_exc()

    @staticmethod
    def draw_path(path: List[Tuple[int, int]]) -> None:
        """
        Draws a line between positions in a list of tuple, also known as the path.
        :param path: A list of tuple positions defining a path that can be traversed.
        """

        if len(path) > 2:
            path = map(lambda point: ((point[0]) * Config.TILE_SIZE, (point[1]) * Config.TILE_SIZE), path)
            path = list(path)
            for pos1, pos2 in zip(path, path[1:]):
                arcade.draw_line(*pos1, *pos2, color=arcade.color.RED)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = self.player.speed
            self.prev_keypress.append(key)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -self.player.speed
            self.prev_keypress.append(key)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -self.player.speed
            self.prev_keypress.append(key)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = self.player.speed
            self.prev_keypress.append(key)
        elif key == 65307:
            self.close()
        elif key == 65505:
            self.Recipe.next_recipe()
            self.player.cur_recipe = self.Recipe.active

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
            self.prev_keypress.remove(key)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
            self.prev_keypress.remove(key)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
            self.prev_keypress.remove(key)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0
            self.prev_keypress.remove(key)

        if self.prev_keypress:
            self.on_key_press(self.prev_keypress.pop(0), 0)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse is clicked.
        """

        # Create a bullet TEMP SPRITE, currently wielding frog slingshot
        bullet = Temp()
        # Position the bullet at the player's current location
        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        dest_x = x + self.view_left
        dest_y = y + self.view_bottom

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying sideways.
        bullet.angle = math.degrees(angle)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * bullet.speed
        bullet.change_y = math.sin(angle) * bullet.speed

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        """ Movement and game logic """

        if len(self.enemy_list) == 0 and len(self.active_enemies)==0:
        	self.setup()

        # Update Mobs
        self.Mobs.update()

        # scroll screen
        self.scroll_screen()

        # Projectile updates
        self.bullet_list.update()
        for bullet in self.bullet_list:

            # Collision Checks
            hit_list = arcade.check_for_collision_with_list(bullet, self.dungeon.getWalls())
            enemy_hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            if len(enemy_hit_list):
                boon = self.Recipe.add_kill(enemy_hit_list[0].monster_type)
                if boon >= 0:
                    getattr(self.player, Config.BOON_LIST[boon])();
                enemy_hit_list[0].remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

            # If the bullet flies off-screen, remove it. TEMP change to range calc
            if (
                    bullet.bottom < self.view_bottom or
                    bullet.top > self.view_bottom + Config.SCREEN_HEIGHT or
                    bullet.right > self.view_left + Config.SCREEN_WIDTH or
                    bullet.left < self.view_left
            ):
                bullet.remove_from_sprite_lists()

    def scroll_screen(self):
        # Below manages all scrolling mechanics

        changed = False  # Track if we need to change the viewport
        # Scroll left
        left_boundary = self.view_left + Config.LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True
        # Scroll right
        right_boundary = self.view_left + Config.SCREEN_WIDTH - Config.RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True
        # Scroll up
        top_boundary = self.view_bottom + Config.SCREEN_HEIGHT - Config.TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True
        # Scroll down
        bottom_boundary = self.view_bottom + Config.BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                Config.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                Config.SCREEN_HEIGHT + self.view_bottom)

def main() -> None:
    """
    Setups up window classes and runs the game.
    """

    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
