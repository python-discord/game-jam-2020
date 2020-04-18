import arcade

from submission.gameConstants import *


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image. For the player char.
    """
    return [
        arcade.load_texture(PATH['img'] / filename),
        arcade.load_texture(PATH['img'] / filename, mirrored=True)
    ]


def load_texture_pack(filename: str, e_type: int):  # à revoir
    """
    Load the four/three directions of textures. For the entities
    """

    if e_type > 7:  # si tourelle (load 3 directions)
        return [
            arcade.load_texture(PATH['img'] / filename),
            arcade.load_texture(PATH['img'] / filename, mirrored=True),
            arcade.load_texture(PATH['img'] / filename + 'UD'),
            arcade.load_texture(PATH['img'] / filename + 'UD', mirrored=True)
        ]
    elif e_type < 7:  # si ennemi (load 3 directions)
        return [
            arcade.load_texture(PATH['img'] / filename),
            arcade.load_texture(PATH['img'] / filename, mirrored=True),
            # arcade.load_texture(PATH['img'] / filename + 'U')
        ]


class AnimatedEntity(arcade.Sprite):
    """
    Creates animated entity (except player) with init and update_animation
    """

    def __init__(self, anim_filename: str, num_of_frames: int, e_type: int):
        super().__init__()

        self.character_face_direction = UP_FACING

        self.numberFrames = num_of_frames

        self.cur_texture = 0

        main_path = PATH['img'] / 'sprite' / anim_filename  # path

        self.basic_textures = []

        for i in range(num_of_frames):  # nb of frames of the animation
            texture_pair = load_texture_pack(f"{main_path}_f{i+1}.png", e_type)
            self.basic_textures.append(texture_pair)

        self.texture = self.basic_textures[0][0]

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture >= self.numberFrames * ER_MOSQUITO:
            self.cur_texture = 0
            print('cycle')
        self.texture = self.basic_textures[self.cur_texture // ER_MOSQUITO][0]


class AnimatedPlayer(arcade.Sprite):
    """
    Creates animated player sprite
    """

    def __init__(self, anim_file_path: str, num_of_frames: int):
        super(self).__init__()

        self.character_face_direction = RIGHT_FACING

        self.cur_texture_index = 0

        main_path = PATH['img'] / anim_file_path  # path

        self.basic_textures = []

        for i in range(num_of_frames):  # nb of frames of the animation
            texture_pair = load_texture_pair(f"{main_path}_f{i}.png")
            self.basic_textures.append(texture_pair)

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            pass
