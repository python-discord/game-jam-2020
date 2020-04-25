from collections import deque
import json
import arcade
import time
from pyglet.gl import GL_NEAREST
from entities import Splash
from lane import Lane
from patterns import PatternGenerator
from score_screen import Score

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
        self.score_list = None
        self.life_list = None

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
        self.life = 5
        self.stage = [60000, 20000, 2500]
        self.music = None
        self.obstacle_queue = deque([[], [], [], [], []])
        self.score_screen = None

    def setup(self):

        self.background = arcade.SpriteList()
        self.sky_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList(use_spatial_hash=True)
        self.obstacle_list = arcade.SpriteList()
        self.char_list = arcade.SpriteList()
        self.splash_list = arcade.SpriteList()
        self.score_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()

        # Set up lane 1
        q_run_textures = []
        for i in range(4):
            q_run_textures.append(
                arcade.load_texture(f"../ressources/New_Q_Run_{i+1}.png")
            )

        self.lane_up = Lane(
            1,
            1.7,
            SCREEN_HEIGHT,
            SCREEN_WIDTH,
            "../ressources/New_Q_Run_1.png",
            q_run_textures,
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 2},
        )
        self.char_list.append(self.lane_up.char)
        self.floor_list.append(self.lane_up.floor)
        [
            self.background.append(background)
            for background in self.lane_up.generate_background(
                "../ressources/Q_Background_Crayon.png", 2, 107
            )
        ]
        [
            self.sky_list.append(sky)
            for sky in self.lane_up.generate_background(
                "../ressources/Q_Sky.png", 1, 107
            )
        ]

        # Set up lane 2
        w_run_textures = []
        for i in range(3):
            w_run_textures.append(arcade.load_texture(f"../ressources/W_Run_{i+1}.png"))

        self.lane_middle = Lane(
            2,
            1.8,
            SCREEN_HEIGHT,
            SCREEN_WIDTH,
            "../ressources/W_Idle.png",
            w_run_textures,
            {0: 0, 1: 0, 2: 1, 3: 1, 4: 2},
        )
        self.char_list.append(self.lane_middle.char)
        self.floor_list.append(self.lane_middle.floor)
        [
            self.background.append(background)
            for background in self.lane_up.generate_background(
                "../ressources/W_Background.png", 2, -93
            )
        ]
        [
            self.sky_list.append(sky)
            for sky in self.lane_up.generate_background(
                "../ressources/W_Sky.png", 1, -93
            )
        ]

        # Set up lane 3
        w_run_textures = []
        for i in range(6):
            w_run_textures.append(arcade.load_texture(f"../ressources/E_Run_{i+1}.png"))

        self.lane_down = Lane(
            3,
            1.7,
            SCREEN_HEIGHT,
            SCREEN_WIDTH,
            "../ressources/E_Idle.png",
            w_run_textures,
            {0: 0, 1: 1, 2: 2, 3: 1, 4: 3, 5: 4, 6: 5},
        )
        self.char_list.append(self.lane_down.char)
        self.floor_list.append(self.lane_down.floor)
        [
            self.background.append(background)
            for background in self.lane_up.generate_background(
                "../ressources/E_Sky_1.png", 3, -300
            )
        ]
        [
            self.sky_list.append(sky)
            for sky in self.lane_up.generate_background(
                "../ressources/E_Sky_2.png", 8, -300
            )
        ]

        # Visual cue for when an input is valid
        ok_zone = arcade.Sprite("../ressources/Valid Zone.png")
        ok_zone.center_x = (SCREEN_WIDTH // 10) * 2
        ok_zone.center_y = SCREEN_HEIGHT // 2
        self.floor_list.append(ok_zone)

        # Set up obstacle Generation
        self.pattern = PatternGenerator(
            [self.lane_up, self.lane_middle, self.lane_down]
        )
        self.obstacle_queue = deque([[], [], [], [], []])

        # Set up life system
        self.life = 5
        life_pos = [SCREEN_WIDTH// 2 + 40, SCREEN_HEIGHT - 30]
        for life_sprite in range(self.life):
            self.life_list.append(arcade.Sprite("../ressources/Life_Orb.png",
                                                center_x= life_pos[0],
                                                center_y= life_pos[1]))
            life_pos[0] += 40

        # Set up Combo and Score and difficulty
        self.score_screen = Score(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.score_list.append(arcade.Sprite("..//ressources/Score_Box.png",
                                             center_x=700,
                                             center_y=560,
                                             scale=1.2))
        self.score = 0
        self.combo = 0
        self.stage = [60000, 20000, 2500]

        # Set up Technical stuff
        self.time = 0
        self.frame = 0
        self.fps = 0
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        # Play the music
        self.music = None
        if self.music:
            self.music.stop()
        self.music = arcade.Sound(
            "../ressources/Loyalty_Freak_Music_-_04_-_It_feels_good_to_be_alive_too.mp3"
        )

    def draw_game(self):
        """
        Function to draw the game (on_draw)
        """
        arcade.start_render()

        # Draw all the sprites (order determine Z axis)
        self.sky_list.draw(filter=GL_NEAREST)
        self.background.draw(filter=GL_NEAREST)
        self.floor_list.draw()
        self.obstacle_list.draw(filter=GL_NEAREST)
        self.char_list.draw(filter=GL_NEAREST)
        self.splash_list.draw(filter=GL_NEAREST)
        self.score_list.draw(filter=GL_NEAREST)
        self.life_list.draw(filter=GL_NEAREST)
        if self.game_state == EnumGameState.game:
            # Put the text on the screen.
            output = f"{self.score}"
            arcade.draw_text(output, 693, 560, arcade.color.DARK_RED, 15)
            combo = f"{self.combo}"
            arcade.draw_text(combo, 693, 542, arcade.color.DARK_RED, 15)

            # Put the fps on the bottom left
            fps = f"FPS: {self.fps}"
            arcade.draw_text(fps, 730, 10, arcade.color.YELLOW, 14)

        elif self.game_state == EnumGameState.game_over:
            self.score_screen.draw_score_screen()
            output = f"{self.score}"
            arcade.draw_text(output, 700, 560, arcade.color.DARK_RED, 14)

    def draw_title_screen(self):
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            self.title_screen.width,
            self.title_screen.height,
            self.title_screen,
            0,
        )

    def on_draw(self):
        """
        Function to render the game.
        """
        if self.game_state == EnumGameState.title:
            self.draw_title_screen()
        elif (
            self.game_state == EnumGameState.game
            or self.game_state == EnumGameState.game_over
        ):
            self.draw_game()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if self.game_state == EnumGameState.title:
            self.game_state = EnumGameState.game
            self.setup()
            self.music.play(0.5)

        elif self.game_state == EnumGameState.game:
            if key == arcade.key.A or key == arcade.key.Q:
                self.key_action(self.lane_up)
            elif key == arcade.key.Z or key == arcade.key.W:
                self.key_action(self.lane_middle)
            elif key == arcade.key.E:
                self.key_action(self.lane_down)

        elif self.game_state == EnumGameState.game_over:
            if self.score_screen.score_input(chr(key)):
                self.setup()
                self.game_state = EnumGameState.game

    def key_action(self, lane):
        result = lane.action(self.obstacle_list)
        splash = Splash(result.name, [lane.char.center_x + 75, lane.char.center_y + 50])
        self.splash_list.append(splash)

        if result.name == "miss":
            self.combo = 0
            self.life -= 1
            self.life_list[self.life].color = (50, 50, 50)
        else:
            self.combo += 1
            self.score += result.value * self.combo

    def on_update(self, delta_time):
        """ Movement and game logic """

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

        if self.game_state == EnumGameState.game:
            self.time += delta_time
            self.frame += 1
            if self.time >= 1:
                self.fps = self.frame
                self.frame = 0
                self.time = 0

                # Generation of obstacles
                if not self.obstacle_queue:
                    result = self.pattern.generate_pattern()
                    if isinstance(result[0], list):
                        for x in result:
                                self.obstacle_queue.append(x)
                    else:
                        self.obstacle_queue.append(result)
                for obstacle in self.obstacle_queue.popleft():
                    self.obstacle_list.append(obstacle)

            for item in self.splash_list:
                item.update_age(delta_time)

            # Score points and remove obstacles
            for obstacle in self.obstacle_list:
                if obstacle.center_x < 0:
                    if obstacle.hit is False:
                        self.score -= 50
                        self.combo = 0
                        self.life -= 1
                        self.life_list[self.life].color = (50, 50, 50)
                    obstacle.remove_from_sprite_lists()

            # Increase speed at each level of difficulty
            if self.stage and self.score > self.stage[-1]:
                self.lane_up.difficulty += 3
                self.lane_middle.difficulty += 3
                self.lane_down.difficulty += 3
                self.stage.pop()

            # Launch Game Over
            if self.life <= 0:
                self.game_state = EnumGameState.game_over
                self.floor_list = arcade.SpriteList()
                self.obstacle_list = arcade.SpriteList()
                self.char_list = arcade.SpriteList()
                self.splash_list = arcade.SpriteList()
                self.life_list = arcade.SpriteList()
                self.score_screen.load_score(self.score)
                self.score_list.append(arcade.Sprite("..//ressources/Score_Ground.png",
                                                     center_x= SCREEN_WIDTH//2,
                                                     center_y= SCREEN_HEIGHT//2))


        if self.score_screen.restart_timer >= 0:
            self.score_screen.restart_timer += delta_time


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "3 Keys on the Run")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
