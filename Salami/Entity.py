
import arcade

TILE_SIZE = 16


class Tex:

    def __init__(self, filename: str, image_x: float, image_y: float, image_size: float):
        self.filename = filename
        self.image_x = image_x
        self.image_y = image_y
        self.image_size = image_size

class Texs:
    
    ROCK_TILE = Tex("Salami/spritesheet.png", TILE_SIZE, 0, TILE_SIZE)
    PLAYER = Tex("Salami/spritesheet.png", 0, TILE_SIZE * 3, TILE_SIZE)

    BALL = Tex("Salami/spritesheet.png", TILE_SIZE, TILE_SIZE * 5, TILE_SIZE)

    @staticmethod
    def load_textures(filename, image_x, image_y, image_size, times, mirrored: bool=False):
        result = []
        for i in range(times):
            result.append(arcade.load_texture(
                filename,
                image_x * image_size + i * image_size,
                image_y * image_size,
                image_size, image_size,
                mirrored=mirrored))
        return result

class Entity(arcade.Sprite):

    def __init__(self, texture, x: float, y: float):
        super().__init__()

        self.texture = texture

        self.x = x
        self.y = y

        self.left = x
        self.bottom = y

        self.is_solid = False
        self.flying = False

        
        # self.set_hit_box([
        #     [-self.width, -TILE_SIZE_D2],
        #     [-TILE_SIZE_D2, TILE_SIZE_D2],
        #     [TILE_SIZE_D2, TILE_SIZE_D2],
        #     [TILE_SIZE_D2, -TILE_SIZE_D2]
        # ])

    def set_level(self, level):
        self.level = level

    def update(self):
        pass

    def intersects(self, entity):
        left_x = max(self.left, entity.left)
        bottom_y = max(self.bottom, entity.bottom)
        right_x = min(self.right, entity.right)
        top_y = min(self.top, entity.top)

        return left_x < right_x and bottom_y < top_y

        # return self.intersects_rect(entity.x, entity.y, entity.width, entity.height)

    def intersects_rect(self, x, y, width, height):

        # dist_x = (self.center_x - x+width/2)**2
        # dist_y = (self.center_y - y+height/2)**2

        # col_radius = (self.collision_radius + max(width, height))

        # if dist_x + dist_y > col_radius * col_radius:
        #     return False

        left_x = max(self.x, x)
        bottom_y = max(self.y, y)
        right_x = min(self.x + self.width, x + width)
        top_y = min(self.y + self.height, y + height)

        return left_x < right_x and bottom_y < top_y