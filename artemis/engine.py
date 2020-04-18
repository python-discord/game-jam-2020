import arcade


class BiDirectionalPhysicsEnginePlatformer(arcade.PhysicsEnginePlatformer):
    def can_jump(self, y_distance=5):
        if self.gravity_constant > 0:
            return super().can_jump()

        self.player_sprite.center_y += y_distance
        hit_list = arcade.physics_engines.check_for_collision_with_list(
            self.player_sprite, self.platforms
        )
        self.player_sprite.center_y -= y_distance

        if len(hit_list) > 0:
            self.jumps_since_ground = 0

        if (
                len(hit_list) > 0 or self.allow_multi_jump
                and self.jumps_since_ground < self.allowed_jumps
                ):
            return True
        else:
            return False
