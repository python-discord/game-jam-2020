"""Module for the player sprite."""
from __future__ import annotations
import arcade
from typing import Mapping
from PIL import Image, ImageDraw

from constants import ASSETS, HEIGHT, SPEED, WIDTH
import game


class Player(arcade.Sprite):
    """The player sprite."""

    TEXTURES = [
        'jump', 'walk_forward', 'walk_right_0', 'walk_right_1',
        'walk_right_2', 'walk_right_3', 'walk_right_4', 'walk_right_5',
        'walk_right_6', 'walk_right_7'
    ]

    def __init__(self, game: game.Game, n: int = 0, x: int = WIDTH // 5,
                 y: int = HEIGHT // 2, speed: int = SPEED):
        """Set up counters and load textures."""
        self.image = ASSETS + f'player_{n}_{{name}}.png'
        super().__init__(center_x=x, center_y=y)
        self.player = n
        self.textures = {}
        for texture in Player.TEXTURES:
            if texture == 'jump':
                self.textures.update(self.load_rotations(texture))
            else:
                self.textures.update(self.load_flipped_pair(texture))
        self.texture = self.textures['walk_forward_up']
        self.game = game
        self.speed = speed
        self.time_since_change = 0
        self.num = 0
        self.last_x = -1
        self.engine = None    # will be overwritten by game

    def prepare(self, name: str) -> Image.Image:
        """Open and resize an image for a texture."""
        file = self.image.format(name=name)
        old = Image.open(file)
        pixel_size = 2
        old_w, old_h = old.size
        new_w = old_w * pixel_size
        new_h = old_h * pixel_size
        new = Image.new('RGBA', (new_w, new_h), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(new)
        for x in range(old_w):
            for y in range(old_h):
                col = old.getpixel((x, y))
                draw.rectangle([
                    x * pixel_size, y * pixel_size, (x + 1) * pixel_size,
                    (y + 1) * pixel_size
                ], col, col)
        return new

    def load_rotations(self, name: str) -> Mapping[str, arcade.Texture]:
        """Load the four rotations by 90 degrees of an image."""
        im = self.prepare(name)
        textures = {}
        for n in range(4):
            n_name = f'{name}_{n}'
            textures[n_name] = arcade.Texture(n_name, im.rotate(n * 90))
        return textures

    def load_flipped_pair(self, name: str) -> Mapping[str, arcade.Texture]:
        """Load the vertically flipped versions of an image."""
        im = self.prepare(name)
        return {
            f'{name}_up': arcade.Texture(name + 'up', im),
            f'{name}_down': arcade.Texture(
                name + 'down', im.transpose(Image.FLIP_TOP_BOTTOM)
            )
        }

    def switch(self):
        """If allowed, switch gravity."""
        if self.engine.can_jump():
            self.engine.gravity_constant *= -1

    def update(self):
        """Move the player and change the texture."""
        direction = ['up', 'down'][self.engine.gravity_constant < 0]
        if abs(self.center_x - self.last_x) < 1:
            name = f'walk_forward_{direction}'
        elif self.engine.can_jump():
            name = f'walk_right_{self.num}_{direction}'
        else:
            name = f'jump_{self.num}'
        self.texture = self.textures[name]

        self.last_x = self.center_x

        # check touching sprites
        gems = arcade.check_for_collision_with_list(self, self.game.gems)
        for gem in gems:
            for box in self.game.boxes:
                if not box.colour:
                    box.add_gem(gem.colour, self.player)
                    break
            gem.place()

        spikes = arcade.check_for_collision_with_list(self, self.game.spikes)
        if spikes:
            self.game.game_over('Hit a Spike', self.player)
            return

        self.change_x = self.speed
        if self.center_x < self.game.left + WIDTH // 5:
            self.change_x *= 1.1
        self.engine.update()
        self.change_x = 0

        self.time_since_change += 1
        if self.time_since_change > 6:
            self.time_since_change = 0
            self.num += 1
            self.num %= 4
