
import Textures

from Mob import Mob

class Heart(Mob):
    def __init__(self, x, y):
        super().__init__(Textures.get_texture(4, 9), x, y)

    def update(self):

        if self.intersects(self.level.player):
            self.level.player.heal(3)

        super().update()