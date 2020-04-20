import arcade
from .util import (
    get_distance, closest_distance_between_planets, get_unit_push_distance
)
import logging
import random
from .config import (
    SCREEN_SIZE, PLANET_BASE_SPEED, PUSH_BASE_SPEED,
    PUSH_MAX_DISTANCE, BASE_DAMAGE, PLANET_DAMAGE, MAX_ATTACK_DISTANCE,
    PLANET_COLORS, PLANET_SPRITES, TRIANGULATION_START_LIKELIHOOD,
    TRIANGULATION_END_LIKELIHOOD, ATTACK_SOUND, ATTACK_PLAYS_SOUND_CHANCE,
    SOUND_VOLUME
)

logger = logging.getLogger()


class Planet(arcade.Sprite):
    def __init__(self, planet_name, *args, **kwargs):
        super().__init__(PLANET_SPRITES[planet_name], *args, **kwargs)
        self.name = planet_name
        self.speed_x = None
        self.speed_y = None
        self.health = 1
        self.can_push_planets = self.name == "yogh"
        self.can_blast_planets = self.name == "yogh"
        self.can_melee_planets = self.name == "ze"
        self.can_range_planets = self.name == "ezh"
        self.max_attack_distance = MAX_ATTACK_DISTANCE[self.name]
        self.base_damage = BASE_DAMAGE * PLANET_DAMAGE[self.name]
        self.color = PLANET_COLORS[self.name]
        self.attack_sound = arcade.Sound(ATTACK_SOUND[self.name])

        self.parent = None
        self.others = None
        self.damage_on_others = None

        self.attacked_last_round = []
        self.total_healing = 0

        self.is_triangulating = False

    def setup(
            self, parent, others, center_x, center_y,
            start_speed_x, start_speed_y):
        self.parent = parent
        self.others = others
        self.damage_on_others = {other.name: 0 for other in others}
        self.center_x = center_x
        self.center_y = center_y
        self.speed_x = start_speed_x
        self.speed_y = start_speed_y

    def move(self, delta_x=None, delta_y=None):
        if self.center_y > SCREEN_SIZE[1] - 5:
            self.speed_y = -abs(self.speed_y) - (random.random() / 100)
        if self.center_y < 0 + 5:
            self.speed_y = abs(self.speed_y) + (random.random() / 100)
        if self.center_x > SCREEN_SIZE[0] - 5:
            self.speed_x = -abs(self.speed_x) - (random.random() / 100)
        if self.center_x < 0 + 5:
            self.speed_x = abs(self.speed_x) + (random.random() / 100)

        if delta_x is None:
            delta_x = self.speed_x * PLANET_BASE_SPEED
        if delta_y is None:
            delta_y = self.speed_y * PLANET_BASE_SPEED

        logger.debug(f"Moving {self.name}. {delta_x=}, {delta_y=}.")
        self.center_y += delta_y
        self.center_x += delta_x

    def try_push_others(self):
        if not self.can_push_planets:
            return
        for other in self.others:
            distance = closest_distance_between_planets(self, other)
            if distance < PUSH_MAX_DISTANCE:
                self.push_other(other)

    def push_other(self, other):
        self_coords = (self.center_x, self.center_y)
        other_coords = (other.center_x, other.center_y)
        unit_push_distance = get_unit_push_distance(self_coords, other_coords)
        logger.debug(
            f"{self.name} ({self_coords}) pushing {other.name} "
            f"({other_coords}) by {unit_push_distance}")
        other.move(
            delta_x=unit_push_distance[0]*PUSH_BASE_SPEED,
            delta_y=unit_push_distance[1]*PUSH_BASE_SPEED)

    def try_attack_others(self):
        for other in self.others:
            distance = closest_distance_between_planets(self, other)
            if distance < self.max_attack_distance:
                self.attack_other(other)

    def attack_other(self, other):
        if random.random() > ATTACK_PLAYS_SOUND_CHANCE:
            self.attack_sound.play(SOUND_VOLUME)
        self.attacked_last_round.append(other)
        distance_between = closest_distance_between_planets(self, other)
        logger.debug(
            f"{self.name} attacking {other.name} "
            f"({distance_between=} for {self.base_damage}")
        other.health -= self.base_damage
        self.damage_on_others[other.name] += self.base_damage
        other.scale = other.health
        if other.health < 0:
            other.die()

    def die(self):
        for planet in self.others:
            logger.info(f"Removing {self.name} from others in {planet.name}")
            planet.others.remove(self)
        self.parent.planets.remove(self)
        self.parent.game_over(f"{self.name} has died")

    def get_stats_str(self):
        total_damage_on_others = round(sum(self.damage_on_others.values()), 4)
        damage_on_others = {
            other: round(self.damage_on_others[other], 4)
            for other in self.damage_on_others}
        return (
            f"{self.name}:\t{total_damage_on_others=}, {damage_on_others=}, "
            f"{self.total_healing=}"
        )

    def draw_triangulation_circle(self):
        health_normalized = int(255 * min(self.health, 1))
        transparentized_color = arcade.make_transparent_color(
            self.color, health_normalized)
        lithium_location = self.parent.lithium_location
        distance_to_lithium = get_distance(
            self.center_x, self.center_y, *lithium_location
        )
        arcade.draw_circle_outline(
            self.center_x, self.center_y, distance_to_lithium,
            color=transparentized_color)

    def get_healed(self, health):
        self.health += health
        self.total_healing += health
        self.scale = self.health
        assert self.health > 0

    def update_triangulating(self):
        if random.random() < TRIANGULATION_START_LIKELIHOOD:
            self.is_triangulating = True
        if random.random() < TRIANGULATION_END_LIKELIHOOD:
            self.is_triangulating = False
