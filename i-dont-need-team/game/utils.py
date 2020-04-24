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
            textures.append(arcade.load_texture(t))
        elif isinstance(te, tuple):
            img = PIL.Image.new("RGB", (BLOCK_WIDTH, BLOCK_HEIGHT), te)
            textures.append(arcade.Texture(str(te), image=img))
    return textures


def create_board() -> t.List[t.List[int]]:
    """Initialize game board (road)."""
    board = []
    # Add first frame row
    board.append([Blocks.frame for _ in range(BLOCKS_AMOUNT_X)])
    # Create other rows
    for _ in range(BLOCKS_AMOUNT_Y - 2):  # Remove 2 frames rows
        board.append(
            [Blocks.frame]
            + [Blocks.empty for _ in range(BLOCKS_AMOUNT_X - 2)]
            + [Blocks.frame]
        )
    # Add one more frame row
    board.append([Blocks.frame for _ in range(BLOCKS_AMOUNT_X)])
    return board
