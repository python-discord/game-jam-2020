import typing as t

import arcade
import PIL

from .constants import TEXTURES_AND_COLORS, BLOCK_WIDTH, BLOCK_HEIGHT


def create_textures() -> t.List[arcade.Texture]:
    """Create textures based on constants dictionary."""
    textures = []
    for t in TEXTURES_AND_COLORS.values():
        if isinstance(t, str):
            textures.append(arcade.load_texture(t))
        elif isinstance(t, tuple):
            img = PIL.Image.new("RGB", (BLOCK_WIDTH, BLOCK_HEIGHT), t)
            textures.append(arcade.Texture(str(t), image=img))
    return textures
