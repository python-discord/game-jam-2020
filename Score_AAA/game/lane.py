import arcade
from characters import Character

class Lane():


    # init a lane with char/floor/physics engine/
    def __init__(self, tier, SCREEN_HEIGHT, SCREEN_WIDTH, sprite_char, run_textures):

        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.tier = tier
        self.char = Character(sprite_char,
                              SCREEN_HEIGHT - (SCREEN_HEIGHT // 3)*tier + 20,
                              run_textures)
        self.char.center_x = SCREEN_WIDTH // 10
        self.char.scale = 1

        self.floor = arcade.Sprite("../ressources/Floor_Tempo.png")
        self.floor.center_y = SCREEN_HEIGHT - (SCREEN_HEIGHT // 3)*tier
        floor_list = arcade.SpriteList()
        floor_list.append(self.floor)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.char, floor_list)

    def generate_obstacle(self):
        obstacle = arcade.Sprite("../ressources/Tempo_Obstacle.png")
        obstacle.center_x = self.SCREEN_WIDTH
        obstacle.center_y = self.SCREEN_HEIGHT - \
                            ( self.SCREEN_HEIGHT // 3) * self.tier + 20
        obstacle.change_x = -6
        return obstacle

    def generate_tree(self):
        tree = arcade.Sprite("../ressources/Tree_Tempo.png")
        tree.scale = 0.5
        tree.center_x = self.SCREEN_WIDTH
        tree.center_y = self.SCREEN_HEIGHT - \
                            (self.SCREEN_HEIGHT // 3) * self.tier + 38
        tree.change_x = -2
        return tree

