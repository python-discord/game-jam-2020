"""Sprites for the game view that are not directly part of game play."""
from __future__ import annotations
import arcade
import typing

from constants import ASSETS, SCALING, SPEED
import game
import multiplayer
import player
from ui import IconButton


class Box(arcade.Sprite):
    """Display for an inventory slot."""

    def __init__(self, x: int, y: int, player: player.Player, scale: float,
                 image: str = ASSETS + 'box.png'):
        """Set up box."""
        super().__init__(image, scale, center_x=x, center_y=y)
        self.alpha = 50
        self.colour: typing.Optional[str] = None
        self.gem: typing.Optional[BoxGem] = None
        self.player = player

    def add_gem(self, colour: str):
        """Set the gem in the box."""
        self.colour = colour
        self.gem = BoxGem(self)
        self.alpha = 100

    def remove_gem(self):
        """Remove any gems from the box."""
        if self.gem:
            self.gem.remove_from_sprite_lists()
            self.alpha = 50
            self.colour = self.gem = None

    def update(self):
        """Update x with viewport scrolling."""
        self.center_x += SPEED
        if self.gem:
            self.gem.update()

    def draw(self):
        """Draw the sprite and it's gem if present."""
        super().draw()
        if self.gem:
            self.gem.draw()


class BoxGem(arcade.Sprite):
    """An gem for an inventory slot."""

    def __init__(self, box: Box):
        """Add to a box."""
        super().__init__(
            f'{ASSETS}gem_{box.colour}.png', SCALING * 0.25,
            center_x=box.center_x, center_y=box.center_y
        )
        self.box = box

    def update(self):
        """Update x to stay with box."""
        self.center_x = self.box.center_x


class PausePlay(IconButton):
    """Button for pausing/playing the game."""

    def __init__(self,
                 x: int, y: int,
                 game: typing.Union[game.Game, multiplayer.MultiplayerGame]):
        """Set up the button."""
        super().__init__(game, x, y, 'pause', self.go, 32)
        self.game = game

    def go(self):
        """Pause or unpause the game."""
        self.game.paused = not self.game.paused
        image = ['pause', 'play'][self.game.paused]
        self.icon_texture = self.load_texture(image, 16)
        self.game.pause_screen = None
        self.game.window.show_view(self.game)
