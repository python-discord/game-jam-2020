import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_ROOM_NUM = 20
MAX_ROOM_NEIGH = 4
ROOM_W = SCREEN_WIDTH // MAX_ROOM_NUM
ROOM_H = SCREEN_HEIGHT // MAX_ROOM_NUM
CELL_SIZE = (20, 20)

class Room():
    def __init__(self, width, height, color, neighbors, x, y):
        self.width = width
        self.height = height
        self.color = color
        self.neighbors = neighbors
        self.x = x
        self.y = y


def generate(nodes, depth, count):
    if(depth > 5 and count == MAX_ROOM_NUM):
        return True
    else:
        new_node_list = []
        for node in nodes:
            for index,branch in enumerate(node.neighbors):
                if(branch == None and random.randint(1, 3) != 1 and count < MAX_ROOM_NUM ):
                    if(index == 0):
                        x = node.x - 40
                        y = node.y
                    elif(index == 1):
                        x = node.x
                        y = node.y - 40
                    elif(index == 2):
                        x = node.x + 40
                        y = node.y
                    elif(index == 3):
                        x = node.x
                        y = node.y + 40

                    new_room = Room(ROOM_W, ROOM_H,
                                    (random.randint(0,255), 
                                    random.randint(0,255), 
                                    random.randint(0,255)),
                                    [None]*MAX_ROOM_NEIGH,
                                    x,
                                    y)
                    node.neighbors[index] = new_room
                    new_node_list.append(new_room)
                    count += 1
        depth += 1
        generate(new_node_list, depth, count)
"""
def traverseAndPrint(node, depth, count):
    if(count == MAX_ROOM_NUM):
        return
    else:
        for n in node:
            for k in n.neighbors:
                if k is not None:
                    print('_' * depth, k.name)
                    depth += 1
                    count += 1
                    traverseAndPrint([k], depth ,count)
"""

root = Room(ROOM_W, ROOM_H, (random.randrange(0,255), 
                            random.randrange(0,255), 
                            random.randrange(0,255)), 
                            [None]*MAX_ROOM_NEIGH, 
                            SCREEN_WIDTH // 2, 
                            SCREEN_HEIGHT // 2)
                        
#generate([root], 0, 0)
#traverseAndPrint([root], 0, 1)