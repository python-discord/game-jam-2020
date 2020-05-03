
from Constants import TILE_SIZE

class Engine:

    def __init__(self, entities, tiles, level, gravity: float=0.0):
        
        self.entities = entities
        self.tiles = tiles
        self.level = level

        self.gravity = gravity

    def update(self):
        
        for entity in self.entities:
            if entity.removed:
                self.entities.remove(entity)
                continue
            if not entity.flying:
                entity.change_y -= self.gravity

            entity.update()

    def check_for_collision(self):
        pass

    def can_jump(self, entity, y_dist = 1):
        x0 = int(entity.left / TILE_SIZE)
        y0 = int(entity.bottom / TILE_SIZE)
        x1 = int(entity.right / TILE_SIZE)
        y1 = int(entity.top / TILE_SIZE)

        tiles = self.level.get_tiles(x0, y0, x1, y1)

        entity.center_y -= y_dist

        for tile in tiles:
            if entity.intersects(tile):
                return True

        entity.center_y += y_dist
        
        return False