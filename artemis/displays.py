import arcade
from PIL import Image

from constants import ASSETS, SCALING, HEIGHT, TOP


class BoxGem(arcade.Sprite):
    def __init__(self, box):
        super().__init__(
            f'{ASSETS}gem_{box.colour}.png', SCALING*0.25,
            center_x=box.center_x, center_y=box.center_y
        )
        box.game.others.append(self)
        self.box = box

    def update(self):
        self.center_x = self.box.center_x


class Box(arcade.Sprite):
    def __init__(self, game, n, image=ASSETS+'box.png'):
        super().__init__(
            image, SCALING*0.5,
            center_x=(n+0.6) * 256 * SCALING,
            center_y=HEIGHT - (TOP - game.blocks[0].height//2)//2
        )
        self.game = game
        self.alpha = 50
        self.colour = None
        self.gem = None
        game.boxes.append(self)

    def add_gem(self, colour):
        self.colour = colour
        self.gem = BoxGem(self)
        self.alpha = 100
        self.game.gem_added()

    def remove_gem(self):
        if self.gem:
            self.gem.remove_from_sprite_lists()
            self.alpha = 50
            self.colour = self.gem = None

    def update(self):
        self.center_x += self.game.player.speed


class PausePlay(arcade.Sprite):
    def __init__(self, x, y, game):
        super().__init__(center_x=x, center_y=y)
        self.game = game
        game.on_mouse_release = self.on_mouse_release
        self.textures = {
            'pause': self.load_texture('pause.png'),
            'play': self.load_texture('play.png')
        }
        self.texture = self.textures['pause']

    def load_texture(self, file, size=32):
        im = Image.open(ASSETS+file).resize((size, size))
        return arcade.Texture(file, im)

    def pressed(self):
        self.game.paused = not self.game.paused
        image = ['pause', 'play'][self.game.paused]
        self.texture = self.textures[image]
        self.game.window.show_view(self.game)

    def on_mouse_release(self, x, y, button, modifiers):
        x += self.game.left
        if self.left <= x <= self.right and self.bottom <= y <= self.top:
            self.pressed()
