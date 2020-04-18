import arcade
import os

def loadSounds(foldername: str, s_dict):
    for sound in os.listdir('sounds'):
        print(sound)
        print(foldername)
        s_dict[sound] = arcade.Sound(foldername+'\\'+sound)