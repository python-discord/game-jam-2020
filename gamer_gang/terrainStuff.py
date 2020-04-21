import arcade
import pymunk

class NormalGround(arcade.Sprite):
    def __init__(self, pymunk_shape, textures, scale, x, y):
        super().__init__()
        self.pymunk_shape = pymunk_shape

        self.allTextures = textures
        self.texture = self.allTextures[0]
        self.scaling = scale

        self.center_x, self.center_y = x, y

class BadSpike(arcade.Sprite):
    def __init__(self, pymunk_shape, textures, scale, x, y):
        super().__init__()
        self.pymunk_shape = pymunk_shape

        self.allTextures = textures
        self.texture = self.allTextures[0]
        self.scaling = scale

        self.center_x, self.center_y = x, y

def makeTerrain(space, groundType, textures, scale, x, y):
    pos_x, pos_y = x, y
    width, height = textures[0].width, textures[0].height
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 1
    space.add(body, shape)
    sprite = groundType(shape, textures, scale, pos_x, pos_y)
    return sprite

