
import random

import Textures

from Tile import Tile
from Enemy import Enemy
from Slime import Slime
from Boss import Boss
from SpikyBall import SpikyBall
from Entity import Texs, Tex
from RoomTemplates import *

from Constants import TILE_SIZE, ROOM_WIDTH, ROOM_HEIGHT

LEVEL_DEPTH = 4

MAX_TRIES = 8

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

START_ROOM = 0
LEVEL_ROOM = 1
BOSS_ROOM = 3


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.tile_x = x * ROOM_WIDTH
        self.tile_y = y * ROOM_HEIGHT

        self.type = LEVEL_ROOM
        
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
        self.generate_speed = 0

        self.current_room = None
        self.curr_depth = 0
        self.max_depth = 4
        self.rooms = {}
        
        self.drawing = False
        self.rooms_to_draw = []
        self.curr_draw_speed = 60
        self.draw_speed = 0

    def startGen(self, x: int, y: int):
        self.x = x
        self.y = y
        self.curr_depth = self.max_depth
        self.generating = True
        self.current_room = self.rooms.get((x, y))
        if self.current_room is None:
            self.current_room = self.addRoom(x, y)
            if not self.current_room.prev_room:
                self.current_room.prev_room = self.current_room
            self.current_room.type = START_ROOM

    def update(self):
        if self.generating:
            if self.curr_generate_speed == 0:
                self.generateLevelStep()
                self.curr_generate_speed = self.generate_speed

        elif self.drawing:
            if len(self.rooms_to_draw) > 0:
                room = self.rooms_to_draw[0]
                self.drawRoom(room)
                self.rooms_to_draw.pop(0)
                self.curr_draw_speed = self.draw_speed
            else:
                self.drawing = False
        
        if self.curr_generate_speed > 0:
            self.curr_generate_speed -= 1
        if self.curr_draw_speed > 0:
            self.curr_draw_speed -= 1

    def generateLevelStep(self):
        # if self.current_room is None:
        #         self.current_room = self.addRoom(self.x, self.y)
        #         self.current_room.prev_room = self.current_room
        
        if self.curr_depth <= 0:
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

            if self.curr_depth <= 0:
                self.current_room.type = BOSS_ROOM
                self.generating = False
                self.drawing = True
        else:
            if self.current_room.prev_room is not None or self.current_room.prev_room != self.current_room:
                self.current_room = self.current_room.prev_room
            else:
                self.generating = False
                self.drawing = True
                print(f"Stopped generating: No more rooms to put")

    def drawRoom(self, room):
        room_x = int(room.x * ROOM_WIDTH)
        room_y = int(room.y * ROOM_HEIGHT)

        for x in range(0, 3):
            for y in range(0, 3):
                template = ROOM_TEMPLATES[2]

                neighbor_rooms = {}
                for direction in DIRS:
                    neighbor = self.rooms.get((room.x + direction[0], room.y + direction[1]))
                    if neighbor is not None:
                        neighbor_rooms[direction] = neighbor
                        
                left = neighbor_rooms.get((-1, 0)) is not None
                bottom = neighbor_rooms.get((0, -1)) is not None
                top = neighbor_rooms.get((0, 1)) is not None
                right = neighbor_rooms.get((1, 0)) is not None

                if y == 0:
                    if x == 1:
                        if bottom:
                            template = getRandTemplate(BOTTOM_OPEN)
                        else:
                            template = getRandTemplate(BOTTOM)
                    elif x == 0:
                        template = getRandTemplate(BOTTOM_LEFT)
                    elif x == 2:
                        template = getRandTemplate(BOTTOM_RIGHT)
                elif y == 1:
                    if x == 0:
                        if left:
                            template = EMPTY
                        else:
                            template = MIDDLE_LEFT[0]
                    elif x == 1:
                        template = MIDDLE_CENTER[0]
                    elif x == 2:
                        if right:
                            template = EMPTY
                        else:
                            template = MIDDLE_RIGHT[0]
                elif y == 2:
                    if x == 1:
                        if top:
                            template = getRandTemplate(TOP_OPEN)
                        else:
                            template = TOP[0]
                    elif x == 0:
                        template = TOP_LEFT[0]
                    elif x == 2:
                        template = TOP_RIGHT[0]

                drawTemplate(
                    self.level,
                    room_x + x * TEMPLATE_WIDTH,
                    room_y + y * TEMPLATE_HEIGHT,
                    template)

        difficulty = self.level.difficulty
        
        while difficulty > 0:
            if room.type == START_ROOM:
                break
            if room.type == BOSS_ROOM:
                entity_x = random.randrange(room_x - 1, room_x + ROOM_WIDTH - 1) * TILE_SIZE
                entity_y = random.randrange(room_y - 1, room_y + ROOM_HEIGHT - 1) * TILE_SIZE
                boss = Boss(entity_x, entity_y, self.level.difficulty)
                self.level.add_entity_to_list(boss, self.level.entities)
                difficulty -= 5
            else:
                enemy_type = random.randint(0, 2)
                
                entity_x = random.randrange(room_x + 1, room_x + ROOM_WIDTH - 1) * TILE_SIZE
                entity_y = random.randrange(room_y + 1, room_y + ROOM_HEIGHT - 1) * TILE_SIZE
                if enemy_type == 0:
                    slem = Slime(Textures.get_texture(3, 2), entity_x, entity_y, self.level.difficulty)
                    self.level.add_entity_to_list(slem, self.level.entities)
                    difficulty -= 1
                elif enemy_type == 1:
                    enemy = Enemy(Textures.get_texture(0, 2), entity_x, entity_y, self.level.difficulty)
                    self.level.add_entity_to_list(enemy, self.level.entities)
                    difficulty -= 1
                else:
                    spiky_ball = SpikyBall(entity_x, entity_y, self.level.difficulty)
                    self.level.add_entity_to_list(spiky_ball, self.level.entities)
                    difficulty -= 1

    
    def addRoom(self, x, y):
        if not self.rooms.get((x, y)):
            room = Room(x, y)
            self.rooms[(x, y)] = room
            self.rooms_to_draw.append(room)
            self.curr_depth -= 1
            print(f"Added room at: {x}, {y} | {self.curr_depth}")
            return room
        return self.rooms.get((x, y))
        
def getRandTemplate(template_list, start: int=0, end: int=0):
    end = end if end != 0 else len(template_list) - 1
    index = random.randint(start, end)
    return template_list[index]


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