import arcade
import pymunk

class GroundSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, textures, scale, x, y):
        super().__init__()
        self.pymunk_shape = pymunk_shape

        self.textures = textures
        self.texture = self.textures[0]

        self.scaling = scale

        self.center_x = x
        self.center_y = y


class PlayerSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, textures, scale, x, y, name):
        super().__init__()
        self.pymunk_shape = pymunk_shape
        self.can_jump = True

        self.textures = textures
        self.texture = self.textures[0]
        self.name = name

        self.scaling = scale

        self.acc_x = 0
        self.acc_y = 0

        self.center_x, self.center_y = x, y
        self.og_x, self.og_y = self.center_x, self.center_y

    def update(self):
        self.og_x = self.center_x
        self.og_y = self.center_y


def makePlayer(mass, space, textures, scale, x, y, name):
    pos_x, pos_y = x, y

    width, height = textures[0].width, textures[0].height
    mass = mass
    body = pymunk.Body(mass, pymunk.inf)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    space.add(body, shape)
    sprite = PlayerSprite(shape, textures, scale, pos_x, pos_y, name)
    return sprite, body, shape


def makeGround(space, textures, scale, x, y):
    pos_x, pos_y = x, y
    width, height = textures[0].width, textures[0].height
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 1
    space.add(body, shape)
    sprite = GroundSprite(shape, textures, scale, pos_x, pos_y)
    return sprite