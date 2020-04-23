import json
from typing import Any

import arcade
import PIL

with open("assets/images.json") as file:
    data = json.load(file)

TILES = PIL.Image.open("assets/tileset.png")
WIDTH = data.get("width", 64)
HEIGHT = data.get("height", 64)


class Tile:
    def __init__(self, name: str, block_x: int, block_y: int) -> None:
        self.name = name
        self.alias = "".join(part[0] for part in name.split("_"))
        self.w = WIDTH
        self.h = HEIGHT
        self.x = block_x * self.w
        self.y = block_y * self.h

        self.image = TILES.crop((self.x, self.y, self.x + self.w, self.y + self.h))
        self.image.load()
        self.texture = arcade.Texture(self.name, self.image)


class NamedDict(dict):
    def __getattr__(self, attr: str) -> Any:
        name = attr.casefold()
        return self[name]


tiles = NamedDict()

for n, tile_info in enumerate(data.get("tiles", [])):
    tile = Tile(**tile_info)
    tiles.update({tile.name: tile, tile.alias: tile, n: tile})
