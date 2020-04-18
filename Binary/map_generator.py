import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_ROOM_NUM = 20
MAX_ROOM_NEIGH = 4
ROOM_W = SCREEN_WIDTH // MAX_ROOM_NUM
ROOM_H = SCREEN_HEIGHT // MAX_ROOM_NUM

grid = [[None],[None]]*ROOM_W

class Room():
    def __init__(self, width, height, color, neighbors, name, x, y):
        self.name = name
        self.width = width
        self.height = height
        self.color = color
        self.neighbors = neighbors
        self.x = x
        self.y = y

def generate(list_t):
    if len(list_t) == 20:
        return list_t
    else:
        room_list = list_t
        for room in room_list:
            for index,neigh in enumerate(room.neighbors):
                if(neigh == None and len(room_list) < 20 and random.randrange(1, 3) != 1 and room.neighbors.count(None) > 2):
                    new_room = Room(ROOM_W, ROOM_H, (random.randrange(0,255), 
                                                    random.randrange(0,255), 
                                                    random.randrange(0,255)), 
                                                    [None]*MAX_ROOM_NEIGH, f"node {index}",
                                                    random.randrange(SCREEN_WIDTH // 2 + 10, SCREEN_WIDTH),
                                                    random.randrange(SCREEN_HEIGHT // 2 + 10, SCREEN_HEIGHT))
                    room.neighbors[index] = new_room
                    room_list.append(new_room)
                else:
                    if(len(room_list) < 20):
                        pass
                    else:
                        return room_list
        generate(room_list)

print(len(grid))