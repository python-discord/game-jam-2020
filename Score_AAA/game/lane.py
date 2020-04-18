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
        self.char.scale = 1.7

        self.floor = arcade.Sprite("../ressources/Floor_Tempo.png")
        self.floor.center_y = SCREEN_HEIGHT - (SCREEN_HEIGHT // 3)*tier
        floor_list = arcade.SpriteList()
        floor_list.append(self.floor)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.char, floor_list)
        self.valid_zone = self.generate_valid_zone()

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

    def generate_valid_zone(self):
        valid_zone = arcade.Sprite("../ressources/Lane_Valid_Zone.png")
        valid_zone.center_x = (self.SCREEN_WIDTH // 10) * 2
        valid_zone.center_y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 3)*self.tier + 90
        valid_zone.color = (0, 0, 0)
        return valid_zone

    def action(self, obstacle_list):
        score = False
        if self.physics_engine.can_jump(5):
            for collision in arcade.check_for_collision_with_list(self.valid_zone,
                                                                  obstacle_list):
                obstacle_list.remove(collision)
                score = True
            self.physics_engine.jump(6)
        return score

    def gen_background(self, sprite_path, speed, offset):
        # offset 107 for Q
        result = []
        background = arcade.Sprite(sprite_path)
        background.center_y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 3)*self.tier \
                              + offset
        background.center_x = self.SCREEN_WIDTH // 2
        background.change_x = -speed
        result.append(background)

        background = arcade.Sprite(sprite_path)
        background.center_y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 3)*self.tier \
                                + offset
        background.center_x = self.SCREEN_WIDTH + self.SCREEN_WIDTH // 2
        background.change_x = -speed
        result.append(background)
        return result