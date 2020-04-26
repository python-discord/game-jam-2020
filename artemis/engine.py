"""Module for the physics engine."""
import arcade

import game
import player


def check_for_collision(sprite1: arcade.Sprite,
                        sprite2: arcade.Sprite) -> bool:
    """Check for collision between two sprites.

    Used instead of Arcade's default implementation as we need a hack to
    return False if there is just a one pixel overlap, if it's not
    multiplayer...
    """
    allowed_overlap = 0
    if isinstance(sprite1, player.Player):
        if isinstance(sprite1.game, game.Game):
            allowed_overlap = 1
    x_collision = (
        sprite1.right - allowed_overlap > sprite2.left + allowed_overlap
        and sprite1.left + allowed_overlap < sprite2.right - allowed_overlap
    )
    if not x_collision:
        return False
    return (
        sprite1.top - allowed_overlap > sprite2.bottom + allowed_overlap
        and sprite1.bottom + allowed_overlap < sprite2.top - allowed_overlap
    )


def check_for_collision_with_list(sprite: arcade.Sprite,
                                  sprite_list: arcade.SpriteList
                                  ) -> arcade.SpriteList:
    """Check for collision between a sprite and a spritelist.

    Used instead of Arcade's default implementation as we need a hack to
    return False if there is just a one pixel overlap, if it's not
    multiplayer...
    """
    overlapping: arcade.SpriteList = arcade.SpriteList()
    for other in sprite_list:
        if check_for_collision(sprite, other):
            overlapping.append(other)
    return overlapping


def _circular_check(player: arcade.Sprite, walls: arcade.SpriteList):
    """Guess our way out of a collision."""
    original_x = player.center_x
    original_y = player.center_y

    vary = 1
    while True:
        last_x = player.center_x
        last_y = player.center_y
        try_list = [[original_x + vary, original_y],
                    [original_x - vary, original_y],
                    ]

        for my_item in try_list:
            x, y = my_item
            player.center_x = x
            player.center_y = y
            check_hit_list = check_for_collision_with_list(
                player, walls
            )
            if len(check_hit_list) == 0:
                return
        vary += 1
    player.center_x = last_x
    player.center_y = last_y


def _move_sprite(moving_sprite: arcade.Sprite, walls: arcade.SpriteList):
    # Rotate
    moving_sprite.angle += moving_sprite.change_angle

    hit_list = check_for_collision_with_list(moving_sprite, walls)

    if len(hit_list) > 0:
        # Resolve any collisions by this weird kludge
        _circular_check(moving_sprite, walls)

    # --- Move in the y direction
    moving_sprite.center_y += moving_sprite.change_y

    # Check for wall hit
    hit_list_x = check_for_collision_with_list(moving_sprite, walls)
    # print(f"Post-y move {hit_list_x}")

    # If we hit a wall, move so the edges are at the same point
    if len(hit_list_x) > 0:
        if moving_sprite.change_y > 0:
            while check_for_collision_with_list(moving_sprite, walls):
                moving_sprite.center_y -= 1
        elif moving_sprite.change_y < 0:
            while check_for_collision_with_list(moving_sprite, walls):
                moving_sprite.center_y += 1

        moving_sprite.change_y = min(0.0, hit_list_x[0].change_y)

    moving_sprite.center_y = round(moving_sprite.center_y, 2)

    # --- Move in the x direction
    moving_sprite.center_x += moving_sprite.change_x

    check_again = True
    while check_again:
        check_again = False
        # Check for wall hit
        hit_list_y = check_for_collision_with_list(moving_sprite, walls)

        # If we hit a wall, move so the edges are at the same point
        if len(hit_list_y) > 0:
            change_x = moving_sprite.change_x
            if change_x > 0:
                while check_for_collision_with_list(moving_sprite,
                                                    walls):
                    moving_sprite.center_x -= 1

            elif change_x < 0:
                while check_for_collision_with_list(moving_sprite,
                                                    walls):
                    moving_sprite.center_x += 1

            else:
                raise AssertionError(
                    "Error, x collision while player wasn't moving.\n"
                    "Make sure you aren't calling multiple updates, like "
                    "a physics engine update and an all sprites list update."
                )


class PhysicsEngine(arcade.PhysicsEnginePlatformer):
    """The pyhsics engine.

    A slightly modified version of arcade's PhysicsEnginePlatformer, adding
    support for detection of platforms above the player, as well as below.
    """

    def update(self):
        """Move everything and resolve collisions."""
        self.player_sprite.change_y -= self.gravity_constant
        _move_sprite(self.player_sprite, self.platforms)

    def can_jump(self, y_distance: int = 5) -> bool:
        """Check if the player can jump ie. if they are on a platform."""
        if self.gravity_constant > 0:
            return super().can_jump()

        self.player_sprite.center_y += y_distance
        hit_list = check_for_collision_with_list(
            self.player_sprite, self.platforms
        )
        self.player_sprite.center_y -= y_distance

        if len(hit_list) > 0:
            self.jumps_since_ground = 0

        return (
            len(hit_list) > 0 or self.allow_multi_jump
            and self.jumps_since_ground < self.allowed_jumps
        )
