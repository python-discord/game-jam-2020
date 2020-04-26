"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import random
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "TRI GEM DEFENCE"

SPRITE_SIZE = 128
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 15
SOCIAL_DISTANCE = 80     # how many pixels the sprites will stay away from each other before starting to follow.
PROJECTILE_SPEED = 10

# Scaling
SPRITE_SCALING = 1


# View Point Margins
LEFT_VIEWPORT_MARGIN = 400
RIGHT_VIEWPORT_MARGIN = 400
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100
PLAYER_START_X = 30
PLAYER_START_Y = 500
TEXTURE_LEFT = 1
TEXTURE_RIGHT = 0
ENEMY_SPAWN_LOCATION_LEFT = [-1700, 150]
ENEMY_SPAWN_LOCATION_RIGHT = [1700, 150]

class Player(arcade.Sprite):
    def __init__(self, path, wall, ladder):
        super().__init__()

        self.textures = []
        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        texture = arcade.load_texture(path)
        self.textures.append(texture)
        texture = arcade.load_texture(path, mirrored=True)
        self.textures.append(texture)

        self.scale = SPRITE_SCALING

        # By default, face right.
        self.set_texture(TEXTURE_RIGHT)

        # Set health
        self.health = 100

        # Set up cooldowns
        self.attack_cooldown = 0.0

        # physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self,
                                                        wall,
                                                        GRAVITY,
                                                        ladders=ladder)


    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]




        # timers / cooldowns





