"""
sprites.py
A file dedicated to managing sprites and animations for characters.
"""
import re


class AnimationSet(object):
    """
    A class that helps assist with grabbing new animations from a set.
    """

    def __init__(self, directory: str):
        """
        Initializes the AnimationSet class by loading files and

        :param directory: A directory containing valid animation files in the correct format.
        """
        pass


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

        self.idles = self.getAnimations(re.compile(r'idle_\d+.png'))
        self.down = self.getAnimations(re.compile(r'run_down_\d+.png'))
        self.right = self.getAnimations(re.compile(r'run_right_\d+.png'))
        self.up = self.getAnimations(re.compile(r'run_up_\d+.png'))
        self.down = self.getAnimations(re.compile(r'run_left_\d+.png'))

    def __loadAnimations(self):