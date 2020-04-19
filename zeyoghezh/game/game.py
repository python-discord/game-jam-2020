import random
import arcade
import logging
from util import get_distance, log_exceptions
from planet import Planet
from config import (
    SCREEN_SIZE, TRIANGULATION_FREQUENCY, SCREEN_TITLE, ALL_PLANETS
)
import sys


LOGGING_FORMAT = ("%(asctime)-15s %(levelname)s in %(funcName)s "
                  "at %(pathname)s:%(lineno)d: %(message)s")
logging.basicConfig(
    stream=sys.stderr, level=logging.INFO, format=LOGGING_FORMAT)

logger = logging.getLogger()


def get_new_lithium_location():
    return (
        random.randint(SCREEN_SIZE[0]/10, 9*SCREEN_SIZE[0]/10),
        random.randint(SCREEN_SIZE[1]/10, 9*SCREEN_SIZE[1]/10),
    )


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_SIZE[0], SCREEN_SIZE[1], SCREEN_TITLE)
        self.planets = None
        self.planet_sprites = arcade.SpriteList()
        self.lithium_location = get_new_lithium_location()
        self.lithium_count = 0
        self.lithium_score_location = (SCREEN_SIZE[0]/3, SCREEN_SIZE[1]/20)

    def setup(self):
        self.planets = [Planet(planet_name) for planet_name in ALL_PLANETS]
        for i, planet in enumerate(self.planets):
            # TODO improve this
            self.planet_sprites.append(planet)
            planets_copy = self.planets.copy()
            planets_copy.remove(planet)
            planet.setup(
                parent=self,
                others=planets_copy,
                center_x=random.random()*SCREEN_SIZE[0],
                center_y=random.random()*SCREEN_SIZE[1],
                start_speed_x=random.random(),
                start_speed_y=random.random()
            )

    @log_exceptions
    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        for planet in self.planets:
            for other in planet.attacked_last_round:
                arcade.draw_line(
                    start_x=planet.center_x, start_y=planet.center_y,
                    end_x=(
                        other.center_x+(
                            random.random()*other.width/2)
                        - (other.width/2)),
                    end_y=(
                        other.center_y+(
                            random.random()*other.height/2)
                        - (other.height/2)),
                    color=planet.color,
                    line_width=planet.base_damage * 1e4)
            planet.attacked_last_round = []
            planet.pushed_last_round = []

            # TODO make this last some time, not just 1 frame
            if TRIANGULATION_FREQUENCY > random.random():
                planet.draw_triangulation_circle()
        self.planet_sprites.draw()
        arcade.draw_text(
            f"{self.lithium_count=}", *self.lithium_score_location,
            color=arcade.color.WHITE, font_size=24)

    @log_exceptions
    def on_mouse_press(self, x, y, button, modifiers):
        if get_distance(x, y, *self.lithium_location) < 10:
            self.clicked_lithium()
        for planet in self.planets:
            if self.lithium_count and planet.collides_with_point((x, y)):
                logger.info(f"Healing {planet.name}")
                self.lithium_count -= 1
                planet.get_healed(0.1)

    def clicked_lithium(self):
        self.lithium_count += 1
        self.lithium_location = get_new_lithium_location()

    def on_update(self, delta_time):
        logger.debug("\nNew Round\n")
        self.run_assertions()
        self.planet_sprites.update()
        [planet.move() for planet in self.planets]
        [planet.try_attack_others() for planet in self.planets]
        [planet.try_push_others() for planet in self.planets]

    def run_assertions(self):
        assert len(self.planets) == 3
        assert self.lithium_count >= 0
        for planet in self.planets:
            assert len(planet.others) == 2
            assert planet.center_x > -SCREEN_SIZE[0]
            assert planet.center_x < SCREEN_SIZE[0] * 2
            assert planet.center_y > -SCREEN_SIZE[1]
            assert planet.center_y < SCREEN_SIZE[1] * 2
            assert planet.speed_x != 0
            assert planet.speed_y != 0

    def game_over(self, reason):
        print(f"Game over! {reason}")
        for planet in self.planets:
            logger.info(planet.get_stats_str())
        sys.exit(0)


def main():
    window = Game()
    window.setup()
    arcade.run()