class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        arcade.set_background_color(arcade.color.LIGHT_SLATE_GRAY)

        # where the lists for all the sprites go should be set to none
        self.player_list = None
        self.wall_list = None
        self.enemy_list = None
        self.background_list = None
        self.ladder_list = None
        self.projectile_list = None

        # Keeps Track of physics such as gravity
        #self.physics_engine = None

        # Scrolling
        self.view_bottom = 0
        self.view_left = 0

        # keep track of score
        self.score = 0


        # timers / cooldowns
        self.cooldown = None
        self.enemy_spawn_cooldown = None

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        super().on_resize(width, height)


    def setup(self):

        self.game_over = False
        self.view_bottom = 0
        self.view_left = 0

        # keep track of score
        self.score = 0

        # create sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.ladder_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()


        # -----     Map creation     ----- #
        # create the floor
        # loop to place sprite over and over
        distance = SCREEN_WIDTH
        hight = 337
        for x in range(-1800, 1800, 128):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        for x in range(3):
            for x in range(int(distance) * -1, int(distance), 128):
                wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
                wall.center_x = x
                wall.center_y = int(hight)
                self.wall_list.append(wall)

            distance -= 400
            hight += 300


        # Ladder Positions
        ladder_pos_x = [0, -900, 900, -450, 450, 0]
        ladder_pos_y = [160, 160, 160, 465, 465, 765]

        # create Ladders
        for i in range(6):
            for y in range(ladder_pos_y[i], ladder_pos_y[i] + 200, 96):
                ladder = arcade.Sprite(":resources:images/items/ladderMid.png")
                ladder.center_x = ladder_pos_x[i]
                ladder.center_y = y
                self.ladder_list.append(ladder)

        # create an opening for the ladders though the floor
        for ladder in self.ladder_list:
            hit_list = arcade.check_for_collision_with_list(ladder,
                                                            self.wall_list)
            if len(hit_list) > 0:
                for i in hit_list:
                    wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
                    wall.center_x = ladder.center_x - ladder.width
                    wall.center_y = i.center_y
                    self.wall_list.append(wall)
                    wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
                    wall.center_x = ladder.center_x + ladder.width
                    wall.center_y = i.center_y
                    self.wall_list.append(wall)
                    i.remove_from_sprite_lists()

        # create the players
        # warrior
        self.warrior_sprite = Player(":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk0.png", self.wall_list, self.ladder_list)
        self.warrior_sprite.center_x = 50
        self.warrior_sprite.center_y = 200
        self.player_list.append(self.warrior_sprite)
        # archer
        self.archer_sprite = Player(":resources:images/animated_characters/robot/robot_idle.png", self.wall_list, self.ladder_list)
        self.archer_sprite.center_x = 50
        self.archer_sprite.center_y = 200
        self.player_list.append(self.archer_sprite)
        # wizard
        self.wizard_sprite = Player(":resources:images/animated_characters/male_person/malePerson_walk0.png", self.wall_list, self.ladder_list)
        self.wizard_sprite.center_x = 50
        self.wizard_sprite.center_y = 200
        self.player_list.append(self.wizard_sprite)

        # Create Gem
        gem = arcade.Sprite(":resources:images/items/gemRed.png", 1)
        gem.center_x = 0
        gem.center_y = 1150
        self.wall_list.append(gem)

        # Create the physics engine
        self.warrior_physics_engine = arcade.PhysicsEnginePlatformer(self.warrior_sprite,
                                                                     self.wall_list,
                                                                     GRAVITY,
                                                                     ladders=self.ladder_list)
        self.archer_physics_engine = arcade.PhysicsEnginePlatformer(self.archer_sprite,
                                                                    self.wall_list,
                                                                    GRAVITY,
                                                                    ladders=self.ladder_list)
        self.wizard_physics_engine = arcade.PhysicsEnginePlatformer(self.wizard_sprite,
                                                                    self.wall_list,
                                                                    GRAVITY,
                                                                    ladders=self.ladder_list)
        # Sets the controled / active player.
        self.active_sprite = self.warrior_sprite
        self.active_sprite_physics_engine = self.warrior_physics_engine

        # timers / cooldowns
        self.cooldown = 0.0
        self.enemy_spawn_cooldown = 0.0



    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Place the visual of all the sprites

        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.ladder_list.draw()
        self.projectile_list.draw()

        # Draw the score on the screen scrolling it with the view port
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)


    def on_update(self, delta_time):
        # This will repeatedly update
        if not self.game_over:
            self.enemy_list.update()
            self.projectile_list.update()


            for enemy in self.enemy_list:
                if enemy.center_x > 0:
                    enemy.change_x = -2
                elif enemy.center_x < 0:
                    enemy.change_x = 2

                if enemy.center_y < 1150:
                    if enemy.physics_engine.is_on_ladder():
                        enemy.change_y = PLAYER_JUMP_SPEED / 4
                    if not enemy.physics_engine.is_on_ladder():
                        enemy.change_y = 0


            # update player(s)
            self.player_list.update()
            for i in self.player_list:
                if i != self.active_sprite:
                        if i.position[0] > self.active_sprite.position[0] + SOCIAL_DISTANCE:
                            i.change_x = random.randint(-7, -1)
                        elif i.position[0] < self.active_sprite.position[0] - SOCIAL_DISTANCE:
                            i.change_x = random.randint(1, 7)
                        elif i.position[0] < self.active_sprite.position[0] + SOCIAL_DISTANCE or i.position[0] > self.active_sprite.position[0] - SOCIAL_DISTANCE:
                            i.change_x = 0

                        if i.position[1] < self.active_sprite.position[1]:
                            if i.physics_engine.is_on_ladder():
                                i.change_y = PLAYER_JUMP_SPEED / 2

                        elif i.position[1] > self.active_sprite.position[1]:
                            i.change_y = -PLAYER_JUMP_SPEED / 2


            self.warrior_physics_engine.update()
            self.archer_physics_engine.update()
            self.wizard_physics_engine.update()





            # See if an enemy has been hit.
            for enemy in self.enemy_list:
                hit_list = arcade.check_for_collision_with_list(enemy,
                                                                     self.projectile_list)
                if len(hit_list) > 0:
                    enemy.health -= 100

                for projectile in hit_list:
                    projectile.remove_from_sprite_lists()

             # See if enemy or play died.
            for sprite in self.enemy_list:
                if sprite.health <= 0:
                    sprite.remove_from_sprite_lists()
                    self.score += 1
            for sprite in self.player_list:
                if sprite.health <= 0:
                    sprite.remove_from_sprite_lists()


            # See if the player hit a enemy. If so, lose heath
            for i in self.player_list:
                hit_list = arcade.check_for_collision_with_list(i, self.enemy_list)
                for i in hit_list:
                    if hit_list[0].attack_cooldown > 3:
                        i.health -= random.randint(1, 5)
                        hit_list[0].attack_cooldown = 0.0


            #update timers
            self.cooldown += delta_time
            self.enemy_spawn_cooldown += delta_time
            for i in self.enemy_list:
                i.attack_cooldown += delta_time
            for i in self.player_list:
                i.attack_cooldown += delta_time


            # enemy spawning
            # Zombie
            if self.enemy_spawn_cooldown > 5:
                zombie = Player(":resources:images/animated_characters/zombie/zombie_idle.png", self.wall_list, self.ladder_list)
                if random.randint(0, 1) == 0:
                    zombie.center_x = ENEMY_SPAWN_LOCATION_LEFT[0]
                    zombie.center_y = ENEMY_SPAWN_LOCATION_LEFT[1]
                else:
                    zombie.center_x = ENEMY_SPAWN_LOCATION_RIGHT[0]
                    zombie.center_y = ENEMY_SPAWN_LOCATION_RIGHT[1]

                # Set boundaries on the left/right the enemy can't cross
                zombie.change_x = 2
                self.enemy_list.append(zombie)
                self.enemy_spawn_cooldown = 0.0

            for enemy in self.enemy_list:
                if enemy.collides_with_point((0, 1050)):
                    end_game = f"Score: {self.score} \n You Died \n Wait 10 Seconds To Play Again"
                    arcade.draw_text(end_game, 10 + self.view_left, 10 + self.view_bottom,
                                     arcade.csscolor.WHITE, 18)
                    arcade.pause(10)
                    MyGame.setup()

            # --- Manage Scrolling ---

            # Track if we need to change the viewpoint

            changed_viewport = False

            # Did the player fall off the map?
            for i in self.player_list:
                if i.center_y < -100:
                    i.center_x = PLAYER_START_X
                    i.center_y = PLAYER_START_Y

                # set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed_viewport = True
                #arcade.play_sound(self.game_over)

            # scroll left
            left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
            if self.active_sprite.left < left_boundary:
                self.view_left -= left_boundary - self.active_sprite.left
                changed_viewport = True

            # Scroll right
            right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
            if self.active_sprite.right > right_boundary:
                self.view_left += self.active_sprite.right - right_boundary
                changed_viewport = True

            # Scroll up
            top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
            if self.active_sprite.top > top_boundary:
                self.view_bottom += self.active_sprite.top - top_boundary
                changed_viewport = True

            # Scroll down
            bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
            if self.active_sprite.bottom < bottom_boundary:
                self.view_bottom -= bottom_boundary - self.active_sprite.bottom
                changed_viewport = True

            if changed_viewport:
                # Only scroll to integers. Otherwise we end up with pixels that
                # don't line up on the screen
                self.view_bottom = int(self.view_bottom)
                self.view_left = int(self.view_left)

                # Do the scrolling
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom)


    def on_key_press(self, key, key_modifiers):
        # called when a key is pressed

        if key == arcade.key.UP or key == arcade.key.W:
            if self.active_sprite_physics_engine.can_jump():
                self.active_sprite.change_y = PLAYER_JUMP_SPEED
            if self.active_sprite_physics_engine.is_on_ladder():
                self.active_sprite.change_y = PLAYER_JUMP_SPEED / 2
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.active_sprite.change_y = -3 * PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.active_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.active_sprite.change_x = PLAYER_MOVEMENT_SPEED


        # Change the charecter in control
        elif key == arcade.key.SPACE:
            if self.active_sprite == self.warrior_sprite:
                self.active_sprite = self.archer_sprite
                self.active_sprite_physics_engine = self.archer_physics_engine
            elif self.active_sprite == self.archer_sprite:
                self.active_sprite = self.wizard_sprite
                self.active_sprite_physics_engine = self.wizard_physics_engine
            elif self.active_sprite == self.wizard_sprite:
                self.active_sprite = self.warrior_sprite
                self.active_sprite_physics_engine = self.warrior_physics_engine

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            for i in self.player_list:
                i.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            for i in self.player_list:
                i.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.W:
            self.active_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.active_sprite.change_y = 0


    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.active_sprite == self.archer_sprite:
            if self.archer_sprite.attack_cooldown > 5:
                # Create a bullet
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 1)

                # Position the bullet at the player's current location
                start_x = self.active_sprite.center_x
                start_y = self.active_sprite.center_y
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Get from the mouse the destination location for the bullet
                # IMPORTANT! If you have a scrolling screen, you will also need
                # to add in self.view_bottom and self.view_left.
                dest_x = x + self.view_left
                dest_y = y + self.view_bottom


                # Do math to calculate how to get the bullet to the destination.
                # Calculation the angle in radians between the start points
                # and end points. This is the angle the bullet will travel.
                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                # Angle the bullet sprite so it doesn't look like it is flying
                # sideways.
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * PROJECTILE_SPEED
                bullet.change_y = math.sin(angle) * PROJECTILE_SPEED

                # Add the bullet to the appropriate lists
                self.projectile_list.append(bullet)

                # Reset timer
                self.cooldown = 0.0

        elif self.active_sprite == self.warrior_sprite:
            if self.warrior_sprite.attack_cooldown > 0.5:
                for enemy in self.enemy_list:
                    if self.warrior_sprite.center_x < abs(enemy.center_x - 150):
                        if self.warrior_sprite.center_y < abs(enemy.center_y - 100):
                            if enemy.collides_with_point((x + self.view_left, y + self.view_bottom)):
                                enemy.health -= random.randint(15, 40)
                                self.warrior_sprite.attack_cooldown = 0.0
                                break
        elif self.active_sprite == self.wizard_sprite:
            if self.wizard_sprite.attack_cooldown > 10:
                for enemy in self.enemy_list:
                    if self.wizard_sprite.center_x < abs(enemy.center_x - 340):
                        if self.wizard_sprite.center_y < abs(enemy.center_y - 250):
                            if enemy.collides_with_point((x + self.view_left, y + self.view_bottom)):
                                enemy.health -= random.randint(75, 100)
                                self.wizard_sprite.attack_cooldown = 0.0



    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
