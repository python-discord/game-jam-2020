import arcade
import pymunk

class Ground(arcade.Sprite):
    """it could be dirt, it could be wood, who knows"""
    def __init__(self, pymunk_shape, textures, scale, x, y):
        super().__init__()
        self.pymunk_shape = pymunk_shape

        self.textures = textures
        self.texture = self.textures[0]
        self.scale = scale

        self.center_x, self.center_y = x, y

def makeLand(space, textures, scale, x, y, hit_box):
    pos_x, pos_y = x, y
    width, height = textures[0].width, textures[0].height
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 1
    space.add(body, shape)
    sprite = Ground(shape, textures, scale, pos_x, pos_y)
    sprite.hit_box = hit_box
    return sprite

def makeBox(mass, space, textures, hit_box, scale, x, y):
    body = pymunk.Body(mass, pymunk.moment_for_poly(mass, vertices=hit_box) * 10)
    body.position = pymunk.Vec2d((x, y))
    shape = pymunk.Poly.create_box(body, (textures[0].width, textures[0].height))
    shape.friction = 0.8
    space.add(body, shape)
    sprite = Ground(shape, textures, scale, x, y)
    return sprite
