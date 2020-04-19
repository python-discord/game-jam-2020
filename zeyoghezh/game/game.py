import random
import arcade
import logging
from planet import Planet
from config import SCREEN_SIZE_Y, SCREEN_SIZE_X
import sys


LOGGING_FORMAT = ("%(asctime)-15s %(levelname)s in %(funcName)s "
                  "at %(pathname)s:%(lineno)d: %(message)s")
logging.basicConfig(
    stream=sys.stderr, level=logging.INFO, format=LOGGING_FORMAT)

logger = logging.getLogger()

SCREEN_TITLE = "Zeyoghezh"
ALL_PLANETS = ("ze", "yogh", "ezh")


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_SIZE_X, SCREEN_SIZE_Y, SCREEN_TITLE)
        self.planets = None
        self.planet_sprites = arcade.SpriteList()

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
                center_x=random.random()*SCREEN_SIZE_X,
                center_y=random.random()*SCREEN_SIZE_Y,
                start_speed_x=random.random(),
                start_speed_y=random.random()
            )

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
                    color=planet.attack_color,
                    line_width=planet.base_damage * 1e4)
            planet.attacked_last_round = []
            planet.pushed_last_round = []
        self.planet_sprites.draw()

    def on_update(self, delta_time):
        logger.debug("\nNew Round\n")
        self.run_assertions()
        self.planet_sprites.update()
        [planet.move() for planet in self.planets]
        [planet.try_attack_others() for planet in self.planets]
        [planet.try_push_others() for planet in self.planets]

    def run_assertions(self):
        assert len(self.planets) == 3
        for planet in self.planets:
            assert len(planet.others) == 2
            assert planet.center_x > -SCREEN_SIZE_X
            assert planet.center_x < SCREEN_SIZE_X * 2
            assert planet.center_y > -SCREEN_SIZE_Y
            assert planet.center_y < SCREEN_SIZE_Y * 2
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
