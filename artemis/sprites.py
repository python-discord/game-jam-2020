import arcade
import random

from constants import ASSETS, WIDTH, SIDE, HEIGHT, SCALING, TOP


class Gem(arcade.Sprite):
    TEXTURES = 'rbywp'

    def __init__(self, game, image=ASSETS+'gem_{}.png'):
        super().__init__(image.format('w'), SCALING * 0.25)
        self.textures = []
        for texture in Gem.TEXTURES:
            self.textures.append(arcade.load_texture(
                image.format(texture)
            ))
        self.game = game
        self.game.gems.append(self)
        self.place()
        self.center_x += WIDTH

    def get_texture(self):
        self.colour = random.choices(Gem.TEXTURES, weights=[3, 3, 3, 1, 1])[0]
        return self.textures[Gem.TEXTURES.index(self.colour)]

    def place(self):
        self.texture = self.get_texture()
        self.center_x = self.game.left+WIDTH+random.randrange(SIDE, SIDE*2)
        self.center_y = random.randrange(HEIGHT-TOP)
        overlapping = True
        while overlapping:
            overlapping = False
            for others in (
                    self.game.blocks, self.game.gems, self.game.spikes
                    ):
                if arcade.check_for_collision_with_list(self, others):
                    overlapping = True
                    self.center_y = random.randrange(HEIGHT-TOP)
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
                    int(spike.center_x-self.width*5),
                    int(spike.center_x+self.width*5)
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
        self.reposition()

    def find_y(self):
        range_pixels = HEIGHT - TOP
        range_widths = range_pixels // self.width
        position_widths = random.randrange(range_widths+1)
        self.center_y = position_widths * self.width

    def reposition(self):
        self.center_x += WIDTH + random.randrange(SIDE, SIDE*2)
        self.reposition_y()

    def reposition_y(self):
        attempts = 5
        overlapping = True
        while attempts and overlapping:
            overlapping = False
            attempts -= 1
            self.find_y()
            for others in (
                    self.game.blocks, self.game.gems, self.game.spikes
                    ):
                if arcade.check_for_collision_with_list(self, others):
                    overlapping = True
                    break
            # minimum distance between blocks that aren't touching
            min_dist = 200 * SCALING
            left_bound = self.left - min_dist
            right_bound = self.right + min_dist
            for block in self.game.blocks:
                if (
                            left_bound < block.left < right_bound
                            or left_bound < block.right < right_bound
                        ) and (
                            1 < self.bottom - block.top < min_dist
                            or 1 < block.bottom - self.top < min_dist
                        ):
                    overlapping = True
                    break
            if not overlapping:
                break
        if not attempts:
            self.center_y = HEIGHT * 2    # go off the screen till next time
        self.up = random.randrange(2)

    def total_reposition(self):
        self.center_x = random.randrange(WIDTH)
        self.center_y = random.randrange(HEIGHT-TOP)

    def update(self):
        super().update()
        for others in (self.game.blocks, self.game.gems):
            if arcade.check_for_collision_with_list(self, others):
                self.reposition_y()


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
        blocks = arcade.check_for_collision_with_list(
            self, self.block.game.blocks
        )
        for block in blocks:
            if block != self.block:
                self.remove_from_sprite_lists()
                return
