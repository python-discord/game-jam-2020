import typing as t

import arcade
import PIL

from .constants import (
    Blocks,
    BLOCKS_AMOUNT_X,
    BLOCKS_AMOUNT_Y,
    BLOCK_WIDTH,
    BLOCK_HEIGHT,
    TEXTURES_AND_COLORS
)


def create_textures() -> t.List[arcade.Texture]:
    """Create textures based on constants dictionary."""
    textures = []
    for te in TEXTURES_AND_COLORS.values():
        if isinstance(te, str):
            textures.append(arcade.load_texture(te))
        elif isinstance(te, tuple):
            img = PIL.Image.new("RGB", (100, 100), te)
            textures.append(arcade.Texture(str(te), image=img))
    return textures


def create_board() -> t.List[t.List[int]]:
    """Initialize game board (road)."""
    board = []
    # Create rows
    for _ in range(BLOCKS_AMOUNT_Y + 1):
        board.append(
            [Blocks.frame]
            + [Blocks.empty for _ in range(BLOCKS_AMOUNT_X - 2)]
            + [Blocks.frame]
        )
    return board
