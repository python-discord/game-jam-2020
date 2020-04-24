import random
import arcade
import logging
import itertools
import time
from arcade.gui import Theme, TextButton
from .util import (
    get_distance, log_exceptions, get_attack_triangle_points,
    random_location_in_planet
)
from .planet import Planet
from .config import (
    SCREEN_SIZE, SCREEN_TITLE, ALL_PLANETS, BACKGROUND_IMAGE, BACKGROUND_MUSIC,
    BACKGROUND_MUSIC_VOLUME, STORY_LINES, LITHIUM_MULTIPLIER,
    BASE_TIME_MULTIPLIER, VOLUME_IMAGE, VOLUME_MOVER_IMAGE
)
import sys


LOGGING_FORMAT = ("%(asctime)-15s %(levelname)s in %(funcName)s "
                  "at %(pathname)s:%(lineno)d: %(message)s")
logging.basicConfig(
    stream=sys.stderr, level=logging.INFO, format=LOGGING_FORMAT)

logger = logging.getLogger()


def get_new_lithium_location():
    return (
        random.randint(int(SCREEN_SIZE[0]/10), int(9*SCREEN_SIZE[0]/10)),
        random.randint(int(SCREEN_SIZE[1]/8), int(9*SCREEN_SIZE[1]/10)),
    )


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_SIZE[0], SCREEN_SIZE[1], SCREEN_TITLE)
        self.planets = None
        self.lithium_location = get_new_lithium_location()
        self.lithium_count = 0
        self.lithium_score_location = (SCREEN_SIZE[0]/3, SCREEN_SIZE[1]/20)
        self.theme = None
        self.background = None
        self.background_music = arcade.Sound(BACKGROUND_MUSIC)

        self.master_volume = 0.5

        self.abscond_button = None
        self.volume_meter = None
        self.volume_mover = None

        self.player_in_tutorial = True
        self.game_over_time = None
        self.absconded = None
        self.player_has_clicked_lithium = False
        self.player_has_healed_planet = False
        self.banner_text = None
        self.banner_location = (SCREEN_SIZE[0]/100, SCREEN_SIZE[1]/2)
        self.last_banner_change = None
        self.story_iter = None

        self.volume_location = (7*SCREEN_SIZE[0]/8, SCREEN_SIZE[1]/13)

        self.banner_background_color = arcade.make_transparent_color(
            arcade.color.BLUE, 100)

    def setup(self):
        self.planets = arcade.SpriteList()
        self.absconded = None
        self.game_over_time = None
        self.lithium_count = 0
        self.player_has_clicked_lithium = False
        self.player_has_healed_planet = False
        self.banner_text = ""
        self.last_banner_change = None
        self.story_iter = itertools.cycle(line for line in STORY_LINES)
        self.background = arcade.load_texture(
            BACKGROUND_IMAGE)
        try:
            self.background_music.stop()
        except NameError:
            # Soloud not installed
            pass
        self.background_music.play(
            BACKGROUND_MUSIC_VOLUME * self.master_volume)
        planets = [Planet(planet_name) for planet_name in ALL_PLANETS]
        self.setup_theme()
        self.abscond_button = TextButton(
            SCREEN_SIZE[0]/6, SCREEN_SIZE[1]/15, 200, 50,
            "Abscond", theme=self.theme)
        self.abscond_button.on_press = self.abscond_press
        self.abscond_button.on_release = self.abscond_release
        self.button_list.append(self.abscond_button)

        self.volume_meter = arcade.Sprite(VOLUME_IMAGE)
        self.volume_meter.center_x = self.volume_location[0]
        self.volume_meter.center_y = self.volume_location[1]
        self.volume_meter.width *= 3
        self.volume_meter_leftmost = (
            self.volume_meter.center_x - (self.volume_meter.width / 2))
        self.volume_meter_rightmost = (
            self.volume_meter.center_x + (self.volume_meter.width / 2))
        self.volume_meter_bottommost = (
            self.volume_meter.center_y - 10)
        self.volume_meter_topmost = (
            self.volume_meter.center_y + 10)
        self.volume_mover = arcade.Sprite(VOLUME_MOVER_IMAGE)
        self.volume_mover.center_x = self.volume_meter.center_x
        self.volume_mover.center_y = self.volume_meter.center_y
        self.volume_mover.scale /= 3

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

    def set_banner_text(self, new_text):
        if new_text == self.banner_text:
            return
        self.last_banner_change = time.time()
        self.banner_text = new_text
        x_coord = SCREEN_SIZE[0]/100
        y_coord = (
            (random.random() * (6 * SCREEN_SIZE[1] / 8))
            + (SCREEN_SIZE[1] / 5)
        )
        self.banner_location = (x_coord, y_coord)

    def abscond_press(self):
        self.abscond_button.pressed = True

    def abscond_release(self):
        if self.abscond_button.pressed:
            self.abscond_button.pressed = False
            self.absconded = True
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
                attack_point = random_location_in_planet(
                    (other.center_x, other.center_y),
                    other.width / 4
                )
                attack_start_radius = min(
                    planet.base_damage * 1e4, planet.width / 4)
                start_point_1, start_point_2 = get_attack_triangle_points(
                    (planet.center_x, planet.center_y),
                    attack_point,
                    attack_start_radius
                )
                arcade.draw_triangle_filled(
                    *start_point_1,
                    *start_point_2,
                    *attack_point,
                    color=planet.color
                )
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

        self.volume_meter.draw()
        self.volume_mover.draw()

        arcade.draw_rectangle_filled(
            center_x=SCREEN_SIZE[0]/2,
            center_y=20+self.banner_location[1],
            width=SCREEN_SIZE[0],
            height=40,
            color=self.banner_background_color)

        arcade.draw_text(
            self.banner_text,
            *self.banner_location,
            color=arcade.color.GREEN, font_size=22)

    def check_volume_press(self, x, y):
        if (
            self.volume_meter_leftmost < x < self.volume_meter_rightmost
            and self.volume_meter_bottommost < y < self.volume_meter_topmost
        ):
            self.master_volume = (
                (x - self.volume_meter_leftmost)
                / (self.volume_meter_rightmost - self.volume_meter_leftmost))
            self.background_music.set_volume(
                BACKGROUND_MUSIC_VOLUME * self.master_volume)
            self.volume_mover.center_x = x

    @log_exceptions
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.check_volume_press(x, y)

    @log_exceptions
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over_time:
            return
        if get_distance(x, y, *self.lithium_location) < 10:
            self.clicked_lithium()
        for planet in self.planets:
            if self.lithium_count >= 1 and planet.collides_with_point((x, y)):
                logger.info(f"Healing {planet.name}")
                self.lithium_count -= 1
                planet.get_healed(0.1)
                self.player_has_healed_planet = True

        self.abscond_button.check_mouse_press(x, y)

        self.check_volume_press(x, y)

    def clicked_lithium(self):
        planet_avg_health = self.avg_planet_health()
        self.lithium_count += planet_avg_health * LITHIUM_MULTIPLIER
        self.lithium_location = get_new_lithium_location()
        self.player_has_clicked_lithium = True

    def avg_planet_health(self):
        return (
            sum([planet.health for planet in self.planets]) / len(self.planets)
        )

    def on_update(self, delta_time):
        if self.game_over_time:
            game_over_delta_time = (
                BASE_TIME_MULTIPLIER * (time.time() - self.game_over_time)
            )
            if game_over_delta_time > 3 and not self.absconded:
                self.setup()
                return
        time_multiplier = BASE_TIME_MULTIPLIER * delta_time / 0.0168
        if self.player_in_tutorial:
            time_multiplier /= 6
        logger.debug("\nNew Round\n")
        if not self.player_in_tutorial:
            self.lithium_count += delta_time / 100
        self.run_assertions()
        self.update_banner()
        self.planets.update()
        [planet.move(time_multiplier) for planet in self.planets]
        [planet.try_attack_others(time_multiplier) for planet in self.planets]
        [planet.try_push_others(time_multiplier) for planet in self.planets]
        should_not_triangulate = (
            self.player_in_tutorial
            and self.lithium_count > 2
            and not self.player_has_healed_planet)
        [planet.update_triangulating(time_multiplier,
                                     self.player_in_tutorial,
                                     should_not_triangulate)
         for planet in self.planets]

        try:
            if self.background_music.get_stream_position() == 0.0:
                self.background_music.play(
                    self.master_volume * BACKGROUND_MUSIC_VOLUME)
        except AttributeError:
            # Soloud not installed
            pass

        self.run_assertions()

    def update_banner(self):
        if self.game_over_time:
            return
        if not self.player_in_tutorial:
            self.update_banner_story()
            return
        now = time.time()
        if self.last_banner_change is None:
            self.set_banner_text("This is the story of Ze, Yogh, and Ezh.")
        delta_time = BASE_TIME_MULTIPLIER * (now - self.last_banner_change)
        if not self.player_has_clicked_lithium and delta_time > 3:
            self.set_banner_text(
                "See the circles? Click on their intersection.")
        if (self.player_has_clicked_lithium
                and not self.player_has_healed_planet
                and not self.lithium_count > 2
                and delta_time > 0.5):
            self.set_banner_text("Good. Keep doing it.")
        if self.lithium_count > 2 and not self.player_has_healed_planet:
            self.set_banner_text(
                "Good. Now heal one of the planets by clicking on them."
            )
        if self.player_has_healed_planet:
            self.set_banner_text(
                "You've healed them with lithium. Keep them alive."
            )
            delta_time = BASE_TIME_MULTIPLIER * (now - self.last_banner_change)
            if delta_time > 2:
                self.player_in_tutorial = False

    def update_banner_story(self):
        if self.game_over_time:
            return
        now = time.time()
        self.last_banner_change = self.last_banner_change or now-5
        delta_time = BASE_TIME_MULTIPLIER * (now - self.last_banner_change)
        if delta_time < 3:
            return
        next_story_part = next(self.story_iter, self.banner_text)
        self.set_banner_text(next_story_part)

    def run_assertions(self):
        assert len(self.planets) in (1, 2, 3)
        if not self.game_over_time:
            assert len(self.planets) == 3
        assert self.lithium_count >= 0
        for planet in self.planets:
            if not self.game_over_time:
                assert len(planet.others) == 2
            assert planet.center_x > -SCREEN_SIZE[0]
            assert planet.center_x < SCREEN_SIZE[0] * 2
            assert planet.center_y > -SCREEN_SIZE[1]
            assert planet.center_y < SCREEN_SIZE[1] * 2
            assert planet.speed_x != 0
            assert planet.speed_y != 0

    def game_over(self, reason):
        if self.game_over_time:
            return
        self.banner_text = reason
        logger.info(f"Game over! {reason}")
        for planet in self.planets:
            logger.info(planet.get_stats_str())
        self.game_over_time = time.time()


def main():
    window = Game()
    window.setup()
    arcade.run()
