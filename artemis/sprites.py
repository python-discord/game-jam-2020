import arcade
import random

from constants import ASSETS, WIDTH, SIDE, HEIGHT, TOP, SCALING


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
        self.center_x = self.game.left + WIDTH + SIDE
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
    def __init__(self, game, x, y, up, image=ASSETS+'block.png'):
        super().__init__(image, center_x=x, center_y=y, scale=SCALING)
        self.game = game
        game.blocks.append(self)
        self.spike = None
        self.up = up

    def can_place_spike(self):
        for spike in self.game.spikes:
            if self.center_x in range(
                    int(spike.center_x-self.width*2),
                    int(spike.center_x+self.width*2)
                    ):
                return False
        return True

    def update(self):
        if self.center_x < self.game.left-SIDE:
            self.center_x += WIDTH + SIDE*2
            if self.spike:
                self.spike.remove_from_sprite_lists()
                self.spike = None
            if self.can_place_spike() and not random.randrange(20):
                self.spike = Spike(self, self.up)
                self.game.spikes.append(self.spike)


class Spike(arcade.Sprite):
    def __init__(self, block, up, image=ASSETS+'spikes_{}.png'):
        image = image.format(['down', 'up'][up])
        super().__init__(image, center_x=block.center_x, scale=SCALING)
        if up:
            self.bottom = block.top
        else:
            self.top = block.bottom
        self.block = block

    def update(self):
        self.center_x = self.block.center_x