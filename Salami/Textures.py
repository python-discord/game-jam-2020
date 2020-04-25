
import arcade
import PIL

from Constants import TILE_SIZE

class Textures:

    # @staticmethod
    # def init_textures():
        # sheet_list = arcade.SpriteList()
        # for x in range(16):
        #     for y in range(16):
        #         tile = arcade.Sprite()
        #         tile.texture = sheet[x + y * 16]
        #         tile.left = x * 16
        #         tile.bottom = y * 16
        #         self.sheet_list.append(tile)

    @staticmethod
    def load_texture(filename: str, image_x, image_y, image_size, mirrored: bool=False):
        pass

    @staticmethod
    def load_textures(filename, image_x, image_y, image_size, times, mirrored: bool=False):
        result = []
        for i in range(times):
            result.append(arcade.load_texture(
                filename,
                (image_x + i) * image_size,
                image_y * image_size,
                image_size, image_size,
                mirrored=mirrored))
        return result

    @staticmethod
    def load_backgrounds(filename, times):
        result = []
        for i in range(times):
            result.append(arcade.load_texture(filename + "_" + str(i) + ".png"))
        return result

def get_textures(x, y, count, mirrored=False):
    result = []
    for i in range(count):
        tex = get_texture(x + i, y)
        if tex:
            result.append(tex)
    return result

def get_texture(x, y, mirrored=False):
    if x < 0 or y < 0 or x >= 16 or y >= 16:
        return
    tex = SPRITESHEET[x + y * 16]
    if mirrored:
        tex.image = PIL.ImageOps.mirror(tex.image)
    return tex

CHARACTERS = Textures.load_textures("Salami/chars.png", 0, 0, 8, 27)
SYMBOLS = Textures.load_textures("Salami/chars.png", 0, 1, 8, 21)
SPRITESHEET = arcade.load_spritesheet("Salami/spritesheet.png", 16, 16, 16, 16 * 16)
THIN_CHARS = arcade.load_spritesheet("Salami/thin_chars.png", 6, 8, 27, 27 * 3)