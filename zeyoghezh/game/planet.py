import arcade
from util import get_distance, closest_distance_between_planets
import logging
import random
from config import (
    SCREEN_SIZE, PLANET_BASE_SPEED, PUSH_BASE_SPEED,
    PUSH_MAX_DISTANCE, BASE_DAMAGE, PLANET_DAMAGE, MAX_ATTACK_DISTANCE,
    PLANET_COLORS, PLANET_SPRITES
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

        self.parent = None
        self.others = None
        self.damage_on_others = None

        self.attacked_last_round = []
        self.total_healing = 0

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
        # TODO improve this logic
        x_distance = other.center_x - self.center_x
        y_distance = other.center_y - self.center_y
        distance_sum = abs(x_distance) + abs(y_distance)
        x_distance_normalized = x_distance / distance_sum
        y_distance_normalized = y_distance / distance_sum
        x_push = x_distance_normalized * PUSH_BASE_SPEED
        y_push = y_distance_normalized * PUSH_BASE_SPEED
        logger.debug(
            f"{self.name} pushing {other.name}  ({x_distance=}, {y_distance=} "
            f"by {x_push=}, {y_push=}")

        if self.center_x > other.center_x:
            assert x_push < 0
        if self.center_x < other.center_x:
            assert x_push > 0
        if self.center_x == other.center_x:
            assert x_push == 0
        if self.center_y > other.center_y:
            assert y_push < 0
        if self.center_y < other.center_y:
            assert y_push > 0
        if self.center_y == other.center_y:
            assert y_push == 0
        if abs(x_distance) > abs(y_distance):
            assert abs(x_distance_normalized) > abs(y_distance_normalized)

        other.move(delta_x=x_push, delta_y=y_push)

    def try_attack_others(self):
        for other in self.others:
            distance = closest_distance_between_planets(self, other)
            if distance < self.max_attack_distance:
                self.attack_other(other)

    def attack_other(self, other):
        self.attacked_last_round.append(other)
        distance_between = closest_distance_between_planets(self, other)
        logger.debug(
            f"{self.name} attacking {other.name} "
            f"({distance_between=} for {self.base_damage}")
        # TODO improve this
        other.health -= self.base_damage
        self.damage_on_others[other.name] += self.base_damage
        other.scale = other.health
        if other.health < 0:
            other.die()

    def die(self):
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
        lithium_location = self.parent.lithium_location
        distance_to_lithium = get_distance(
            self.center_x, self.center_y, *lithium_location
        )
        arcade.draw_circle_outline(
            self.center_x, self.center_y, distance_to_lithium,
            color=self.color)

    def get_healed(self, health):
        self.health += health
        self.total_healing += health
        self.scale = self.health
        assert self.health > 0
