
from Tile import Tile
from Entity import Texs

from Constants import TILE_SIZE

ROOM_WIDTH = 15
ROOM_HEIGHT = 12

LEVEL_WIDTH = 60
LEVEL_HEIGHT = 36

def generateLevel(level):
    generateRoom(level, 0, 0)
    generateRoom(level, ROOM_WIDTH + 1, 0)
    generateRoom(level, 0, ROOM_HEIGHT + 1)
    generateRoom(level, ROOM_WIDTH + 1, ROOM_HEIGHT + 1)

def generateRoom(level, x, y):
    drawLine(level, x, y, x + ROOM_WIDTH, y)
    drawLine(level, x + ROOM_WIDTH, y, x + ROOM_WIDTH, y + ROOM_HEIGHT)
    drawLine(level, x, y, x, y + ROOM_HEIGHT)

def drawLine(level, x0, y0, x1, y1):
    for x in range(x0 - 1, x1):
        tile = Tile(Texs.ROCK_TILE, x * TILE_SIZE, y0 * TILE_SIZE)
        level.add_entity_to_list(tile, level.tile_list)

    for y in range(y0 - 1, y1):
        tile = Tile(Texs.ROCK_TILE, x0 * TILE_SIZE, y * TILE_SIZE)
        level.add_entity_to_list(tile, level.tile_list)

def drawRect(level, x0, y0, x1, y1):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            tile = Tile(Texs.ROCK_TILE, x * TILE_SIZE, y * TILE_SIZE)
            level.add_entity_to_list(tile, level.tile_list)