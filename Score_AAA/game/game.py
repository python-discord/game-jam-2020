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
        self.sky_list = None

        # Set up the Lanes
        self.lane_up = None
        self.lane_middle = None
        self.lane_down = None

        # Set up other settings
        self.score = 0
        self.time = 0
        self.frame = 0
        self.fps = 0

    def setup(self):

        self.background = arcade.SpriteList()
        self.sky_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList(use_spatial_hash=True)
        self.obstacle_list = arcade.SpriteList()
        self.char_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up lane 1
        q_run_textures = []
        for i in range(4):
            q_run_textures.append(arcade.load_texture(f"../ressources/New_Q_Run_{i+1}.png"))

        self.lane_up = Lane(1,
                            SCREEN_HEIGHT,
                            SCREEN_WIDTH,
                            "../ressources/New_Q_Run_1.png",
                            q_run_textures)
        self.char_list.append(self.lane_up.char)
        self.floor_list.append(self.lane_up.floor)
        for background in self.lane_up.generate_background("../ressources/Q_Background.png", 2, 107):
            self.background.append(background)
        for sky in self.lane_up.generate_background("../ressources/Q_Sky.png", 1, 107):
            self.sky_list.append(sky)

        # Set up lane 2
        self.lane_middle = Lane(2,
                                SCREEN_HEIGHT,
                                SCREEN_WIDTH,
                                "../ressources/W_Idle.png",
                                [])
        self.char_list.append(self.lane_middle.char)
        self.floor_list.append(self.lane_middle.floor)
        for background in self.lane_up.generate_background("../ressources/W_Background.png", 2,  -93):
            self.background.append(background)

        # Set up lane 3
        self.lane_down = Lane(3,
                              SCREEN_HEIGHT,
                              SCREEN_WIDTH,
                              "../ressources/E_Idle.png",
                              [])
        self.char_list.append(self.lane_down.char)
        self.floor_list.append(self.lane_down.floor)

        # Visual cue for when an input is valid
        ok_zone = arcade.Sprite("../ressources/Valid Zone.png")
        ok_zone.center_x = (SCREEN_WIDTH // 10) * 2
        ok_zone.center_y = SCREEN_HEIGHT // 2
        self.floor_list.append(ok_zone)

        # Set up the rest
        self.score = 0
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.time = 0
        self.fps = 0

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites (order determine Z axis)
        self.sky_list.draw()
        self.background.draw()
        self.floor_list.draw()
        self.obstacle_list.draw()
        self.char_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 700, 550, arcade.color.BLACK, 14)
        fps = f"FPS: {self.fps}"
        arcade.draw_text(fps, 700, 565, arcade.color.BLACK, 14)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.A:
            if self.lane_up.action(self.obstacle_list):
                self.score += 10

        elif key == arcade.key.Z:
            if self.lane_middle.action(self.obstacle_list):
                self.score += 10

        elif key == arcade.key.E:
            if self.lane_down.action(self.obstacle_list):
                self.score += 10
        elif key == arcade.key.U:
            self.lane_down.char.scale = 15

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
            self.fps = self.frame
            self.frame = 0
            rand = random.randint(0, 10)

            if rand == 0:
                self.obstacle_list.append(self.lane_up.generate_obstacle())
            elif rand == 1:
                self.obstacle_list.append(self.lane_middle.generate_obstacle())
            elif rand == 2:
                self.obstacle_list.append(self.lane_down.generate_obstacle())

            self.time = 0

        # Update Physic Engine
        self.lane_up.physics_engine.update()
        self.lane_middle.physics_engine.update()
        self.lane_down.physics_engine.update()

        # Update Sprite_Lists
        self.floor_list.update()
        self.sky_list.update()
        self.background.update()
        self.obstacle_list.update()
        self.char_list.update()

        # Score points and remove obstacles
        for obstacle in self.obstacle_list:
            if obstacle.center_x < 0:
                self.score -= 50
                obstacle.remove_from_sprite_lists()

    # Remove backgrounds item
        for item in self.background:
            if item.right < 0:
                if "Q_Background.png" in item.texture.name:
                    item.center_x = SCREEN_WIDTH + SCREEN_WIDTH // 2
                elif "W_Background.png" in item.texture.name:
                    item.center_x = SCREEN_WIDTH + SCREEN_WIDTH // 2
                else:
                    item.remove_from_sprite_lists()

        # Handle sky

        for item in self.sky_list:
            if item.right < 0:
                if "Q_Sky.png" in item.texture.name:
                    item.center_x = SCREEN_WIDTH + SCREEN_WIDTH // 2

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "3 Keys on the Run")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()