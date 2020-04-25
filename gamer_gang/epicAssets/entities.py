import random
import math
import arcade
import pymunk

class Player(arcade.Sprite):
    def __init__(self, pymunk_shape, textures, scale, x, y, name):
        super().__init__()
        self.pymunk_shape = pymunk_shape
        self.can_jump = True

        self.textureList = textures
        self.texture = self.textureList[0]
        self.name = name
        self.scale = scale

        self.center_x, self.center_y = x, y
        self.timeSinceAnimating = 0

    def update_animation(self, delta_time: float = 1/60):
        if self.timeSinceAnimating < 1:  # don't wanna animate the thing too fast, makes it kinda distracting
            self.timeSinceAnimating += delta_time
            return
        self.timeSinceAnimating = 0
        nextState = random.randint(0, 1)
        if nextState == 0:  # don't change the texture
            return
        else:  # ok, change
            rnTexture = self.textureList.index(self.texture)
            if self.textureList[:rnTexture] + self.textureList[rnTexture + 1:]:
                self.texture = random.choice(self.textureList[:rnTexture] + self.textureList[rnTexture + 1:])


class BeeSprite(arcade.Sprite):
    def __init__(self, textures, scale, x, y):
        super().__init__()

        self.textures = textures
        self.texture = self.textures[0]
        self.animState = True

        self.scale = scale

        self.og_x, self.og_y = self.center_x, self.center_y = x, y

    def update(self, players):
        dists = []
        for p in players:
            if p is not None:
                dists.append(math.sqrt((self.center_x - p.center_x) ** 2 + (self.center_y - p.center_y) ** 2))
            else:
                dists.append(float('inf'))

        if min(dists) < 32 * 8:
            tar = dists.index(min(dists))
            angle = math.atan2((players[tar].center_y - self.center_y), (players[tar].center_x - self.center_x))
            self.center_x += math.cos(angle)
            self.center_y += math.sin(angle)
        else:
            angle = math.atan2((self.og_y - self.center_y), (self.og_x - self.center_x))
            self.center_x += math.cos(angle)
            self.center_y += math.sin(angle)

    def update_animation(self, delta_time: float = 1/60):
        self.texture = self.textures[not self.animState]
        self.animState = not self.animState

class StarSprite(arcade.Sprite):
    def __init__(self, textures, scale, x, y, hitbox):
        super().__init__()

        self.textures = textures
        self.texture = self.textures[0]
        self.scale = scale
        self.hit_box = hitbox
        self.obtained = False

        self.og_x, self.og_y = self.center_x, self.center_y = x, y

    def update(self, frames):
        if not self.obtained:
            self.center_y = self.og_y + math.sin(frames/16) * 6
            self.scale = abs(math.sin(frames/32))/4 + 1
            self.angle = math.sin(frames/32) * 10
        else:
            self.scale *= 1.05
            self.angle += self.scale*2
            self.alpha -= 10 if self.alpha != 5.0 else 0
            self.kill()

def makePlayer(mass, space, textures, scale, x, y, name):
    width, height = textures[0].width, textures[0].height
    body = pymunk.Body(mass, pymunk.inf)
    body.position = pymunk.Vec2d((x, y))
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    space.add(body, shape)
    sprite = Player(shape, textures, scale, x, y, name)
    sprite.set_hit_box([[sprite.width / -2, sprite.height / -2 - 1], [sprite.width / 2, sprite.height / -2 - 1],
                        [sprite.width / 2, sprite.height / 2], [sprite.width / -2, sprite.height / 2]])
    return sprite, body, shape
