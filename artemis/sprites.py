"""Other sprites for the game view."""
from __future__ import annotations
import arcade
import random
import typing

from constants import ASSETS, HEIGHT, SCALING, SIDE, TOP, WIDTH
import game
import multiplayer


def game_type() -> typing.Type:
    """Game or MultiplayerGame typing annotation.

    Function rather than variable to prevent circular imports.
    """
    return typing.Union[game.Game, multiplayer.MultiplayerGame]


class Gem(arcade.Sprite):
    """A gem for the user to collect."""

    TEXTURES = 'rbywp'

    def __init__(self, game: game_type(), image: str = ASSETS + 'gem_{}.png'):
        """Load textures and store parameters."""
        super().__init__(image.format('w'), SCALING * 0.25)
        self.textures = []
        for texture in Gem.TEXTURES:
            self.textures.append(arcade.load_texture(
                image.format(texture)
            ))
        self.game = game
        self.game.gems.append(self)
        self.place()
        self.center_x += WIDTH

    def get_texture(self) -> arcade.Texture:
        """Get a random texture."""
        progress = self.game.left / WIDTH
        white_chance = max(4, 20 - progress / 2)
        pink_chance = 20 - white_chance
        common_chance = 30
        weights = [
            common_chance, common_chance, common_chance, white_chance,
            pink_chance
        ]
        self.colour = random.choices(Gem.TEXTURES, weights=weights)[0]
        return self.textures[Gem.TEXTURES.index(self.colour)]

    def place(self):
        """Reposition the gem so that it does not overlap."""
        self.texture = self.get_texture()
        self.center_x = (
            self.game.left + WIDTH + random.randrange(SIDE, SIDE * 2)
        )
        self.center_y = random.randrange(HEIGHT - TOP)
        overlapping = True
        while overlapping:
            overlapping = False
            for others in (self.game.blocks, self.game.gems,
                           self.game.spikes):
                if arcade.check_for_collision_with_list(self, others):
                    overlapping = True
                    self.center_y = random.randrange(HEIGHT - TOP)
                    break

    def reposition(self):
        """Choose a random position for the gem."""
        self.center_x = random.randrange(WIDTH)
        self.center_y = random.randrange(HEIGHT - TOP)

    def update(self):
        """Reposition the gem if necessary."""
        if self.center_x < self.game.left - SIDE:
            self.place()
        for others in (self.game.blocks, self.game.gems):
            if arcade.check_for_collision_with_list(self, others):
                self.reposition()


class Block(arcade.Sprite):
    """A block on the top or bottom."""

    def __init__(self, game: game_type(), x: int, y: int, up: bool,
                 image: str = ASSETS + 'block.png', scale: float = SCALING):
        """Set up the block."""
        super().__init__(image, center_x=x, center_y=y, scale=scale)
        self.game = game
        game.blocks.append(self)
        self.spike = None
        self.up = up

    def should_place_spike(self) -> bool:
        """Randomly decide whether to place a spike.

        Based on game progression.
        """
        progress = (self.game.left / WIDTH) or 1
        chance_in = int(max(10, 250 / progress))
        return not random.randrange(chance_in)

    def can_place_spike(self) -> bool:
        """Check if we can place a spike.

        (If the block is far enough away from other spikes).
        """
        for spike in self.game.spikes:
            if self.center_x in range(int(spike.center_x - self.width * 5),
                                      int(spike.center_x + self.width * 5)):
                return False
        return True

    def reposition(self):
        """Move the block along."""
        self.center_x += WIDTH + SIDE * 2

    def update(self):
        """Move the block along if it goes off the screen."""
        if self.center_x < self.game.left - SIDE:
            self.reposition()
            if self.spike:
                self.spike.remove_from_sprite_lists()
                self.spike = None
            if self.should_place_spike() and self.can_place_spike():
                self.spike = Spike(self, self.up)
                self.game.spikes.append(self.spike)


class RandomBlock(Block):
    """A block between the top and bottom rows of blocks."""

    def __init__(self, game: game_type()):
        """Create a block and decide a position."""
        super().__init__(
            game, 0, 0, bool(random.randrange(2)), scale=SCALING * 2
        )
        self.total_reposition()
        self.reposition()

    def find_y(self):
        """Find a new y position."""
        range_pixels = HEIGHT - TOP
        range_widths = range_pixels // self.width
        position_widths = random.randrange(range_widths + 1)
        self.center_y = position_widths * self.width

    def reposition(self):
        """Find a new position."""
        self.center_x += WIDTH + random.randrange(SIDE, SIDE * 2)
        self.reposition_y()

    def reposition_y(self):
        """Find a valid value for y."""
        attempts = 5
        overlapping = True
        while attempts and overlapping:
            overlapping = False
            attempts -= 1
            self.find_y()
            for others in (self.game.blocks, self.game.gems,
                           self.game.spikes):
                if arcade.check_for_collision_with_list(self, others):
                    overlapping = True
                    break
            # minimum distance between blocks that aren't touching
            min_dist = 200 * SCALING
            left_bound = self.left - min_dist
            right_bound = self.right + min_dist
            for block in self.game.blocks:
                close_enough = (
                    left_bound < block.left < right_bound
                    or left_bound < block.right < right_bound
                )
                far_enough = (
                    1 < self.bottom - block.top < min_dist
                    or 1 < block.bottom - self.top < min_dist
                )
                if close_enough and far_enough:
                    overlapping = True
                    break
            if not overlapping:
                break
        if not attempts:
            self.center_y = HEIGHT * 2    # go off the screen till next time
        self.up = random.randrange(2)

    def total_reposition(self):
        """Choose a new position for the block."""
        self.center_x = random.randrange(WIDTH)
        self.center_y = random.randrange(HEIGHT - TOP)

    def update(self):
        """Reposition if necessary."""
        super().update()
        for others in (self.game.blocks, self.game.gems):
            if arcade.check_for_collision_with_list(self, others):
                self.reposition_y()


class Spike(arcade.Sprite):
    """A spike, which kills the player upon contact."""

    def __init__(self, block: Block, up: bool,
                 image: str = ASSETS + 'spikes_{}.png'):
        """Set up initial values."""
        image = image.format(['down', 'up'][up])
        if isinstance(block, RandomBlock):
            scale = SCALING * 2
        else:
            scale = SCALING
        super().__init__(image, center_x=block.center_x, scale=scale)
        if up:
            self.bottom = block.top
        else:
            self.top = block.bottom
        self.block = block

    def update(self):
        """Make sure the spike is in the correct position."""
        self.center_x = self.block.center_x
        blocks = arcade.check_for_collision_with_list(
            self, self.block.game.blocks
        )
        for block in blocks:
            if block != self.block:
                self.remove_from_sprite_lists()
                return
