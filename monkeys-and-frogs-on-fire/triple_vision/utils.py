import arcade


def load_texture_pair(filename):
    return (
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    )


def is_in_radius(center_object: arcade.Sprite, target_object: arcade.Sprite, radius: int) -> bool:
    return (
            abs(center_object.center_x - target_object.center_x) <= radius and
            abs(center_object.center_y - target_object.center_y) <= radius
    )
