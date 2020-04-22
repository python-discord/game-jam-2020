
from Entity import Entity

class Tile(Entity):

    def __init__(self, tex, x, y):

        super().__init__(tex, x, y)

        self.flying = True
    
    

    def interact(self, entity):
        pass