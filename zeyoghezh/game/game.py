import random
import arcade
import logging
from arcade.gui import Theme, TextButton
from .util import get_distance, log_exceptions
from .planet import Planet
from .config import (
    SCREEN_SIZE, SCREEN_TITLE, ALL_PLANETS, BACKGROUND_IMAGE, BACKGROUND_MUSIC,
    BACKGROUND_MUSIC_VOLUME
)
import sys


LOGGING_FORMAT = ("%(asctime)-15s %(levelname)s in %(funcName)s "
                  "at %(pathname)s:%(lineno)d: %(message)s")
logging.basicConfig(
    stream=sys.stderr, level=logging.INFO, format=LOGGING_FORMAT)

logger = logging.getLogger()


def get_new_lithium_location():
    return (
        random.randint(int(SCREEN_SIZE[0]/6), int(9*SCREEN_SIZE[0]/10)),
        random.randint(int(SCREEN_SIZE[1]/10), int(9*SCREEN_SIZE[1]/10)),
    )


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_SIZE[0], SCREEN_SIZE[1], SCREEN_TITLE)
        self.planets = arcade.SpriteList()
        self.lithium_location = get_new_lithium_location()
        self.lithium_count = 0
        self.lithium_score_location = (SCREEN_SIZE[0]/3, SCREEN_SIZE[1]/20)
        self.theme = None
        self.background = None
        self.background_music = None

        self.abscond_button = None

        self.game_is_over = False
        self.game_over_reason = None
        self.game_over_location = (SCREEN_SIZE[0]/10, SCREEN_SIZE[1]/2)

    def setup(self):
        self.background = arcade.load_texture(
            BACKGROUND_IMAGE)
        self.background_music = arcade.Sound(BACKGROUND_MUSIC, streaming=True)
        self.background_music.play(BACKGROUND_MUSIC_VOLUME)
        planets = [Planet(planet_name) for planet_name in ALL_PLANETS]
        self.setup_theme()
        self.abscond_button = TextButton(
            SCREEN_SIZE[0]/6, SCREEN_SIZE[1]/15, 200, 50,
            "Abscond", theme=self.theme)
        self.abscond_button.on_press = self.abscond_press
        self.abscond_button.on_release = self.abscond_release
        self.button_list.append(self.abscond_button)
        for planet in planets:
            self.planets.append(planet)
            others = [other for other in planets if other != planet]
            planet.setup(
                parent=self,
                others=others,
                center_x=random.random()*SCREEN_SIZE[0],
                center_y=random.random()*SCREEN_SIZE[1],
                start_speed_x=random.random(),
                start_speed_y=random.random()
            )

    def abscond_press(self):
        self.abscond_button.pressed = True

    def abscond_release(self):
        if self.abscond_button.pressed:
            self.abscond_button.pressed = False
            self.game_over(f"Absconded with {self.lithium_count:.2f} lithium!")

    def set_button_textures(self):
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.WHITE)
        self.set_button_textures()

    @log_exceptions
    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1], self.background)
        super().on_draw()
        for planet in self.planets:
            for other in planet.attacked_last_round:
                arcade.draw_line(
                    start_x=planet.center_x, start_y=planet.center_y,
                    end_x=(
                        other.center_x+(
                            random.random()*other.width/4)
                        - (other.width/4)),
                    end_y=(
                        other.center_y+(
                            random.random()*other.height/4)
                        - (other.height/4)),
                    color=planet.color,
                    line_width=planet.base_damage * 1e4)
            planet.attacked_last_round = []
            planet.pushed_last_round = []

            if planet.is_triangulating:
                planet.draw_triangulation_circle()
        self.planets.draw()
        lithium_count_text = f"Lithium count: {self.lithium_count:.2f}"
        arcade.draw_text(
            f"{lithium_count_text}", *self.lithium_score_location,
            color=arcade.color.WHITE, font_size=24)

        self.abscond_button.draw()

        if self.game_is_over:
            arcade.draw_text(
                f"Game over! {self.game_over_reason}",
                *self.game_over_location,
                color=arcade.color.WHITE, font_size=24)

    @log_exceptions
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_is_over:
            return
        if get_distance(x, y, *self.lithium_location) < 10:
            self.clicked_lithium()
        for planet in self.planets:
            if self.lithium_count >= 1 and planet.collides_with_point((x, y)):
                logger.info(f"Healing {planet.name}")
                self.lithium_count -= 1
                planet.get_healed(0.1)
        self.abscond_button.check_mouse_press(x, y)

    def clicked_lithium(self):
        planet_avg_health = self.avg_planet_health()
        self.lithium_count += planet_avg_health * 1.5
        self.lithium_location = get_new_lithium_location()

    def avg_planet_health(self):
        return (
            sum([planet.health for planet in self.planets]) / len(self.planets)
        )

    def on_update(self, delta_time):
        logger.debug("\nNew Round\n")
        self.run_assertions()
        self.planets.update()
        [planet.move() for planet in self.planets]
        [planet.try_attack_others() for planet in self.planets]
        [planet.try_push_others() for planet in self.planets]
        [planet.update_triangulating() for planet in self.planets]

    def run_assertions(self):
        assert len(self.planets) in (1, 2, 3)
        if not self.game_is_over:
            assert len(self.planets) == 3
        assert self.lithium_count >= 0
        for planet in self.planets:
            if self.game_is_over:
                assert len(planet.others) in (0, 1)
            else:
                assert len(planet.others) == 2
            assert planet.center_x > -SCREEN_SIZE[0]
            assert planet.center_x < SCREEN_SIZE[0] * 2
            assert planet.center_y > -SCREEN_SIZE[1]
            assert planet.center_y < SCREEN_SIZE[1] * 2
            assert planet.speed_x != 0
            assert planet.speed_y != 0

    def game_over(self, reason):
        if self.game_is_over:
            return
        self.game_over_reason = reason
        logger.info(f"Game over! {reason}")
        for planet in self.planets:
            logger.info(planet.get_stats_str())
        self.game_is_over = True


def main():
    window = Game()
    window.setup()
    arcade.run()
