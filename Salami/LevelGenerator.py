
import random

import Textures

from Tile import Tile
from Entity import Texs, Tex

from Constants import TILE_SIZE, ROOM_WIDTH, ROOM_HEIGHT

LEVEL_WIDTH = 60
LEVEL_HEIGHT = 36

LEVEL_DEPTH = 24

MAX_TRIES = 8

# DIRS = [
#     [-1, 0], [1, 0]
# ]

DIRS = [
    (-1, 0), (1, 0), (0, -1), (0, 1)
]

DRAW_DIR = {
    (-1, 0): 3,
    (1, 0) : 1,
    (0, -1): 2,
    (0, 1) : 0
}

# DIRS = [
#     [-1, 1] , [0, 1] , [1, 1],
#     [-1, 0] ,          [1, 0],
#     [-1, -1], [0, -1], [1, -1]
# ]

TEMPLATE_WIDTH = 6
TEMPLATE_HEIGHT = 4

ROOM_TEMPLATES = [
    [
        0,0,0,0,0,0,
        0,0,1,1,1,0,
        0,0,0,0,0,0,
        1,1,0,0,0,0,
    ]
]


class Room:
    def __init__(self, x, y, direction, prev_room):
        self.x = x
        self.y = y
        self.direction = direction
        self.prev_room = prev_room

def generateLevel(level, x: int, y: int):

    rooms = [(x, y)]
    dirs = []
    depth = 0
    prev_index = 0
    prev_room = (x, y)
    curr_room = (x, y)
    tries = 0

    while depth < LEVEL_DEPTH:
        rand_dir = random.randint(0, 99)
        direction = DIRS[rand_dir % 2] if rand_dir < 60 else DIRS[rand_dir % len(DIRS)]
        curr_room = (prev_room[0] + direction[0], prev_room[1] + direction[1])
        curr_dir = DRAW_DIR[direction]
        if curr_room not in rooms:
            rooms.append(curr_room)
            dirs.append(curr_dir)
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
                    print("No rooms to put rooms")
                    break
    # print(rooms)
    # print(dirs)

    for i, room in enumerate(rooms):
        room_x = room[0] * ROOM_WIDTH
        room_y = room[1] * ROOM_HEIGHT
        if i < len(rooms) - 1:
            generateRoom(level, room_x, room_y, dirs[i])
        else:
            generateRoom(level, room_x, room_y, dirs[i - 1])

    for i, room in enumerate(rooms):
        direction = dirs[i if i < len(rooms) - 1 else i - 1]
        x = room[0] * ROOM_WIDTH
        y = room[1] * ROOM_HEIGHT

        if direction == 0:
            x_pos = random.randint(1, ROOM_WIDTH - 2)
            removeRect(level, x + x_pos, y + ROOM_HEIGHT, x + x_pos + 1, y + ROOM_HEIGHT + 1)
        if direction == 1:
            removeRect(level, x + ROOM_WIDTH - 1, y + 1, x + ROOM_WIDTH, y + 4)
        if direction == 2:
            x_pos = random.randint(1, ROOM_WIDTH - 2)
            removeRect(level, x + x_pos, y - 1, x + x_pos + 1, y)
        if direction == 3:
            removeRect(level, x - 1, y + 1, x, y + 4)


    # for room in rooms:
    #     x = room[0] * ROOM_WIDTH
    #     y = room[1] * ROOM_HEIGHT
    #     for direction in DIRS:
    #         neighbor_x = room[0] + direction[0]
    #         neighbor_y = room[1] + direction[1]
    #         if (neighbor_x, neighbor_y) in rooms:
    #                 removeRect(level,
    #                     x + (ROOM_WIDTH - 2) * direction[0],
    #                     y + (ROOM_HEIGHT - 3) * direction[1],
    #                     x + (ROOM_WIDTH + 2) * direction[0],
    #                     y + (ROOM_HEIGHT + 1) * direction[1])

                    # removeRect(level, x + ROOM_WIDTH - 1, y + 1, x + ROOM_WIDTH, y + 2)
                    # removeRect(level, x + x_pos, y - 1, x + x_pos + 1, y)
                    # removeRect(level, x - 1, y + 1, x, y + 2)

    # generateRoom(level, 0, 0)
    # generateRoom(level, ROOM_WIDTH + 1, 0)
    # generateRoom(level, 0, ROOM_HEIGHT + 1)
    # generateRoom(level, ROOM_WIDTH + 1, ROOM_HEIGHT + 1)

    # drawLine(level, 0, -1, LEVEL_WIDTH, -1, Tex("Salami/spritesheet.png", 0, 0, TILE_SIZE))
    # drawLine(level, -1, 0, -1, LEVEL_HEIGHT, Tex("Salami/spritesheet.png", 0, 0, TILE_SIZE))

def generateRoom(level, x, y, direction):
    # drawLine(level, x, y + ROOM_HEIGHT, x, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])

    drawLine(level, x, y + ROOM_HEIGHT, x + ROOM_WIDTH, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])
    drawLine(level, x + ROOM_WIDTH, y, x + ROOM_WIDTH, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])
    drawLine(level, x, y, x + ROOM_WIDTH, y, Textures.SPRITESHEET[1])
    drawLine(level, x, y, x, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])

    # if direction == 0:
    #     removeRect(level, x + 1, y + ROOM_HEIGHT, x + 2, y + ROOM_HEIGHT + 1)
    # if direction == 1:
    #     removeRect(level, x + ROOM_WIDTH - 1, y + 1, x + ROOM_WIDTH, y + 2)
    # if direction == 2:
    #     x_pos = random.randint(1, ROOM_WIDTH - 2)
    #     removeRect(level, x + x_pos, y - 1, x + x_pos + 1, y)
    # if direction == 3:
    #     removeRect(level, x - 1, y + 1, x, y + 2)

def drawLine(level, x0, y0, x1, y1, tex):
    for x in range(x0, x1):
        tile = Tile(tex, x * TILE_SIZE, y0 * TILE_SIZE)
        level.add_tile(tile)

    for y in range(y0, y1):
        tile = Tile(tex, x0 * TILE_SIZE, y * TILE_SIZE)
        level.add_tile(tile)

def removeLine(level, x0, y0, x1, y1):
    for x in range(x0, x1):
        level.remove_tile(x, y0)

    for y in range(y0, y1):
        level.remove_tile(x0, y)

def removeRect(level, x0, y0, x1, y1):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            level.remove_tile(x, y)


def drawRect(level, x0, y0, x1, y1):
    for x in range(x0, x1):
        for y in range(y0, y1):
            tile = Tile(Texs.ROCK_TILE, x * TILE_SIZE, y * TILE_SIZE)
            level.add_tile(tile)