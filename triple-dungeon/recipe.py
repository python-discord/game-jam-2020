'''
Recipes are combinations of three monsters. When a player fills a recipe they get an updgrade
'''

import arcade

from enum import Enum


class Recipe(Enum):
    '''
    A class of different recipes
    '''

    GHOSTS = ['ghost', 'ghost', 'ghost']
    FROGS = ['frog', 'frog', 'frog']
    GHOST_FROG = ['ghost', 'ghost', 'frog']
    FROG_GHOST = ['ghost', 'frog', 'frog']


class ActiveRecipe(arcade.SpriteList):
    '''
    Keeps track of the active recipe and draws it.
    '''

    def __init__(self):
        super().__init__()
        self.active = Recipe.GHOSTS
        self.cycle_recipes = [self.set_frogs, self.set_ghosts]
        self.pos = 0

    def render(self) -> None:
        x = 0
        for sprite in self.sprite_list:
            screen_right = arcade.get_viewport()[1] - 100
            screen_top = arcade.get_viewport()[3] - 80
            sprite.scale = 4
            sprite.center_x = screen_right - x
            sprite.center_y = screen_top
            x += 70
            sprite.draw()

    def next_recipe(self):
        
        self.cycle_recipes[self.pos]()
        self.pos += 1
        if self.pos == len(self.cycle_recipes):
            self.pos = 0

    def set_ghosts(self) -> None:
        self.active = Recipe.GHOSTS
        self.sprite_list = []
        self.sprite_list.append(arcade.Sprite(filename="resources/images/monsters/ghost/ghost1.png"))
        self.sprite_list.append(arcade.Sprite(filename="resources/images/monsters/ghost/ghost1.png"))
        self.sprite_list.append(arcade.Sprite(filename="resources/images/monsters/ghost/ghost1.png"))

    def set_frogs(self) -> None:
        self.active = Recipe.FROGS
        self.sprite_list = []
        self.sprite_list.append(arcade.Sprite(filename="resources/images/monsters/frog/frog1.png"))
        self.sprite_list.append(arcade.Sprite(filename="resources/images/monsters/frog/frog1.png"))
        self.sprite_list.append(arcade.Sprite(filename="resources/images/monsters/frog/frog1.png"))
