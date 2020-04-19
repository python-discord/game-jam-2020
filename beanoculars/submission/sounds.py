import arcade
import os
from submission.gameConstants import PATH

def loadSounds(s_dict):
    os.chdir(PATH['sound'])
    for sound in os.listdir():
        s_dict[sound] = arcade.Sound(sound)