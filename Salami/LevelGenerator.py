
import random

import Textures

from Tile import Tile
from Entity import Texs, Tex

from Constants import TILE_SIZE, ROOM_WIDTH, ROOM_HEIGHT

LEVEL_WIDTH = 60
LEVEL_HEIGHT = 36

LEVEL_DEPTH = 4

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
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,3,3,1],
        [2,2,1,1,2,2,1]
    ],
    [
        [1,1,1,1,1,1,1],
        [0,0,0,1,1,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,1,2,2,0,0,0]
    ],
    [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ],
    [
        [1,0,3,3,0,0,1],
        [0,0,2,2,2,0,0],
        [0,0,0,0,0,0,0],
        [0,3,0,0,0,2,2],
        [2,2,1,1,2,2,2]
    ]
]


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.tile_x = x * ROOM_WIDTH
        self.tile_y = y * ROOM_HEIGHT
        
        self.prev_room = None

        self.top_room = None
        self.bottom_room = None
        self.left_room = None
        self.right_room = None

    # def __eq__(self, object):
    #     return self.x == object.x and self.y == object.y
class LevelGen:
    def __init__(self, level):
        
        self.x = 0
        self.y = 0

        self.level = level

        self.generating = False
        self.curr_generate_speed = 0
        self.generate_speed = 24

        self.current_room = None
        self.curr_depth = 0
        self.rooms = {}

    def startGen(self, x: int, y: int):
        self.x = x
        self.y = y
        self.curr_depth = 24
        self.generating = True
        self.current_room = self.rooms.get(x, y)
        if not self.current_room:
            self.current_room = self.addRoom(x, y)

    def update(self):
        if self.generating:
            if self.curr_generate_speed == 0:
                self.generateLevelStep()
                self.curr_generate_speed = self.generate_speed
        if self.curr_generate_speed > 0:
            self.curr_generate_speed -= 1

    def generateLevelStep(self):
        if self.current_room is None:
                self.current_room = self.addRoom(self.x, self.y)
                self.current_room.prev_room = self.current_room
        
        if self.curr_depth == 0:
            print(f"Current depth is zero!")
            return
        
        dirs = []
        for direction in DIRS:
            if not self.rooms.get((self.current_room.x + direction[0], self.current_room.y + direction[1])):
                dirs.append(direction)
        
        if len(dirs) > 0:
            rand_dir = random.randrange(len(dirs))
            new_room = self.addRoom(self.current_room.x + dirs[rand_dir][0], self.current_room.y + dirs[rand_dir][1])
            new_room.prev_room = self.current_room
            self.current_room = new_room

            self.curr_depth -= 1
            if self.curr_depth == 0:
                self.generating = False
            self.drawRoom(new_room)
        else:
            if self.current_room.prev_room is not None or self.current_room.prev_room != self.current_room:
                self.current_room = self.current_room.prev_room
            else:
                self.generating = False
                print(f"Stopped generating: No more rooms to put")

    def drawRoom(self, room):
        room_x = room.x * ROOM_WIDTH
        room_y = room.y * ROOM_HEIGHT

        for x in range(0, 3):
            for y in range(0, 3):
                template = ROOM_TEMPLATES[2]
                if y == 0:
                    
                    template = ROOM_TEMPLATES[0]
                elif y == 2:
                    template = ROOM_TEMPLATES[1] 

                drawTemplate(
                    self.level,
                    room_x + x * TEMPLATE_WIDTH,
                    room_y + y * TEMPLATE_HEIGHT,
                    template)
        
    
    def addRoom(self, x, y):
        if not self.rooms.get((x, y)):
            room = Room(x, y)
            self.rooms[(x, y)] = room
            print(f"Added room at: {x}, {y}")
            return room


def generateLevel(level, x: int, y: int):
    start_room = Room(x, y)
    start_room.prev_room = start_room
    level.rooms.append(start_room)
    dirs = []
    depth = 0
    prev_room = Room(x, y)
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
            depth += 1
            print(f"Added room at {curr_room.x}, {curr_room.y} | Tries: {tries}")
            tries = 0
        else:
            tries += 1
            curr_room = curr_room.prev_room
            prev_room = curr_room.prev_room
            if tries > MAX_TRIES or curr_room is None or curr_room == start_room:
                print(f"No rooms to put rooms | Tries: {tries}")
                break


    for i, room in enumerate(level.rooms):
        # if room.prev_room:
        print(room.x, room.y, room.prev_room.x, room.prev_room.y)

    for i, room in enumerate(level.rooms):
        room_x = room.x * ROOM_WIDTH
        room_y = room.y * ROOM_HEIGHT
        # print(room_x, room_y, room_x + ROOM_WIDTH - 1, room_y + ROOM_HEIGHT - 1)

        # generateRoom(level, room_x, room_y)

        for x in range(0, 3):
            for y in range(0, 3):
                template = ROOM_TEMPLATES[2]
                if y == 0:
                    
                    template = ROOM_TEMPLATES[0]
                elif y == 2:
                    template = ROOM_TEMPLATES[1] 

                drawTemplate(
                    level,
                    room_x + x * TEMPLATE_WIDTH,
                    room_y + y * TEMPLATE_HEIGHT,
                    template)

    # drawLine(level, 0, -1, LEVEL_WIDTH, -1, Tex("Salami/spritesheet.png", 0, 0, TILE_SIZE))
    # drawLine(level, -1, 0, -1, LEVEL_HEIGHT, Tex("Salami/spritesheet.png", 0, 0, TILE_SIZE))

def generateRoom(level, x, y):
    # Draw the room boundaries
    drawLine(level, x, y + ROOM_HEIGHT, x + ROOM_WIDTH, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])
    drawLine(level, x + ROOM_WIDTH, y, x + ROOM_WIDTH, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])
    drawLine(level, x, y, x + ROOM_WIDTH, y, Textures.SPRITESHEET[1])
    drawLine(level, x, y, x, y + ROOM_HEIGHT, Textures.SPRITESHEET[0])

def drawTemplate(level, x_pos, y_pos, template):
    mirrored = False
    # mirrored = True if random.randint(0, 100) > 60 else False
    for y in range(TEMPLATE_HEIGHT):
        for x in range(TEMPLATE_WIDTH):
            type = template[y][x]
            cell_x = (TEMPLATE_WIDTH - x) if mirrored else x
            tile_x = (x_pos + cell_x) * TILE_SIZE
            tile_y = (y_pos + TEMPLATE_HEIGHT - y) * TILE_SIZE
            if type == 0:
                continue
                # level.remove_tile(x_pos + x, y_pos + TEMPLATE_HEIGHT - y)
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