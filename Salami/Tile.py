
from Entity import Entity

class Tile(Entity):

    def __init__(self, texture, x, y, is_solid: bool=True):
        super().__init__(texture, x, y)

        self.flying = True
        self.is_solid = is_solid
    

    def interact(self, entity):
        pass