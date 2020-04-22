import arcade
import pymunk

class Player(arcade.Sprite):
    def __init__(self, pymunk_shape, textures, scale, x, y, name):
        super().__init__()
        self.pymunk_shape = pymunk_shape
        self.can_jump = True

        self.textures = textures
        self.texture = self.textures[0]
        self.name = name

        self.scale = scale

        self.acc_x = self.acc_y = 0

        self.center_x, self.center_y = x, y
        self.og_x, self.og_y = self.center_x, self.center_y

    def update(self):
        self.og_x, self.og_y = self.center_x, self.center_y


class EnemyThing(arcade.Sprite):
    pass

def makeMob(mass, space, mobType, textures, scale, x, y, name):
    pos_x, pos_y = x, y

    width, height = textures[0].width, textures[0].height
    mass = mass
    body = pymunk.Body(mass, pymunk.inf)
    body.position = pymunk.Vec2d((pos_x, pos_y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    space.add(body, shape)
    sprite = mobType(shape, textures, scale, pos_x, pos_y, name)
    sprite.set_hit_box([[sprite.width / -2, sprite.height / -2 - 1], [sprite.width / 2, sprite.height / -2 - 1],
                   [sprite.width / 2, sprite.height / 2], [sprite.width / -2, sprite.height / 2]])
    return sprite, body, shape
