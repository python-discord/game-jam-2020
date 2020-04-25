
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

TEMPLATE_WIDTH = 7
TEMPLATE_HEIGHT = 5

ROOM_TEMPLATES = [
    [
        [1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,3,0,0,3,3,0],
        [2,2,1,1,2,2,1]
    ],
    [
        [1,0,3,3,0,0,1],
        [0,0,2,2,2,0,0],
        [0,0,0,0,0,0,0],
        [0,3,0,0,0,2,2],
        [2,2,1,1,2,2,2],
    ]
]


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.tile_x = x * ROOM_WIDTH
        self.tile_y = y * ROOM_HEIGHT
        self.prev_room = None

def generateLevel(level, x: int, y: int):
    level.rooms.append(Room(x, y))
    dirs = []
    depth = 0
    prev_index = 0
    prev_room = Room(x, y)
    curr_room = Room(x, y)
    tries = 0

    while depth < LEVEL_DEPTH:
        rand_dir = random.randint(0, 99)
        direction = DIRS[rand_dir % 2] if rand_dir < 60 else DIRS[rand_dir % len(DIRS)]
        curr_room = Room(prev_room.x + direction[0], prev_room.y + direction[1])
        curr_dir = DRAW_DIR[direction]
        if curr_room not in level.rooms:
            curr_room.prev_room = prev_room
            level.rooms.append(curr_room)
            dirs.append(curr_dir)
            prev_room = curr_room
            prev_index = len(level.rooms) - 1
            depth += 1
            print(f"Added room at {curr_room.x}, {curr_room.y} | Tries: {tries}")
            tries = 0
        else:
            if prev_index >= 0:
                prev_index -= 1
                prev_room = level.rooms.get(prev_index)
            else:
                tries += 1
                if tries > MAX_TRIES:
                    print(f"No rooms to put rooms | Tries: {tries}")
                    break
    # print(rooms)
    # print(dirs)

    for i, room in enumerate(level.rooms):
        room_x = room.x * ROOM_WIDTH
        room_y = room.y * ROOM_HEIGHT
        # print(room_x, room_y, room_x + ROOM_WIDTH - 1, room_y + ROOM_HEIGHT - 1)

        # generateRoom(level, room_x, room_y)

        for x in range(0, 3):
            for y in range(0, 3):
                drawTemplate(
                    level,
                    room_x + x * TEMPLATE_WIDTH,
                    room_y + y * TEMPLATE_HEIGHT,
                    ROOM_TEMPLATES[0])

    # for i, room in enumerate(rooms):
    #     direction = dirs[i if i < len(rooms) - 1 else i - 1]
    #     x = room[0] * ROOM_WIDTH
    #     y = room[1] * ROOM_HEIGHT

    #     if direction == 0:
    #         x_pos = random.randint(1, ROOM_WIDTH - 2)
    #         removeRect(level, x + x_pos, y + ROOM_HEIGHT, x + x_pos + 1, y + ROOM_HEIGHT + 1)
    #     if direction == 1:
    #         removeRect(level, x + ROOM_WIDTH - 1, y + 1, x + ROOM_WIDTH, y + 4)
    #     if direction == 2:
    #         x_pos = random.randint(1, ROOM_WIDTH - 2)
    #         removeRect(level, x + x_pos, y - 1, x + x_pos + 1, y)
    #     if direction == 3:
    #         removeRect(level, x - 1, y + 1, x, y + 4)


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

def generateRoom(level, x, y):
    
    # Draw the room boundaries
    drawLine(level, x, y + ROOM_HEIGHT, x + ROOM_WIDTH, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])
    drawLine(level, x + ROOM_WIDTH, y, x + ROOM_WIDTH, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])
    drawLine(level, x, y, x + ROOM_WIDTH, y, Textures.SPRITESHEET[1])
    drawLine(level, x, y, x, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])

    # if direction == 0:
    #     removeRect(level, x + 1, y + ROOM_HEIGHT - 1, x + 2, y + ROOM_HEIGHT)
    # if direction == 1:
    #     removeRect(level, x + ROOM_WIDTH - 2, y + 1, x + ROOM_WIDTH - 1, y + 2)
    # if direction == 2:
    #     x_pos = random.randint(1, ROOM_WIDTH - 2)
    #     removeRect(level, x + x_pos, y - 1, x + x_pos + 1, y)
    # if direction == 3:
    #     removeRect(level, x - 1, y + 1, x, y + 2)

def drawTemplate(level, x_pos, y_pos, template):
    for y in range(TEMPLATE_HEIGHT):
        for x in range(TEMPLATE_WIDTH):
            type = template[y][x]
            tile_x = (x_pos + x) * TILE_SIZE
            tile_y = (y_pos + TEMPLATE_HEIGHT - y) * TILE_SIZE
            if type == 0:
                # continue
                level.remove_tile(x_pos + x, y_pos + TEMPLATE_HEIGHT - y)
            elif type == 1:
                level.add_tile(Tile(Textures.SPRITESHEET[0], tile_x, tile_y))
            elif type == 2:
                level.add_tile(Tile(Textures.SPRITESHEET[1], tile_x, tile_y))
            elif type == 3:
                level.add_tile(Tile(Textures.SPRITESHEET[2], tile_x, tile_y, False))

def drawLine(level, x0, y0, x1, y1, tex):
    if x0 != x1:
        for x in range(x0, x1):
            tile = Tile(tex, x * TILE_SIZE, y0 * TILE_SIZE)
            level.add_tile(tile)

    if y0 != y1:
        for y in range(y0, y1):
            tile = Tile(tex, x0 * TILE_SIZE, y * TILE_SIZE)
            level.add_tile(tile)

def removeLine(level, x0, y0, x1, y1):
    for x in range(x0, x1 + 1):
        level.remove_tile(x, y0)

    for y in range(y0, y1 + 1):
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