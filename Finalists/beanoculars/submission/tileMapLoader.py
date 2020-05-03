import arcade
from submission.gameConstants import *


def loadPathTilemap():
    map_name = PATH['maps'] / "maptest.tmx"
    path_layer_name = 'Path'

    my_map = arcade.tilemap.read_tmx(map_name)

    return arcade.tilemap.process_layer(my_map, path_layer_name, TILE_SCALING)
