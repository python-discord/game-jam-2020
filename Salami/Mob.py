
import arcade
from Entity import Entity, Tex

from Constants import TILE_SIZE

class Mob(Entity):

    def __init__(self, texture, x: float, y: float):
        super().__init__(texture, x, y)

    def update(self):
         
        if self.change_x != 0:
            self.move(self.change_x, 0)
        
        if self.change_y != 0:
            self.move(0, self.change_y)

    def move(self, dx: float, dy: float):
        
        if dy != 0:
            self.center_y += dy

            collision_list_y = self.level.get_tiles(
                int(self.left / TILE_SIZE),
                int(self.bottom / TILE_SIZE),
                int(self.right / TILE_SIZE),
                int(self.top / TILE_SIZE))
            # collision_list_y = arcade.check_for_collision_with_list(self, self.level.tile_list)

            for entity in collision_list_y:
                if not entity.is_solid:
                    continue
                if self.intersects(entity):
                    if self.change_y > 0:
                        self.center_y = entity.center_y - self.height
                    elif self.change_y < 0:
                        self.center_y = entity.center_y + entity.height
                    self.collided(entity, 0, dy)

        if dx != 0:

            self.center_x += dx

            collision_list_x = self.level.get_tiles(
                int(self.left / TILE_SIZE),
                int(self.bottom / TILE_SIZE),
                int(self.right / TILE_SIZE),
                int(self.top / TILE_SIZE))

            # collision_list_x = arcade.check_for_collision_with_list(self, self.level.tile_list)

            for entity in collision_list_x:
                if not entity.is_solid:
                    continue
                if self.intersects(entity):
                    if self.change_x > 0:
                        self.center_x = entity.center_x - self.width
                    elif self.change_x < 0:
                        self.center_x = entity.center_x + entity.width
                    self.collided(entity, dx, 0)

    def collided(self, entity, dx, dy):
        if dx != 0:
            self.change_x = 0
        if dy != 0:
            self.change_y = 0