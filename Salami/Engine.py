
class Engine:

    def __init__(self, entities, tiles, gravity: float=0.0):
        
        self.entities = entities
        self.tiles = tiles

    def update(self, delta):
        pass

    def check_for_collision(self):
        pass