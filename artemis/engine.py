"""Module for the physics engine."""
import arcade


class BiDirectionalPhysicsEnginePlatformer(arcade.PhysicsEnginePlatformer):
    """The pyhsics engine.

    A slightly modified version of arcade's PhysicsEnginePlatformer, adding
    support for detection of platforms above the player, as well as below.
    """

    def can_jump(self, y_distance: int = 5) -> bool:
        """Check if the player can jump ie. if they are on a platform."""
        if self.gravity_constant > 0:
            return super().can_jump()

        self.player_sprite.center_y += y_distance
        hit_list = arcade.physics_engines.check_for_collision_with_list(
            self.player_sprite, self.platforms
        )
        self.player_sprite.center_y -= y_distance

        if len(hit_list) > 0:
            self.jumps_since_ground = 0

        return (
            len(hit_list) > 0 or self.allow_multi_jump
            and self.jumps_since_ground < self.allowed_jumps
        )
