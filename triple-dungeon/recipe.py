'''
Recipes are combinations of three monsters. When a player fills a recipe they get an updgrade
'''

import arcade


class Recipe:
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
        self.cycle_recipes = [self.set_ghosts, self.set_frogs, self.set_ggf]
        self.ghost = arcade.Sprite(filename="resources/images/monsters/ghost/ghost1.png")
        self.frog = arcade.Sprite(filename="resources/images/monsters/frog/frog1.png")
        self.pos = 0
        self.kill_list = []


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
        x = 0
        for kill in self.kill_list:
            sprite = getattr(self, kill)
            screen_right = arcade.get_viewport()[1] - 240
            screen_top = arcade.get_viewport()[3] - 150
            sprite.scale = 4
            sprite.center_x = screen_right + x
            sprite.center_y = screen_top
            x += 70
            sprite.draw()

    def next_recipe(self):
        self.pos += 1
        if self.pos == len(self.cycle_recipes):
            self.pos = 0
        self.cycle_recipes[self.pos]()

    def add_kill(self, monster_type) -> int:
        # Adds a kill to kill_list. If 3 or more check the recipe then give a power up if it matches.
        self.kill_list.append(monster_type)
        ret_val = -1
        if len(self.kill_list) >= 3:
            if self.active == self.kill_list:
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                self.kill_list = []
                ret_val = self.pos
            self.kill_list = []
        return ret_val

    def set_ghosts(self) -> None:
        self.active = Recipe.GHOSTS
        self.sprite_list = []
        self.sprite_list.append(self.ghost)
        self.sprite_list.append(self.ghost)
        self.sprite_list.append(self.ghost)
            
    def set_frogs(self) -> None:
        self.active = Recipe.FROGS
        self.sprite_list = []
        self.sprite_list.append(self.frog)
        self.sprite_list.append(self.frog)
        self.sprite_list.append(self.frog)
        
    def set_ggf(self) -> None:
        self.active = Recipe.GHOST_FROG
        self.sprite_list = []
        self.sprite_list.append(self.frog)
        self.sprite_list.append(self.ghost)
        self.sprite_list.append(self.ghost)