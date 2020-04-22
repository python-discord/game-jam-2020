
import arcade
from Entity import Entity, Tex

class Mob(Entity):

    def __init__(self, tex: Tex, x: float, y: float):
        super().__init__(tex, x, y)

    def update(self):
         
        if self.change_x != 0:
            self.move(self.change_x, 0)
        
        if self.change_y != 0:
            self.move(0, self.change_y)

    def move(self, dx: float, dy: float):
        
        if dy != 0:
            self.center_y += dy

            collision_list_y = arcade.check_for_collision_with_list(self, self.level.tile_list)

            for entity in collision_list_y:
                if self.intersects(entity):
                    if self.change_y > 0:
                        self.center_y = entity.center_y - self.width
                    elif self.change_y < 0:
                        self.center_y = entity.center_y + entity.width
                    self.change_y = 0

        if dx != 0:

            self.center_x += dx
            collision_list_x = arcade.check_for_collision_with_list(self, self.level.tile_list)

            for entity in collision_list_x:

                if self.intersects(entity):
                    if self.change_x > 0:
                        self.center_x = entity.center_x - self.width
                    elif self.change_x < 0:
                        self.center_x = entity.center_x + entity.width
                    self.change_x = 0

