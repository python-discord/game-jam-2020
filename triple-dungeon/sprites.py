"""
sprites.py
A file dedicated to managing sprites and animations for characters.
"""

import arcade
import os
import re

from itertools import cycle


class AnimationSet(object):
    """
    A class that helps assist with grabbing new animations from a set.
    """

    def __init__(self, directory: str):
        """
        Initializes the AnimationSet class by loading files and

        :param directory: A directory containing valid animation files in the correct format.
        """

        self.directory = directory
        self.animations = os.listdir(directory)

    def getAnimations(self, pattern: re.Pattern) -> iter:
        """
        Loads all animations from the AnimationSet's directory that match the pattern.
        The pattern must have 1 group that specifies the animation's index.

        :param pattern: A RegEx Pattern object.
        :return: A infinite iterable looping through arcade.Texture objects.
        """

        # Finds all matching files
        matches = [file for file in self.animations if re.match(pattern, file)]
        # Sort in ascending order based on the connected animation index. Zero-indexing or not does not affect order.
        matches.sort(key=lambda match : int(match.group(1)))
        # Grab the filename and load it to the file directory
        matches = list(map(lambda match : arcade.load_texture(os.path.join(self.directory, match.group(0))), matches))
        return cycle(matches)

class PlayerAnimations(AnimationSet):
    """
    A class dedicated to serving player animations.
    Player animations must be served to the class in the correct format.
    """

    def __init__(self):
        """
        Initializes the PlayerAnimations class.
        """

        super(PlayerAnimations, self).__init__()

        # Grabs all animations needed. These are infinite iters, use next(iter) to grab the next animation.
        self.idles = self.getAnimations(re.compile(r'idle_(\d+).png'))
        self.down = self.getAnimations(re.compile(r'run_down_(\d+).png'))
        self.right = self.getAnimations(re.compile(r'run_right_(\d+).png'))
        self.up = self.getAnimations(re.compile(r'run_up_(\d+).png'))
        self.down = self.getAnimations(re.compile(r'run_left_(\d+).png'))

    def __loadAnimations(self):