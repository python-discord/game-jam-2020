import arcade

from .constants import (
    BLOCK_LEN,
    FLOOR_LENGTH,
    TEXTURE_SIZE,
    GRAVITY,
    GROUND_CONTROL,
    AIR_CONTROL,
    PLAYER_MOVEMENT_SPEED,
    JUMP_FORCE,
    JUMP_COUNT,
    DASH_DISTANCE,
    RIGHT,
    LEFT,
    JUMP_VELOCITY_BONUS,
    DASH_COUNT,
    VIEWPORT_MARGIN
)
from .player import Player
from .sprite import Sprite
from .tile_image import tiles
from .utils import sweep_trace


class GameState:
    """Represent the state of the current game, and manage it."""

    def __init__(self, game):
        self.view_left = 0
        self.view_bottom = 0
        self.game = game

        self.level_geometry = arcade.SpriteList()  # Have collisions
        self.level_objects = arcade.SpriteList()  # Doesn't have collision

        self.player = Player(scale=0.99)
        for tile in (tiles.player_white, tiles.player_red, tiles.player_green, tiles.player_blue):
            self.player.append_texture(tile.texture)
        self.player.set_texture(0)

        self.player.center_x = 200
        self.player.center_y = 200

        self.load_level(0)

        self.engine = arcade.PhysicsEnginePlatformer(self.player, self.level_geometry, GRAVITY)

    def load_level(self, level_id: int) -> None:
        self.level_objects = arcade.SpriteList()
        self.level_geometry = arcade.SpriteList()

        with open(f"levels/level_{level_id}") as file:
            left, bottom = 0, 0
            for line in reversed(file.read().strip().splitlines()):
                for index in range(0, len(line), BLOCK_LEN):
                    block_str = line[index:index+BLOCK_LEN].strip()

                    if block_str:
                        tile = getattr(tiles, block_str)

                        sprite = Sprite.from_texture(tile.texture)
                        sprite.left = left
                        sprite.bottom = bottom

                        if tile.name.startswith("block"):
                            self.level_geometry.append(sprite)
                        else:
                            self.level_objects.append(sprite)

                    left += TEXTURE_SIZE

                left = 0
                bottom += TEXTURE_SIZE

    def on_update(self, delta_time: float) -> None:
        """Handle update event."""
        if self.engine.can_jump():
            self.player.movement_control = GROUND_CONTROL
        else:
            self.player.movement_control = AIR_CONTROL
        self.player.update()
        self.engine.update()
        self.level_objects.update()

        self.update_screen()

    def on_draw(self) -> None:
        """Handle draw event."""
        arcade.start_render()
        self.player.draw()
        self.level_geometry.draw()
        self.level_objects.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        # Pre
        if self.engine.can_jump():
            self.player.dash_count = 0
            self.player.jump_count = 0

        # Dashing
        if key == arcade.key.LSHIFT:
            if not sweep_trace(self.player, DASH_DISTANCE, 0, self.level_geometry):
                can_dash = True

                if not self.engine.can_jump():
                    if self.player.dash_count < DASH_COUNT:
                        self.player.dash_count += 1

                    else:
                        can_dash = False

                if can_dash:
                    self.player.left += DASH_DISTANCE * self.player.direction

        # Jumping
        if key == arcade.key.SPACE:
            self.player.jump_count += 1
            if self.player.jump_count <= JUMP_COUNT:
                self.player.change_y = 0
                self.player.is_jumping = True
                self.player.jump_force = (
                    JUMP_FORCE + abs(self.player.velocity[0]) * JUMP_VELOCITY_BONUS
                )

        # Moving
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.movement_x = -PLAYER_MOVEMENT_SPEED
            self.player.direction = LEFT
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.movement_x = PLAYER_MOVEMENT_SPEED
            self.player.direction = RIGHT

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        # Jumping
        if key == arcade.key.SPACE:
            self.player.is_jumping = False

        # Moving
        if key == arcade.key.LEFT or key == arcade.key.A:
            if self.player.movement_x < 0:
                self.player.movement_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if self.player.movement_x > 0:
                self.player.movement_x = 0

    def update_screen(self):
        """Update viewport and scroll camera.

        From https://arcade.academy/examples/sprite_move_scrolling.html#sprite-move-scrolling"""
        # Keep track of if we changed the boundary. We don't want to call the
        # set_viewport command if we didn't change the view port.
        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + self.game.width - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + self.game.height - VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                self.game.width + self.view_left,
                                self.view_bottom,
                                self.game.height + self.view_bottom)
