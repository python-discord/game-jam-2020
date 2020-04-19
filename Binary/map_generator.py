import random

SCALE_FACTOR = 4
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_ROOM_NUM = 20
MAX_ROOM_NEIGH = 4
ROOM_W = SCREEN_WIDTH
ROOM_H = SCREEN_HEIGHT


class Room():
    def __init__(self, width, height, color, neighbors, id, parent):
        self.width = width
        self.height = height
        self.color = color
        self.neighbors = neighbors
        self.id = id
        self.parent = parent

def generate(nodes, depth, count):
    # If I reach max depth OR max count then I return
    if(depth > 5 or count > MAX_ROOM_NUM):
        return True
    else:
        #Empty tmp list to hold new nodes
        new_node_list = []
        #Basically iterating through each node I'm feeding to the func, the parents
        for node in nodes:
            #Iteratign through each of its neighbours
            for index,branch in enumerate(node.neighbors):
                #If spot is free and coin flip is ok and I can fit rooms then I generate a new node
                if(branch is None and random.randint(1, 3) != 1 and count < MAX_ROOM_NUM ):
                    #Selecting index (L,U,R,D order)
                    if(index == 0):
                        id = (node.id[0] - 1, node.id[1])
                    elif(index == 1):
                        id = (node.id[0], node.id[1] + 1)
                    elif(index == 2):
                        id = (node.id[0] + 1, node.id[1])
                    elif(index == 3):
                        id = (node.id[0], node.id[1] - 1)
                    #Generating node
                    new_room = Room(ROOM_W, ROOM_H,
                                    (random.randint(0,255), 
                                    random.randint(0,255), 
                                    random.randint(0,255)),
                                    [None]*MAX_ROOM_NEIGH,
                                    id,
                                    node)
                    #Adding it to the parent
                    node.neighbors[index] = new_room
                    new_room.neighbors[index - 2] = node
                    #Adding it to the tmp list
                    new_node_list.append(new_room)
                    count += 1
        depth += 1
        #Recurse!
        generate(new_node_list, depth, count)

"""def traverseAndPrint(node, depth, count):
    if(count == MAX_ROOM_NUM):
        return
    else:
        for n in node:
            if(depth == 0):
                print(n, n.parent, n.id)
            for k in n.neighbors:
                if k is not None:
                    print('_' * depth, k, k.id,k.parent.id)
                    depth += 1
                    count += 1
                    traverseAndPrint([k], depth ,count)

root = Room(ROOM_W, ROOM_H, (random.randrange(0,255), 
                            random.randrange(0,255), 
                            random.randrange(0,255)), 
                            [None]*MAX_ROOM_NEIGH, 
                            (0,0),
                            None)
                        
generate([root], 0, 0)
traverseAndPrint([root], 0, 1)"""