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

        if e_type == E_ANT:
            self.update_rate = UR_ANT
        elif e_type == E_MOSQUITO:
            self.update_rate = UR_MOSQUITO
        elif e_type == E_SPIDER:
            self.update_rate = UR_SPIDER
        elif e_type == E_DUNG_BEETLE:
            self.update_rate = UR_DUNG_BEETLE
        elif e_type == T_SPRAY:
            self.update_rate = UR_SPRAY
        elif e_type == T_LAMP:
            self.update_rate = UR_LAMP
        elif e_type == T_VACUUM:
            self.update_rate = UR_VACUUM

        self.character_face_direction = LEFT_FACING

        self.numberFrames = num_of_frames

        self.cur_texture_index = 0

        main_path = PATH['img'] / 'sprite' / anim_filename  # path

        self.basic_textures = []

        for i in range(num_of_frames):  # nb of frames of the animation
            texture_pair = load_texture_pack(f"{main_path}_f{i + 1}.png", e_type)
            self.basic_textures.append(texture_pair)

        self.texture = self.basic_textures[0][0]

    def update_animation(self, delta_time: float = 1 / 60):

        self.cur_texture_index += 1
        if self.cur_texture_index >= self.numberFrames * self.update_rate:
            self.cur_texture_index = 0
        self.texture = self.basic_textures[self.cur_texture_index // self.update_rate][0]


class AnimatedPlayer(arcade.Sprite):
    """
    Creates animated player sprite
    """

    def __init__(self, anim_filename: str, num_of_frames: int):
        super().__init__()

        self.numberFrames = num_of_frames

        self.character_face_direction = LEFT_FACING

        self.cur_texture_index = 0

        main_path = PATH['img'] / 'sprite' / anim_filename  # path

        self.basic_textures = []

        for i in range(num_of_frames):  # nb of frames of the animation
            texture_pair = load_texture_pair(f"{main_path}_f{i+1}.png")
            self.basic_textures.append(texture_pair)

        self.texture = self.basic_textures[0][0]

        self.cur_pos = []
        self.is_moving = False
        self.direction = None
        self.corr_x = False
        self.corr_y = False
        self.destination = [-1,-1]
        self.cur_speed = MOVE_SPEED

        self.inventory = 0

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture_index += 1
        if self.cur_texture_index >= self.numberFrames * UR_PLAYER:
            self.cur_texture_index = 0
        self.texture = self.basic_textures[self.cur_texture_index // UR_PLAYER][self.character_face_direction]