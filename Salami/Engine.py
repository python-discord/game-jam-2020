
class Engine:

    def __init__(self, entities, tiles, gravity: float=0.0):
        
        self.entities = entities
        self.tiles = tiles

        self.gravity = gravity

    def update(self, delta):
        
        for entity in self.entities:
            if not entity.flying:
                entity.change_y -= self.gravity

            entity.update()

    def check_for_collision(self):
        pass

    