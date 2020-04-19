
import arcade

TILE_SIZE = 16
    
class Tex:
    def __init__(self, filename: str, image_x: float, image_y: float, image_size: float):
        self.filename = filename
        self.image_x = image_x
        self.image_y = image_y
        self.image_size = image_size

class Entity(arcade.Sprite):
    
    def __init__(self, tex: Tex, x: float, y: float):
        super().__init__(tex.filename, 1, tex.image_x, tex.image_y, tex.image_size, tex.image_size)

        self.x = x
        self.y = y

        self.left = x
        self.bottom = y

    def intersects(self, entity):
        pass

ROCK_TILE = Tex("Salami/spritesheet.png", 0, 0, TILE_SIZE)
PLAYER = Tex("Salami/spritesheet.png", TILE_SIZE, 0, TILE_SIZE)