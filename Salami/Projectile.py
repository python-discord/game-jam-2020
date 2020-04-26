
from Mob import Mob
from Entity import Entity

class Projectile(Mob):

    def __init__(self, tex, x, y, dx = 0, dy = 0):
        super().__init__(tex, x, y)

        self.change_x = dx
        self.change_y = dy

        self.life = 600
        self.damage = 1
    
    def update(self):
        
        self.life -= 1
        if self.life < 0:
            self.removed = True

        super().update()
    
    def collided(self, entity, dx, dy):
        # self.change_x = 0
        # self.change_y = 0
        # self.flying = True
        self.removed = True