"""Module for the player sprite."""
from __future__ import annotations
import arcade
from typing import Dict, Optional, Union
from PIL import Image, ImageDraw

from constants import ASSETS, HEIGHT, SCALING, SPEED, TOP, WIDTH
import displays
import engine
import game
import multiplayer
from utils import play_sound_effect


class Player(arcade.Sprite):
    """The player sprite."""

    TEXTURES = [
        'jump', 'walk_forward', 'walk_right_0', 'walk_right_1',
        'walk_right_2', 'walk_right_3', 'walk_right_4', 'walk_right_5',
        'walk_right_6', 'walk_right_7'
    ]

    def __init__(self,
                 master: Union[multiplayer.MultiplayerGame, game.Game],
                 player_num: int = 0, x: int = WIDTH // 5,
                 y: int = HEIGHT // 2, speed: float = SPEED):
        """Set up counters and load textures."""
        self.image = ASSETS + f'player_{player_num}_{{name}}.png'
        super().__init__(center_x=x, center_y=y)
        self.player = player_num
        self.all_textures = {}
        for texture in Player.TEXTURES:
            if texture == 'jump':
                self.all_textures.update(self.load_rotations(texture))
            else:
                self.all_textures.update(self.load_flipped_pair(texture))
        self.texture = self.all_textures['walk_forward_up']
        self.game = master
        self.speed = speed
        self.time_since_change = 0
        self.num = 0
        self.last_x = -1
        self.boxes: arcade.SpriteList = arcade.SpriteList()
        y = HEIGHT - TOP // 2 + 8
        start_x = player_num * (WIDTH / 4)
        for n in range(5):
            if isinstance(self.game, game.Game):
                scale = 0.5 * SCALING
            else:
                scale = 0.4 * SCALING
            x = start_x + (n + 0.6) * scale * 500
            self.boxes.append(displays.Box(x, y, self, scale))
        self.score = 0
        self.engine: Optional[engine.PhysicsEngine] = None
        self.blocks: Optional[arcade.SpriteList] = None
        self.revive_after: Optional[int] = None
        self.death_message: Optional[str] = None

    def prepare(self, name: str) -> Image.Image:
        """Open and resize an image for a texture."""
        file = self.image.format(name=name)
        old = Image.open(file)
        pixel_size = int(8 * SCALING)
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

    def load_rotations(self, name: str) -> Dict[str, arcade.Texture]:
        """Load the four rotations by 90 degrees of an image."""
        im = self.prepare(name)
        textures = {}
        for n in range(4):
            uid = f'{name}_{n}_{self.player}'
            textures[f'{name}_{n}'] = arcade.Texture(uid, im.rotate(n * 90))
        return textures

    def load_flipped_pair(self, name: str) -> Dict[str, arcade.Texture]:
        """Load the vertically flipped versions of an image."""
        im = self.prepare(name)
        return {
            f'{name}_up': arcade.Texture(f'{name}_up_{self.player}', im),
            f'{name}_down': arcade.Texture(
                f'{name}_down_{self.player}', im.transpose(
                    Image.FLIP_TOP_BOTTOM
                )
            )
        }

    def switch(self):
        """If allowed, switch gravity."""
        if self.engine.can_jump():
            self.engine.gravity_constant *= -1

    def update(self):
        """Move the player and change the texture."""
        self.boxes.update()

        if self.revive_after is not None:
            self.revive_after -= 1
            self.center_x += self.speed
            if self.center_x < self.game.left + WIDTH // 5:
                self.center_x += self.speed * 0.1
            if self.revive_after <= 0:
                self.revive_after = None
                self.death_message = None
                for other in self.game.players:
                    if self not in other.blocks and other != self:
                        other.blocks.append(self)
            return

        direction = ['up', 'down'][self.engine.gravity_constant < 0]
        if abs(self.center_x - self.last_x) < 1:
            name = f'walk_forward_{direction}'
        elif self.engine.can_jump():
            name = f'walk_right_{self.num}_{direction}'
        else:
            name = f'jump_{self.num}'
        self.texture = self.all_textures[name]

        self.last_x = self.center_x

        gems = arcade.check_for_collision_with_list(self, self.game.gems)
        for gem in gems:
            play_sound_effect('gem')
            self.add_gem(gem.colour)
            gem.place()

        spikes = arcade.check_for_collision_with_list(self, self.game.spikes)
        if spikes:
            self.game.game_over('Hit a Spike', self)
            return

        if self.bottom < 32:
            self.bottom = 32
        elif self.top > HEIGHT - TOP - 16:
            self.top = HEIGHT - TOP - 16

        self.change_x = self.speed
        ideal = self.game.left + WIDTH // 5
        if self.center_x < ideal:
            self.change_x *= 1.1
        elif self.center_x > ideal:
            self.change_x *= 0.9
        self.engine.update()
        self.change_x = 0

        self.time_since_change += 1
        if self.time_since_change > 6:
            self.time_since_change = 0
            self.num += 1
            self.num %= 4

    def draw(self):
        """Draw the sprite and it's boxes to the screen."""
        for box in self.boxes:
            box.draw()
        if self.revive_after is None:
            self.alpha = 255
        else:
            self.alpha = 128
        super().draw()

    def add_gem(self, colour: str):
        """Add a gem and process points."""
        for box in self.boxes:
            if not box.colour:
                box.add_gem(colour)
                break

        colours = [box.colour for box in self.boxes if box.colour]
        counts = {'r': 0, 'b': 0, 'y': 0}
        for colour in colours:
            if colour == 'w':
                for key in counts:
                    counts[key] += 1
            elif colour in counts:
                counts[colour] += 1
        all_three = None
        for colour in counts:
            if counts[colour] >= 3:
                all_three = colour
        if all_three:
            self.score += 1
            self.remove_three(all_three)
            return
        over = False
        size = 5 - colours.count('p')
        unique = sum(1 for i in 'rby' if (i in colours))
        if len(colours) == 5:
            over = True
        elif size < 3:
            over = True
        elif size - unique < 2:
            over = True
        if over:
            self.game.game_over('Inventory Full', self)

    def remove_three(self, colour: str):
        """Once notified that there are three of some colour, remove them."""
        play_sound_effect('match')
        removed = 0
        for box in self.boxes:
            if box.colour == colour:
                box.remove_gem()
                removed += 1
                if removed == 3:
                    return
        for box in self.boxes:
            if box.colour == 'w':
                box.remove_gem()
                removed += 1
                if removed == 3:
                    return
