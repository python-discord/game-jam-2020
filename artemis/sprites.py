import arcade
import random

from constants import (
    ASSETS, WIDTH, SIDE, HEIGHT, TOP, SCALING, BLOCKS_TOP, BLOCKS_Y
)


class Gem(arcade.Sprite):
    TEXTURES = 'rbywp'

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
        self.colour = random.choices(Gem.TEXTURES, weights=[3, 3, 3, 1, 1])[0]
        return self.textures[Gem.TEXTURES.index(self.colour)]

    def place(self):
        self.texture = self.get_texture()
        self.center_x = self.game.left + WIDTH + random.randrange(SIDE, SIDE*2)
        self.center_y = random.randrange(HEIGHT-TOP)
        while True:
            overlapping = False
            for others in (
                    self.game.blocks, self.game.gems, self.game.spikes
                    ):
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
    def __init__(
            self, game, x, y, up, image=ASSETS+'block.png', scale=SCALING
            ):
        super().__init__(image, center_x=x, center_y=y, scale=scale)
        self.game = game
        game.blocks.append(self)
        self.spike = None
        self.up = up

    def can_place_spike(self):
        for spike in self.game.spikes:
            if self.center_x in range(
                    int(spike.center_x-self.width*3),
                    int(spike.center_x+self.width*3)
                    ):
                return False
        return True

    def reposition(self):
        self.center_x += WIDTH + SIDE*2

    def update(self):
        if self.center_x < self.game.left-SIDE:
            self.reposition()
            if self.spike:
                self.spike.remove_from_sprite_lists()
                self.spike = None
            if self.can_place_spike() and not random.randrange(20):
                self.spike = Spike(self, self.up)
                self.game.spikes.append(self.spike)


class RandomBlock(Block):
    def __init__(self, game):
        super().__init__(game, 0, 0, random.randrange(2), scale=SCALING*2)
        self.total_reposition()

    def find_y(self):
        range_pixels = HEIGHT - TOP
        range_widths = range_pixels // self.width
        position_widths = random.randrange(range_widths+1)
        self.center_x = position_widths * self.width

    def reposition(self):
        self.center_x += WIDTH + random.randrange(SIDE, SIDE*2)
        self.find_y()
        while True:
            overlapping = False
            for others in (
                    self.game.blocks, self.game.gems, self.game.spikes
                    ):
                if arcade.check_for_collision_with_list(self, others):
                    overlapping = True
                    self.find_y()
                    break
            if not overlapping:
                break
        self.up = random.randrange(2)

    def total_reposition(self):
        self.center_x = random.randrange(WIDTH)
        self.center_y = random.randrange(HEIGHT-TOP)

    def update(self):
        for others in (self.game.blocks, self.game.gems):
            if arcade.check_for_collision_with_list(self, others):
                self.total_reposition()
        super().update()


class Spike(arcade.Sprite):
    def __init__(self, block, up, image=ASSETS+'spikes_{}.png'):
        image = image.format(['down', 'up'][up])
        if isinstance(block, RandomBlock):
            scale = SCALING * 2
        else:
            scale = SCALING
        super().__init__(image, center_x=block.center_x, scale=scale)
        if up:
            self.bottom = block.top
        else:
            self.top = block.bottom
        self.block = block

    def update(self):
        self.center_x = self.block.center_x