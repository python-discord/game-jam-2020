from .constants import (
    FLOOR_LENGTH, FLOOR_TEXTURE_LENGTH, GRAVITY, GROUND_CONTROL, AIR_CONTROL, PLAYER_MOVEMENT_SPEED, JUMP_FORCE,
    JUMP_COUNT, DASH_DISTANCE, RIGHT, LEFT, DASH_COUNT, JUMP_VELOCITY_BONUS
)
from .player import Player
import arcade

from .utils import sweep_trace


class GameState:
    """Represent the state of the current game, and manage it."""

    def __init__(self):
        self.level_geometry = arcade.SpriteList()

        self.player = Player('assets/simple_cube.png')
        self.player.center_x = 200
        self.player.center_y = 200

        for left in range(0, FLOOR_LENGTH * FLOOR_TEXTURE_LENGTH, FLOOR_TEXTURE_LENGTH):
            floor = arcade.Sprite('assets/simple_block.png')
            floor.left = left
            floor.bottom = 0
            self.level_geometry.append(floor)

        obstacle = arcade.Sprite('assets/simple_block.png')
        obstacle.left = 100
        obstacle.bottom = FLOOR_TEXTURE_LENGTH
        self.level_geometry.append(obstacle)

        self.engine = arcade.PhysicsEnginePlatformer(self.player, self.level_geometry, GRAVITY)

    def on_update(self, delta_time: float) -> None:
        """Handle update event."""
        if self.engine.can_jump():
            self.player.movement_control = GROUND_CONTROL
        else:
            self.player.movement_control = AIR_CONTROL
        self.player.update()
        self.engine.update()

    def on_draw(self) -> None:
        """Handle draw event."""
        arcade.start_render()
        self.player.draw()
        self.level_geometry.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # Dashing
        if key == arcade.key.LSHIFT and not self.engine.can_jump():
            if self.player.dash_count > 0 and not sweep_trace(self.player, DASH_DISTANCE, 0, self.level_geometry):
                self.player.left += DASH_DISTANCE * self.player.direction
                self.player.dash_count -= 1
        else:
            self.player.dash_count = DASH_COUNT

        # Jumping
        if self.engine.can_jump():
            self.player.jump_count = 0
        if key == arcade.key.SPACE:
            self.player.jump_count += 1
            if self.player.jump_count <= JUMP_COUNT:
                self.player.change_y = 0
                self.player.is_jumping = True
                self.player.jump_force = JUMP_FORCE + abs(self.player.velocity[0]) * JUMP_VELOCITY_BONUS

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
