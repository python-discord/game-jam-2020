import itertools
from pathlib import Path
from typing import Any, Optional, Tuple

import arcade

from triple_vision.constants import Direction
from triple_vision.utils import load_texture_pair


class AnimatedEntity(arcade.Sprite):

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

        self.entity_face_direction = Direction.RIGHT
        self._prev_anim_delta = 0

        self._textures = dict()

        gender = f'{gender}_' if gender is not None else ''

        if self.is_colored:
            colors = ('red', 'green', 'blue')
            self.cur_color = colors[0]

            for color in colors:
                self._textures[color] = dict()

                for state in states:
                    self._textures[color][state] = {
                        'cycle': itertools.cycle(frame_range)
                    }

                    self._textures[color][state]['texture'] = [
                        load_texture_pair(
                            self.assets_path / color / f'{sprite_name}_{gender}{state}_anim_f{i}.png'
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

            self.texture = self._textures[self.cur_color]['idle']['texture'][0][self.entity_face_direction]

        else:
            for state in states:
                self._textures[state] = {
                    'cycle': itertools.cycle(frame_range)
                }

                self._textures[state]['texture'] = [
                    load_texture_pair(
                        self.assets_path / f'{sprite_name}_{gender}{state}_anim_f{i}.png'
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

            self.texture = self._textures['idle']['texture'][0][self.entity_face_direction]

        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1/60) -> None:
        self._prev_anim_delta += delta_time

        if self.change_x < 0 and self.entity_face_direction == Direction.RIGHT:
            self.entity_face_direction = Direction.LEFT
        elif self.change_x > 0 and self.entity_face_direction == Direction.LEFT:
            self.entity_face_direction = Direction.RIGHT

        if self._prev_anim_delta > 0.15:
            state = 'idle' if self.change_x == 0 else 'run'

            if self.is_colored:
                self.texture = self._textures[self.cur_color][state]['texture'][
                    next(self._textures[self.cur_color][state]['cycle'])
                ][self.entity_face_direction]

            else:
                self.texture = self._textures[state]['texture'][
                    next(self._textures[state]['cycle'])
                ][self.entity_face_direction]

            self._prev_anim_delta = 0

    def update(self, delta_time: float = 1/60) -> None:
        self.update_animation(delta_time)
        super().update()
