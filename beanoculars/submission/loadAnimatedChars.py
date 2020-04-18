import arcade

from submission.gameConstants import *


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class AnimatedChar(arcade.Sprite):
    def __init__(self, anim_file_path: str, num_of_frames: int, entity_type: int):
        super(self).__init__()

        self.character_face_direction = UP_FACING

        self.cur_texture_index = 0

        main_path = PATH_ADD + anim_file_path  # path

        self.basic_textures = []

        for i in range(num_of_frames): # nb of frames of the animation
            texture_pair = load_texture_pair(f"{main_path}_f{i}.png")
            self.basic_textures.append(texture_pair)

    def update_animation(self, delta_time: float = 1/60):

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            pass


class AnimatedPlayer(arcade.Sprite):
    def __init__(self, anim_file_path: str, num_of_frames: int):
        super(self).__init__()

        self.character_face_direction = RIGHT_FACING

        self.cur_texture_index = 0

        main_path = PATH_ADD + anim_file_path  # path

        self.basic_textures = []

        for i in range(num_of_frames):  # nb of frames of the animation
            texture_pair = load_texture_pair(f"{main_path}_f{i}.png")
            self.basic_textures.append(texture_pair)

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            pass