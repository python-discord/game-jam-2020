import os
# SETUP CONSTANTS
DEBUG_MODE = True
if DEBUG_MODE:
    PATH_ADD = ''
else:
    PATH_ADD = 'submission\\'

FULLSCREEN = True

# CONSTANTS
TILE_SIZE = 32  # x32 = 256px
PLAYER_SCALING = 1
TILE_SCALING = 1

WINDOW_WIDTH = 512
WINDOW_HEIGHT = 512
WINDOW_TITLE = 'Tricerasect'

LEFT_FACING = 0
RIGHT_FACING = 1
DOWN_FACING = 2
UP_FACING = 3

# PLAYER CONSTANTS
MOVE_SPEED = 1
MOVE_SPEED_CHARGED = 0.7 * MOVE_SPEED

# ENTITY TYPES
E_ANT = 0
E_MOSQUITO = 1
E_SPIDER = 2
E_DUNG_BEETLE = 3

T_SPRAY = 10
T_LAMP = 11
T_VACUUM = 12

VOLUME = 0.5

# UPDATE RATES FOR ENTITIES
ER_MOSQUITO = 5

from pathlib import Path
PATH = {}
PATH['project'] = Path(os.path.dirname(__file__))
PATH['img'] = PATH['project'] / "images"
PATH['sound'] = PATH['project'] / "sounds"
PATH['maps'] = PATH['project'] / "tmx_maps"
