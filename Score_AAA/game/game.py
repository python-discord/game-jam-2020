from collections import deque
import arcade
from pyglet.gl import GL_NEAREST
from entities import Splash
from lane import Lane
from patterns import PatternGenerator

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class EnumGameState:
    title = 0
    game = 1
    game_over = 2


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
        self.splash_list = None

        # Set up the Lanes
        self.lane_up = None
        self.lane_middle = None
        self.lane_down = None
        self.pattern = None

        # Set up the title screen
        self.game_state = EnumGameState.title
        self.title_screen = arcade.load_texture("../ressources/title_screen.png")

        # Set up other settings
        self.score = 0
        self.time = 0
        self.frame = 0
        self.fps = 0
        self.combo = 0
        self.stage = [100000, 50000, 10000]
        self.obstacle_queue = deque([[], [], [], [], []])

    def setup(self):

        self.background = arcade.SpriteList()
        self.sky_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList(use_spatial_hash=True)
        self.obstacle_list = arcade.SpriteList()
        self.char_list = arcade.SpriteList()
        self.splash_list = arcade.SpriteList()

        # Set up lane 1
        q_run_textures = []
        for i in range(4):
            q_run_textures.append(arcade.load_texture(f"../ressources/New_Q_Run_{i+1}.png"))

        self.lane_up = Lane(1, 1.7,
                            SCREEN_HEIGHT,
                            SCREEN_WIDTH,
                            "../ressources/New_Q_Run_1.png",
                            q_run_textures,
                            {0: 0, 1: 1, 2: 2, 3: 3, 4: 2})
        self.char_list.append(self.lane_up.char)
        self.floor_list.append(self.lane_up.floor)
        for background in self.lane_up.generate_background("../ressources/Q_Background_Crayon.png", 2, 107):
            self.background.append(background)
        for sky in self.lane_up.generate_background("../ressources/Q_Sky.png", 1, 107):
            self.sky_list.append(sky)

        # Set up lane 2

        w_run_textures = []
        for i in range(3):
            w_run_textures.append(arcade.load_texture(f"../ressources/W_Run_{i+1}.png"))

        self.lane_middle = Lane(2, 1.8,
                                SCREEN_HEIGHT,
                                SCREEN_WIDTH,
                                "../ressources/W_Idle.png",
                                w_run_textures,
                                {0: 0, 1: 0, 2: 1, 3: 1, 4: 2})
        self.char_list.append(self.lane_middle.char)
        self.floor_list.append(self.lane_middle.floor)
        for background in self.lane_up.generate_background("../ressources/W_Background.png", 2,  -93):
            self.background.append(background)
        for sky in self.lane_up.generate_background("../ressources/W_Sky.png", 1, -93):
            self.sky_list.append(sky)

        # Set up lane 3

        w_run_textures = []
        for i in range(6):
            w_run_textures.append(arcade.load_texture(f"../ressources/E_Run_{i+1}.png"))

        self.lane_down = Lane(3, 1.7,
                              SCREEN_HEIGHT,
                              SCREEN_WIDTH,
                              "../ressources/E_Idle.png",
                              w_run_textures,
                              {0: 0, 1: 1, 2: 2, 3: 1, 4: 3, 5: 4, 6: 5})
        self.char_list.append(self.lane_down.char)
        self.floor_list.append(self.lane_down.floor)
        for background in self.lane_up.generate_background("../ressources/E_Sky_1.png", 3,  -300):
            self.background.append(background)
        for sky in self.lane_up.generate_background("../ressources/E_Sky_2.png", 8, -300):
            self.sky_list.append(sky)

        # Visual cue for when an input is valid
        ok_zone = arcade.Sprite("../ressources/Valid Zone.png")
        ok_zone.center_x = (SCREEN_WIDTH // 10) * 2
        ok_zone.center_y = SCREEN_HEIGHT // 2
        self.floor_list.append(ok_zone)

        # Set up the rest
        self.pattern = PatternGenerator([self.lane_up, self.lane_middle, self.lane_down])
        self.score = 0
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.time = 0
        self.fps = 0

    def draw_game(self):
        """
        Function to draw the game (on_draw)
        """

        # Draw all the sprites (order determine Z axis)
        self.sky_list.draw(filter=GL_NEAREST)
        self.background.draw(filter=GL_NEAREST)
        self.floor_list.draw()
        self.obstacle_list.draw(filter=GL_NEAREST)
        self.char_list.draw(filter=GL_NEAREST)
        self.splash_list.draw(filter=GL_NEAREST)

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 700, 550, arcade.color.BLACK, 14)
        fps = f"FPS: {self.fps}"
        arcade.draw_text(fps, 700, 565, arcade.color.BLACK, 14)
        combo = f"COMBO: {self.combo}"
        arcade.draw_text(combo, 700, 535, arcade.color.BLACK, 14)

    def draw_title_screen(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      self.title_screen.width,
                                      self.title_screen.height,
                                      self.title_screen, 0)

    def on_draw(self):
        """
        Function to render the game.
        """
        # This command has to happen before we start drawing
        arcade.start_render()

        if self.game_state == EnumGameState.title:
            self.draw_title_screen()
        elif self.game_state == EnumGameState.game:
            self.draw_game()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if self.game_state == EnumGameState.title:
            self.game_state = EnumGameState.game
            self.setup()

        elif self.game_state == 1:
            if key == arcade.key.A or key == arcade.key.Q:
                self.key_action(self.lane_up)
            elif key == arcade.key.Z or key == arcade.key.W:
                self.key_action(self.lane_middle)
            elif key == arcade.key.E:
                self.key_action(self.lane_down)

    def key_action(self, lane):
        result = lane.action(self.obstacle_list)
        splash = Splash(result.name,
                        [lane.char.center_x + 75, lane.char.center_y + 50])
        self.splash_list.append(splash)

        if result.name == "miss":
            self.combo = 0
        else:
            self.combo += 1
            self.score += result.value * self.combo

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.A or key == arcade.key.Q:
            pass
        elif key == arcade.key.Z or key == arcade.key.W:
            pass
        elif key == arcade.key.E:
            pass

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.time += delta_time
        self.frame += 1
        if self.time >= 1:
            self.fps = self.frame
            self.frame = 0
            self.time = 0

            # Generation of obstacles
            if not self.obstacle_queue:
                self.obstacle_queue.append(self.pattern.generate_pattern())
            for obstacle in self.obstacle_queue.popleft():
                self.obstacle_list.append(obstacle)

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
        self.splash_list.update()
        for item in self.splash_list:
            item.update_age(delta_time)
        # Score points and remove obstacles
        for obstacle in self.obstacle_list:
            if obstacle.center_x < 0:
                if obstacle.hit == False:
                    self.score -= 50
                    self.combo = 0
                obstacle.remove_from_sprite_lists()

        # Increase speed at each level of difficulty
        if self.stage and self.score > self.stage[-1]:
            self.lane_up.difficulty += 3
            self.lane_middle.difficulty += 3
            self.lane_down.difficulty += 3
            self.stage.pop()
def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "3 Keys on the Run")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()