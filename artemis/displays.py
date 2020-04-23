"""Sprites for the game view that are not directly part of game play."""
from __future__ import annotations
import arcade

from constants import ASSETS, HEIGHT, SCALING, TOP
import game
from ui import IconButton


class Box(arcade.Sprite):
    """Display for an inventory slot."""

    def __init__(self, game: game.Game, n: int,
                 image: str = ASSETS + 'box.png'):
        """Set up box."""
        super().__init__(
            image, SCALING * 0.5,
            center_x=(n + 0.6) * 256 * SCALING,
            center_y=HEIGHT - (TOP - game.blocks[0].height // 2) // 2
        )
        self.game = game
        self.alpha = 50
        self.colour = None
        self.gem = None
        game.boxes.append(self)

    def add_gem(self, colour: str):
        """Set the gem in the box."""
        self.colour = colour
        self.gem = BoxGem(self)
        self.alpha = 100
        self.game.gem_added()

    def remove_gem(self):
        """Remove any gems from the box."""
        if self.gem:
            self.gem.remove_from_sprite_lists()
            self.alpha = 50
            self.colour = self.gem = None

    def update(self):
        """Update x with viewport scrolling."""
        self.center_x += self.game.player.speed


class BoxGem(arcade.Sprite):
    """An gem for an inventory slot."""

    def __init__(self, box: Box):
        """Add to a box."""
        super().__init__(
            f'{ASSETS}gem_{box.colour}.png', SCALING * 0.25,
            center_x=box.center_x, center_y=box.center_y
        )
        box.game.others.append(self)
        self.box = box

    def update(self):
        """Update x to stay with box."""
        self.center_x = self.box.center_x


class PausePlay(IconButton):
    """Button for pausing/playing the game."""

    def __init__(self, x: int, y: int, game: game.Game):
        """Set up the button."""
        super().__init__(game, x, y, 'pause', self.go, 32)
        self.game = game
        game.on_mouse_release = self.on_mouse_release

    def go(self):
        """Pause or unpause the game."""
        self.game.paused = not self.game.paused
        image = ['pause', 'play'][self.game.paused]
        self.icon_texture = self.load_texture(image, 16)
        self.game.pause_screen = None
        self.game.window.show_view(self.game)
