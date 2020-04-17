import itertools
from pathlib import Path

import arcade

from triple_vision.constants import Direction, SCALING
from triple_vision.utils import load_texture_pair


class Player(arcade.Sprite):

    def __init__(self, gender: str) -> None:
        super().__init__(scale=SCALING)

        self.character_face_direction = Direction.RIGHT
        self.cur_texture = 0

        self.prev_anim = 0

        self._textures = dict()
        self.cur_color = 'blue'

        main_path = Path('assets/wizard')

        colors = ('red', 'green', 'blue')
        states = ('idle', 'run')

        for color in colors:
            self._textures[color] = dict()

            for state in states:
                self._textures[color][state] = {
                    'cycle': itertools.cycle(range(4))
                }

                self._textures[color][state]['texture'] = [
                    load_texture_pair(
                        main_path / color / f'wizzard_{gender}_{state}_anim_f{i}.png'
                    ) for i in range(4)
                ]

            self._textures[color]['hit'] = {
                'cycle': itertools.cycle((0,))
            }

            self._textures[color]['hit']['texture'] = [
                load_texture_pair(
                    main_path / color / f'wizzard_{gender}_hit_anim_f0.png'
                )
            ]

        self.texture = self._textures[self.cur_color]['idle']['texture'][0][self.character_face_direction]

        self.set_hit_box(self.texture.hit_box_points)

        self.center_x += 500
        self.center_y += 500

    def update_animation(self, delta_time: float = 1/60):
        self.prev_anim += delta_time

        if self.change_x < 0 and self.character_face_direction == Direction.RIGHT:
            self.character_face_direction = Direction.LEFT
        elif self.change_x > 0 and self.character_face_direction == Direction.LEFT:
            self.character_face_direction = Direction.RIGHT

        if self.prev_anim > 0.15:

            if self.change_x == 0:
                self.texture = self._textures[self.cur_color]['idle']['texture'][
                    next(self._textures[self.cur_color]['idle']['cycle'])
                ][self.character_face_direction]

                self.prev_anim = 0
