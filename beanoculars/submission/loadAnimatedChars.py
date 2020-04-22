import arcade

from submission.gameConstants import *


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image. For the player char.
    """
    return [
        arcade.load_texture(PATH['img'] / filename, mirrored=True),  # RIGHT
        arcade.load_texture(PATH['img'] / filename)  # LEFT
    ]


def load_texture_pack(filename: str, upFilename: str, e_type: int):  # à revoir
    """
    Load the four/three directions of textures. For the entities
    """

    if e_type > 7:  # si tourelle (load 4 directions)
        return [
            arcade.load_texture(PATH['img'] / filename, flipped=True),  # UP
            arcade.load_texture(PATH['img'] / filename),  # DOWN
            #arcade.load_texture(PATH['img'] / upFilename),  # RIGHT
            #arcade.load_texture(PATH['img'] / upFilename, mirrored=True)  # LEFT
        ]
    elif e_type < 7:  # si ennemi (load 3 directions)
        return [
            arcade.load_texture(PATH['img'] / upFilename),  # UP
            arcade.load_texture(PATH['img'] / upFilename, flipped=True),  # DOWN
            arcade.load_texture(PATH['img'] / filename)  # RIGHT
        ]

    else:
        raise Exception('Problem with loading an entity sprite')


class AnimatedEntity(arcade.Sprite):
    """
    Creates animated entity (except player) with init and update_animation
    """

    def __init__(self, e_type: int, coor: [int, int]):
        super().__init__()

        main_path = ''

        if e_type == E_ANT:
            self.e_type = E_ANT
            self.update_rate = UR_ANT
            self.numberFrames = F_ANT
            main_path = PATH['img'] / 'sprite' / 'ant'

        elif e_type == E_MOSQUITO:
            self.e_type = E_MOSQUITO
            self.update_rate = UR_MOSQUITO
            self.numberFrames = F_MOSQUITO
            main_path = PATH['img'] / 'sprite' / 'mosquito'

        elif e_type == E_SPIDER:
            self.e_type = E_SPIDER
            self.update_rate = UR_SPIDER
            self.numberFrames = F_SPIDER
            main_path = PATH['img'] / 'sprite' / 'spider'

        elif e_type == E_DUNG_BEETLE:
            self.e_type = E_DUNG_BEETLE
            self.update_rate = UR_DUNG_BEETLE
            self.numberFrames = F_DUNG_BEETLE
            main_path = PATH['img'] / 'sprite' / 'dung_beetle'

        elif e_type == T_SPRAY:
            self.e_type = T_SPRAY
            self.update_rate = UR_SPRAY
            self.numberFrames = F_SPRAY
            main_path = PATH['img'] / 'sprite' / 'spray'

        elif e_type == T_LAMP:
            self.e_type = T_LAMP
            self.update_rate = UR_LAMP
            self.numberFrames = F_LAMP
            main_path = PATH['img'] / 'sprite' / 'lamp'

        elif e_type == T_VACUUM:
            self.e_type = T_VACUUM
            self.update_rate = UR_VACUUM
            self.numberFrames = F_VACUUM
            main_path = PATH['img'] / 'sprite' / 'vacuum'

        if e_type > 7:
            self.character_face_direction = UP_FACING # TODO A CHANGER EN DOWN
        elif e_type < 7:
            self.character_face_direction = RIGHT_FACING

        self.cur_texture_index = 0

        self.basic_textures = []

        for i in range(self.numberFrames):  # nb of frames of the animation
            texture_pack = load_texture_pack(f"{main_path}_f{i + 1}.png", f"{main_path}_Uf{i+1}.png", e_type)
            self.basic_textures.append(texture_pack)

        self.center_x = coor[0]*32 + 16
        self.center_y = coor[1]*32 + 16

        self.ud = True

        self.texture = self.basic_textures[0][0]

    def update_animation(self, delta_time: float = 1 / 60):

        self.cur_texture_index += 1
        if self.cur_texture_index >= self.numberFrames * self.update_rate:
            self.cur_texture_index = 0
        self.texture = self.basic_textures[self.cur_texture_index // self.update_rate][self.character_face_direction]


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
        self.destination = [-1, -1]
        self.initial_vector = None
        self.cur_speed = MOVE_SPEED
        self.dir_changed = False
        self.xdone = False
        self.ydone = False

        self.inventory = 0
        self.actual_cur_pos = []

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture_index += 1
        if self.cur_texture_index >= self.numberFrames * UR_PLAYER:
            self.cur_texture_index = 0
        if self.character_face_direction == RIGHT_FACING:
            self.texture = self.basic_textures[self.cur_texture_index // UR_PLAYER][1]
        elif self.character_face_direction == LEFT_FACING:
            self.texture = self.basic_textures[self.cur_texture_index // UR_PLAYER][0]