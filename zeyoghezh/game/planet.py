import arcade
from .util import (
    get_distance, closest_distance_between_planets, get_unit_push_distance
)
import logging
import time
import random
from .config import (
    SCREEN_SIZE, PLANET_BASE_SPEED, PUSH_BASE_SPEED,
    PUSH_MAX_DISTANCE, BASE_DAMAGE, PLANET_DAMAGE, MAX_ATTACK_DISTANCE,
    PLANET_COLORS, PLANET_SPRITES, TRIANGULATION_START_LIKELIHOOD,
    ATTACK_SOUND, ATTACK_PLAYS_SOUND_CHANCE, TRIANGULATION_FADE_OUT_TIME,
    SOUND_VOLUME, BOTTOM_BORDER_Y, TRIANGULATION_FADE_IN_TIME,
    TRIANGULATION_FADE_TOTAL_TIME
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

        self.last_triangulating = None

        self.proper_name = self.name[0].upper() + self.name[1:].lower()

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
        self.last_triangulating = time.time()

    def move(self, time_multiplier, delta_x=None, delta_y=None):
        # I have no idea why this needs to be 4 and not 2
        planet_radius = int(self.width / 4)

        if delta_x is None:
            delta_x = self.speed_x * PLANET_BASE_SPEED
        if delta_y is None:
            delta_y = self.speed_y * PLANET_BASE_SPEED

        delta_x *= time_multiplier
        delta_y *= time_multiplier

        new_x = self.center_x + delta_x
        new_y = self.center_y + delta_y

        if new_y >= SCREEN_SIZE[1] - planet_radius:
            new_y = SCREEN_SIZE[1] - planet_radius
            self.speed_y = min(-0.1, -random.random())
        if new_y <= BOTTOM_BORDER_Y + planet_radius:
            new_y = BOTTOM_BORDER_Y + planet_radius
            self.speed_y = max(0.1, random.random())
        if new_x >= SCREEN_SIZE[0] - planet_radius:
            new_x = SCREEN_SIZE[0] - planet_radius
            self.speed_x = min(-0.1, -random.random())
        if new_x <= planet_radius:
            new_x = planet_radius
            self.speed_x = max(0.1, random.random())

        adjusted_delta_x = new_x - self.center_x
        adjusted_delta_y = new_y - self.center_y

        logger.debug(
            f"Moving {self.name}. {self.center_x=}, {self.center_y=}, "
            f"{planet_radius=}, {delta_x=}, {delta_y=}, "
            f"{adjusted_delta_x=}, {adjusted_delta_y=}, {self.speed_x=}, "
            f"{self.speed_y=}")
        self.center_y += adjusted_delta_y
        self.center_x += adjusted_delta_x

    def try_push_others(self, time_multiplier):
        if not self.can_push_planets:
            return
        for other in self.others:
            distance = closest_distance_between_planets(self, other)
            if distance < PUSH_MAX_DISTANCE:
                self.push_other(other, time_multiplier)

    def push_other(self, other, time_multiplier):
        self_coords = (self.center_x, self.center_y)
        other_coords = (other.center_x, other.center_y)
        unit_push_distance = get_unit_push_distance(self_coords, other_coords)
        logger.debug(
            f"{self.name} ({self_coords}) pushing {other.name} "
            f"({other_coords}) by {unit_push_distance}")
        other.move(
            time_multiplier,
            delta_x=unit_push_distance[0]*PUSH_BASE_SPEED,
            delta_y=unit_push_distance[1]*PUSH_BASE_SPEED)
        self.move(
            time_multiplier,
            delta_x=-unit_push_distance[0]*PUSH_BASE_SPEED/3,
            delta_y=-unit_push_distance[1]*PUSH_BASE_SPEED/3
        )

    def try_attack_others(self, time_multiplier):
        for other in self.others:
            distance = closest_distance_between_planets(self, other)
            if distance < self.max_attack_distance:
                self.attack_other(other, time_multiplier)

    def attack_other(self, other, time_multiplier):
        if random.random() < ATTACK_PLAYS_SOUND_CHANCE * time_multiplier:
            try:
                not_playing = self.attack_sound.get_stream_position() == 0.0
            except TypeError:
                not_playing = True
            if not_playing:
                self.attack_sound.play(
                    self.parent.master_volume * SOUND_VOLUME)
        self.attacked_last_round.append(other)
        distance_between = closest_distance_between_planets(self, other)
        damage = self.base_damage * time_multiplier
        logger.debug(
            f"{self.name} attacking {other.name} "
            f"({distance_between=} for {damage}")
        other.health -= damage
        self.damage_on_others[other.name] += damage
        other.scale = other.health
        if other.health < 0:
            other.die()

    def die(self):
        for planet in self.others:
            logger.info(f"Removing {self.name} from others in {planet.name}")
            planet.others.remove(self)
        self.parent.planets.remove(self)
        self.parent.game_over(
            f"All is lost. {self.proper_name} has died.")

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
        triangulation_strength = self.get_triangulation_strength()
        transparentized_color = arcade.make_transparent_color(
            self.color, triangulation_strength)
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

    def get_triangulation_strength(self):
        health_normalized = max(min(self.health, 1), 0.5)
        if self.last_triangulating < self.parent.last_lithium_change:
            return 0
        time_since_last_triangulation = time.time() - self.last_triangulating
        if time_since_last_triangulation <= TRIANGULATION_FADE_IN_TIME:
            triangulation_trace = (
                time_since_last_triangulation
                / TRIANGULATION_FADE_IN_TIME
            )
        else:
            triangulation_trace = max(
                0,
                (TRIANGULATION_FADE_OUT_TIME - (
                    time_since_last_triangulation
                    - TRIANGULATION_FADE_IN_TIME)
                 )
                / TRIANGULATION_FADE_OUT_TIME)
        triangulation_strength = health_normalized * triangulation_trace
        alpha = int(triangulation_strength * 255)
        logger.debug(
            f"{triangulation_trace=}, {health_normalized=}, "
            f"{triangulation_strength=}, {alpha=}, "
            f"{time_since_last_triangulation=}")
        assert 0 <= health_normalized
        assert health_normalized <= 1
        assert 0 <= triangulation_trace
        assert triangulation_trace <= 1, f"{triangulation_trace=}"
        assert 0 <= triangulation_strength
        assert triangulation_strength <= 1
        assert 0 <= alpha
        assert alpha <= 255
        return alpha

    def update_triangulating(
            self, time_multiplier, in_tutorial, should_not_triangulate):
        if should_not_triangulate:
            return
        last_triangulating_delta = time.time() - self.last_triangulating
        if last_triangulating_delta < TRIANGULATION_FADE_TOTAL_TIME:
            return
        adjusted_time_multiplier = (
            time_multiplier * 6 if in_tutorial else time_multiplier)
        start_chance = 1 - (
            (1 - TRIANGULATION_START_LIKELIHOOD) ** adjusted_time_multiplier)
        if random.random() < start_chance:
            self.last_triangulating = time.time()
