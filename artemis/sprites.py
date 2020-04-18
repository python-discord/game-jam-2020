import arcade
import random

from constants import ASSETS, WIDTH, SIDE, HEIGHT, TOP, SCALING


class Gem(arcade.Sprite):
    TEXTURES = 'rbyw'

    def __init__(self, game, image=ASSETS+'gem_{}.png'):
        self.value = random.randrange(50, 125)
        super().__init__(image.format('w'), SCALING * 0.25)
        self.textures = []
        for texture in Gem.TEXTURES:
            self.textures.append(arcade.load_texture(
                image.format(texture)
            ))
        self.texture = self.get_texture()
        self.game = game
        self.game.gems.append(self)
        self.reposition()

    def get_texture(self):
        self.colour = random.choices(Gem.TEXTURES)[0]
        return self.textures[Gem.TEXTURES.index(self.colour)]

    def place(self):
        self.texture = self.get_texture()
        self.center_x = self.game.left + WIDTH + SIDE
        self.center_y = random.randrange(HEIGHT-TOP)
        while True:
            overlapping = False
            for others in (self.game.blocks, self.game.gems):
                if arcade.check_for_collision_with_list(self, others):
                    overlapping = True
                    self.center_y = random.randrange(HEIGHT-TOP)
            if not overlapping:
                break

    def reposition(self):
        self.center_x = random.randrange(WIDTH)
        self.center_y = random.randrange(HEIGHT-TOP)

    def update(self):
        if self.center_x < self.game.left-SIDE:
            self.place()
        for others in (self.game.blocks, self.game.gems):
            if arcade.check_for_collision_with_list(self, others):
                self.reposition()


class Block(arcade.Sprite):
    def __init__(self, game, x, y, image=ASSETS+'block.png'):
        super().__init__(image, center_x=x, center_y=y, scale=SCALING*1)
        self.game = game
        game.blocks.append(self)

    def update(self):
        if self.center_x < self.game.left-SIDE:
            self.center_x += WIDTH + SIDE*2