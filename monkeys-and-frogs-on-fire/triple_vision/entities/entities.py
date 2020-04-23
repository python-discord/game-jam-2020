import itertools
import random
from pathlib import Path
from typing import Any, Optional, Tuple

import arcade

from triple_vision import Direction, Settings as s
from triple_vision.utils import (
    get_change_vector,
    load_texture_pair,
    tile_to_pixels
)


class Entity(arcade.Sprite):

    def __init__(self, ctx, spawn_in_map=True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.ctx = ctx
        self.spawn_in_map = spawn_in_map

    def setup(self) -> None:
        if self.spawn_in_map:
            while True:
                center = tile_to_pixels(random.randrange(0, s.MAP_SIZE[0]), random.randrange(0, s.MAP_SIZE[1]))

                if (
                    len(arcade.get_sprites_at_point(center, self.ctx.view.collision_list)) == 0 and
                    len(arcade.get_sprites_at_point(center, self.ctx.view.map.sprites)) > 0
                ):
                    break

            self.center_x = center[0]
            self.center_y = center[1]


class AnimatedEntity(Entity):

    def __init__(
        self,
        sprite_name: str,
        assets_path: str,
        frame_range: range = range(4),
        is_colored: bool = False,
        has_hit_frame: bool = False,
        gender: Optional[str] = None,
        states: Tuple[str, ...] = ('idle', 'run'),
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)

        self.assets_path = Path(assets_path)
        self.has_hit_frame = has_hit_frame
        self.is_colored = is_colored
        self.states = states

        self.entity_face_direction = Direction.RIGHT
        self._prev_anim_delta = 0

        self._textures = dict()

        gender = f'{gender}_' if gender is not None else ''

        if self.is_colored:
            colors = ('red', 'green', 'blue')
            self.curr_color = colors[0]

            for color in colors:
                self._textures[color] = dict()

                for state in states:
                    self._textures[color][state] = {
                        'cycle': itertools.cycle(frame_range)
                    }
                    s = f'{state}_' if state else ''

                    self._textures[color][state]['texture'] = [
                        load_texture_pair(
                            self.assets_path / color / f'{sprite_name}_{gender}{s}anim_f{i}.png'
                        ) for i in range(4)
                    ]

                if self.has_hit_frame:
                    self._textures[color]['hit'] = {
                        'cycle': itertools.cycle((0,))
                    }

                    self._textures[color]['hit']['texture'] = [
                        load_texture_pair(
                            self.assets_path / color / f'{sprite_name}_{gender}hit_anim_f0.png'
                        )
                    ]

            self.texture = self._textures[self.curr_color][states[0]]['texture'][0][self.entity_face_direction]

        else:
            for state in states:
                self._textures[state] = {
                    'cycle': itertools.cycle(frame_range)
                }
                s = f'{state}_' if state else ''

                self._textures[state]['texture'] = [
                    load_texture_pair(
                        self.assets_path / f'{sprite_name}_{gender}{s}anim_f{i}.png'
                    ) for i in frame_range
                ]

            if self.has_hit_frame:
                self._textures['hit'] = {
                    'cycle': itertools.cycle((0,))
                }

                self._textures['hit']['texture'] = [
                    load_texture_pair(
                        self.assets_path / f'{sprite_name}_{gender}hit_anim_f0.png'
                    )
                ]

            self.texture = self._textures[states[0]]['texture'][0][self.entity_face_direction]

        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1/60) -> None:
        self._prev_anim_delta += delta_time

        if self.change_x < 0 and self.entity_face_direction == Direction.RIGHT:
            self.entity_face_direction = Direction.LEFT
        elif self.change_x > 0 and self.entity_face_direction == Direction.LEFT:
            self.entity_face_direction = Direction.RIGHT

        if self._prev_anim_delta > 0.15:
            state = '' if not self.states[0] else 'idle' if self.change_x == 0 else 'run'

            if self.is_colored:
                self.texture = self._textures[self.curr_color][state]['texture'][
                    next(self._textures[self.curr_color][state]['cycle'])
                ][self.entity_face_direction]

            else:
                self.texture = self._textures[state]['texture'][
                    next(self._textures[state]['cycle'])
                ][self.entity_face_direction]

            self._prev_anim_delta = 0

    def on_update(self, delta_time: float = 1/60) -> None:
        self.update_animation(delta_time)
        super().on_update(delta_time)


class LivingEntity(AnimatedEntity):

    def __init__(self, hp: float = 0, is_pushable: bool = True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.hp = hp
        self.is_pushable = is_pushable
        self.being_pushed = False
        self._is_hit = False
        self._red_color_ticks = 0.0
        self._red_color_duration = 0.5

        self.resistance = 0

    def hit(self, weapon, wall_reference: arcade.SpriteList = tuple()) -> None:
        """
        :param weapon: Weapon the entity is being hit. Used for getting dmg, throwback force
                       and position for knock-back direction.
        :param wall_reference: SpriteList of things that the entity cannot go trough. This will
                               stop the entity from being pushed and slightly damage the entity.
                               TODO: Currently a placeholder, to be implemented,
                                     maybe this check should be done in manager?
                                     So if hits wall and being_pushed True then deduct hp
        """
        self._is_hit = True
        self.color = (255, 0, 0)

        weapon.play_hit_sound()

        self.hp -= weapon.dmg * (1 - self.resistance)
        if self.hp <= 0:
            self.kill()
            return

        if self.being_pushed or not self.is_pushable:
            return

        change = get_change_vector(
            start_position=weapon.position,
            destination_position=self.position,
            speed_multiplier=weapon.throwback_force
        )
        self.change_x, self.change_y = change[0], change[1]

        self.being_pushed = True

    def reduce_throwback(self, delta_time: float) -> None:
        relative_time = delta_time * 60

        if self.being_pushed:
            if self.change_x > 0:
                self.change_x -= 1 * relative_time
            elif self.change_x < 0:
                self.change_x += 1 * relative_time

            if self.change_y > 0:
                self.change_y -= 1 * relative_time
            elif self.change_y < 0:
                self.change_y += 1 * relative_time

            # Change is float so we can't really check if it's exactly 0
            # because it can be 0.1 so we just round it from -1 to 1
            if -1 <= self.change_x <= 1 and -1 <= self.change_y <= 1:
                self.being_pushed = False
                self.change_x = 0
                self.change_y = 0

    def on_update(self, delta_time: float = 1/60):
        if self._is_hit:
            if self._red_color_ticks >= self._red_color_duration:
                self._is_hit = False
                self.color = (255, 255, 255)
                self._red_color_ticks = 0.0
            else:
                self._red_color_ticks += delta_time

        if self.being_pushed and self.is_pushable:
            self.reduce_throwback(delta_time)

        super().on_update(delta_time)


class SoundEntity(arcade.Sprite):
    assets_path = Path("assets/audio/sounds/")

    def __init__(
            self,
            *args,
            activate_sounds: tuple,
            hit_sounds: tuple,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._activate_sounds = self.load_sounds(activate_sounds)
        self._hit_sounds = self.load_sounds(hit_sounds)

    @classmethod
    def load_sounds(cls, sounds: Tuple[str]):
        return [arcade.load_sound(str(cls.assets_path / sound)) for sound in sounds]

    def play_activate_sound(self) -> None:
        arcade.play_sound(random.choice(self._activate_sounds))

    def play_hit_sound(self) -> None:
        arcade.play_sound(random.choice(self._hit_sounds))
