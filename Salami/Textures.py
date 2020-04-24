
import arcade

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


CHARACTERS = Textures.load_textures("Salami/spritesheet.png", 2, 12, 8, 27)
SYMBOLS = Textures.load_textures("Salami/spritesheet.png", 2, 13, 8, 21)
SPRITESHEET = arcade.load_spritesheet("Salami/spritesheet.png", 16, 16, 16, 256)
THIN_CHARS = arcade.load_spritesheet("Salami/thin_chars.png", 6, 8, 27, 27 * 3)