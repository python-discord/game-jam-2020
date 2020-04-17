import arcade


def load_texture_pair(filename):
    return (
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    )
