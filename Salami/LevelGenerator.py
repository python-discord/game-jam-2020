
import random

from Tile import Tile
from Entity import Texs, Tex

from Constants import TILE_SIZE, ROOM_WIDTH, ROOM_HEIGHT

LEVEL_WIDTH = 60
LEVEL_HEIGHT = 36

LEVEL_DEPTH = 8

MAX_TRIES = 8

DIRS = [
    [-1, 0], [0, -1], [1, 0], [0, 1]
]

# DIRS = [
#     [-1, 1] , [0, 1] , [1, 1],
#     [-1, 0] ,          [1, 0],
#     [-1, -1], [0, -1], [1, -1]
# ]

class Room:
    def __init__(self, x, y, direction, prev_room):
        self.x = x
        self.y = y
        self.direction = direction
        self.prev_room = prev_room

def generateLevel(level, x: int, y: int):
    rooms = [(x, y)]
    depth = 0
    prev_index = 0
    prev_room = (x, y)
    curr_room = (x, y)
    tries = 0
    while depth < LEVEL_DEPTH:
        rand_dir = random.randint(0, len(DIRS) - 1)
        direction = DIRS[rand_dir]
        curr_room = (prev_room[0] + direction[0], prev_room[1] + direction[1])
        if curr_room not in rooms:
            rooms.append(curr_room)
            prev_room = curr_room
            prev_index = len(rooms) - 1
            depth += 1
        else:
            if prev_index >= 0:
                prev_index -= 1
                prev_room = rooms[prev_index]
            else:
                tries += 1
                if tries > MAX_TRIES:
                    break

    for room in rooms:
        generateRoom(level, room[0] * ROOM_WIDTH, room[1] * ROOM_HEIGHT)

    print(rooms)

    # generateRoom(level, 0, 0)
    # generateRoom(level, ROOM_WIDTH + 1, 0)
    # generateRoom(level, 0, ROOM_HEIGHT + 1)
    # generateRoom(level, ROOM_WIDTH + 1, ROOM_HEIGHT + 1)

    # drawLine(level, 0, -1, LEVEL_WIDTH, -1, Tex("Salami/spritesheet.png", 0, 0, TILE_SIZE))
    # drawLine(level, -1, 0, -1, LEVEL_HEIGHT, Tex("Salami/spritesheet.png", 0, 0, TILE_SIZE))

def generateRoom(level, x, y):
    # drawLine(level, x, y + ROOM_HEIGHT, x, y + ROOM_HEIGHT, Texs.ROCK_TILE)
    drawLine(level, x, y, x + ROOM_WIDTH, y, Tex("Salami/spritesheet.png", 0, 0, TILE_SIZE))
    # drawLine(level, x + ROOM_WIDTH, y, x + ROOM_WIDTH, y + ROOM_HEIGHT, Texs.ROCK_TILE)
    # drawLine(level, x, y, x, y + ROOM_HEIGHT, Texs.ROCK_TILE)
    # drawLine(level, x, y + ROOM_HEIGHT, x + ROOM_WIDTH, y + ROOM_HEIGHT, Texs.ROCK_TILE)

def drawLine(level, x0, y0, x1, y1, tex):
    for x in range(x0, x1):
        tile = Tile(tex, x * TILE_SIZE, y0 * TILE_SIZE)
        level.add_entity_to_list(tile, level.tile_list)

    for y in range(y0, y1):
        tile = Tile(tex, x0 * TILE_SIZE, y * TILE_SIZE)
        level.add_entity_to_list(tile, level.tile_list)

def drawRect(level, x0, y0, x1, y1):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            tile = Tile(Texs.ROCK_TILE, x * TILE_SIZE, y * TILE_SIZE)
            level.add_entity_to_list(tile, level.tile_list)