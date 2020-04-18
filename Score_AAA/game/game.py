import arcade
import random
from characters import Character
from lane import Lane

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
UPDATES_PER_FRAME = 7


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.char_list = None
        self.obstacle_list = None
        self.floor_list = None
        self.background = None

        # Set up the Lanes
        self.lane_up = None
        self.lane_middle = None
        self.lane_down = None

        # Set up other settings
        self.score = 0
        self.time = 0
        self.frame = 0

    def setup(self):

        self.background = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.char_list = arcade.SpriteList()

        q_background = arcade.Sprite("../ressources/Q_Background.png")
        q_background.center_y = SCREEN_HEIGHT - (SCREEN_HEIGHT // 3) + 107
        q_background.center_x = SCREEN_WIDTH // 2
        q_background.change_x = -2
        self.background.append(q_background)

        q_background = arcade.Sprite("../ressources/Q_Background.png")
        q_background.center_y = SCREEN_HEIGHT - (SCREEN_HEIGHT // 3) + 107
        q_background.center_x = SCREEN_WIDTH + SCREEN_WIDTH // 2
        q_background.change_x = -2
        self.background.append(q_background)

        Q_run_textures = []
        for i in range(3):
            Q_run_textures.append(arcade.load_texture(f"../ressources/Q_Run_{i+1}.png"))

        # Set up lane 1
        self.lane_up = Lane(1,
                            SCREEN_HEIGHT,
                            SCREEN_WIDTH,
                            "../ressources/Q_Run_1.png",
                            Q_run_textures)
        self.char_list.append(self.lane_up.char)
        self.floor_list.append(self.lane_up.floor)

        # Set up lane 2
        self.lane_middle = Lane(2,
                                SCREEN_HEIGHT,
                                SCREEN_WIDTH,
                                "../ressources/W_tempo_char.png",
                                [])
        self.char_list.append(self.lane_middle.char)
        self.floor_list.append(self.lane_middle.floor)

        # Set up lane 3
        self.lane_down = Lane(3,
                              SCREEN_HEIGHT,
                              SCREEN_WIDTH,
                              "../ressources/E_tempo_char.png",
                              [])
        self.char_list.append(self.lane_down.char)
        self.floor_list.append(self.lane_down.floor)

        # Set up the rest
        self.score = 0
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.time = 0

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.floor_list.draw()
        self.background.draw()
        self.obstacle_list.draw()
        self.char_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 700, 550, arcade.color.BLACK, 14)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.A:
            if self.lane_up.physics_engine.can_jump(5):
                self.lane_up.physics_engine.jump(6)
        elif key == arcade.key.Z:
            if self.lane_middle.physics_engine.can_jump(5):
                self.lane_middle.physics_engine.jump(6)
        elif key == arcade.key.E:
            if self.lane_down.physics_engine.can_jump(5):
                self.lane_down.physics_engine.jump(6)

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.A:
            pass
        elif key == arcade.key.Z:
            pass
        elif key == arcade.key.E:
            pass

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Temporary level generation
        self.time += delta_time
        self.frame += 1
        if self.time >= 1:
            print(self.frame)
            self.frame = 0
            rand = random.randint(0, 10)

            if rand == 0:
                self.obstacle_list.append(self.lane_up.generate_obstacle())
            elif rand == 1:
                self.obstacle_list.append(self.lane_middle.generate_obstacle())
            elif rand == 2:
                self.obstacle_list.append(self.lane_down.generate_obstacle())
            elif rand == 3:
                self.background.append(self.lane_up.generate_tree())
            elif rand == 4:
                self.background.append(self.lane_middle.generate_tree())
            elif rand == 5:
                self.background.append(self.lane_down.generate_tree())

            self.time = 0

        # Important stuff to update
        self.lane_up.physics_engine.update()
        self.lane_middle.physics_engine.update()
        self.lane_down.physics_engine.update()

        self.floor_list.update()
        self.background.update()
        self.obstacle_list.update()
        self.char_list.update()

        # Score points and remove obstacles
        temp_list = arcade.SpriteList()
        for obstacle in self.obstacle_list:
            if obstacle.center_x < 0:
                self.score += 10
            else:
                temp_list.append(obstacle)

        self.obstacle_list = temp_list

        # Remove backgrounds item
        temp_background = arcade.SpriteList()
        for item in self.background:
            if item.right > 0:
                temp_background.append(item)
            else:
                if "Q_Background.png" in item.texture.name:
                    q_background = arcade.Sprite("../ressources/Q_Background.png")
                    q_background.center_y = SCREEN_HEIGHT - (SCREEN_HEIGHT // 3) + 107
                    q_background.center_x = SCREEN_WIDTH + SCREEN_WIDTH // 2
                    q_background.change_x = -2
                    temp_background.append(q_background)
        self.background = temp_background

        # Generate a list of all sprites that collided with the player.
        for chars in [self.lane_up.char, self.lane_middle.char, self.lane_down.char]:
            hit_list = arcade.check_for_collision_with_list(chars, self.obstacle_list)

        # Loop through each colliding sprite, remove it, and add to the score.
            if hit_list:
                # TODO to destroy the obstacle/Make it triggered once
                self.score += -50


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "3 Keys on the Run")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()