from .player import Player
import arcade

FLOOR_LENGTH = 60
FLOOR_TEXTURE_LENGTH = 100
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
PLAYER_MOVEMENT_SPEED = 5
GROUND_CONTROL = 0.5
AIR_CONTROL = 0.05


class GameState:
    """Represent the state of the current game, and manage it."""

    def __init__(self):
        self.level_geometry = arcade.SpriteList()

        self.player = Player('assets/placeholders/player.png')
        self.player.center_x = 200
        self.player.center_y = 200

        for left in range(0, FLOOR_LENGTH * FLOOR_TEXTURE_LENGTH, FLOOR_TEXTURE_LENGTH):
            floor = arcade.Sprite('assets/placeholders/floor.png')
            floor.left = left
            floor.bottom = 0
            self.level_geometry.append(floor)

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
        if key == arcade.key.SPACE:
            if self.engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.movement_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.movement_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            if self.player.movement_x < 0:
                self.player.movement_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if self.player.movement_x > 0:
                self.player.movement_x = 0
