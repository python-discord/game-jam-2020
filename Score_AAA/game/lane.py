import arcade
from entities import Character, Obstacle
from enum import Enum

class EnumAction(Enum):
    miss = 0
    ok = 1
    super = 5
    perfect = 10

class Lane():
    """
    Initialise and generate most objects in one of the three lanes.
    """


    # init a lane with char/floor/physics engine/
    def __init__(self, tier: int, SCREEN_HEIGHT: int,
                 SCREEN_WIDTH: int, sprite_path: str, run_textures: list):
        """

        :param tier: What tier of the screen the lane should be.
        :param run_textures: A list of textures for running animation (only Q atm)
        """
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.tier = tier
        self.char = Character(sprite_path,
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

    def generate_obstacle(self)-> arcade.Sprite:
        """
        Used to generate an obstacle on the lane.
        """
        obstacle = Obstacle("../ressources/Tempo_Obstacle.png")
        obstacle.center_x = self.SCREEN_WIDTH
        obstacle.center_y = self.SCREEN_HEIGHT - \
                            ( self.SCREEN_HEIGHT // 3) * self.tier + 20
        obstacle.change_x = -6
        return obstacle

    def generate_tree(self)->arcade.Sprite:
        """
        Unused. Generate a tree that move towards the char
        """
        tree = arcade.Sprite("../ressources/Tree_Tempo.png")
        tree.scale = 0.5
        tree.center_x = self.SCREEN_WIDTH
        tree.center_y = self.SCREEN_HEIGHT - \
                            (self.SCREEN_HEIGHT // 3) * self.tier + 38
        tree.change_x = -2
        return tree

    def generate_valid_zone(self)->arcade.Sprite:
        """
        Generate a sprite in front of the character,
        to detect correct input when an obstacle arrive.
        """
        valid_zone = arcade.Sprite("../ressources/Lane_Valid_Zone.png")
        valid_zone.center_x = (self.SCREEN_WIDTH // 10) * 2
        valid_zone.center_y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 3)*self.tier + 90
        valid_zone.color = (0, 0, 0) # To visualise if drawn
        return valid_zone

    def action(self, obstacle_list: arcade.SpriteList)-> EnumAction:
        """
        Called when a button is pressed, Jump and check if an obstacle is in the valid zone.
        """

        result = EnumAction.miss
        if self.physics_engine.can_jump(5):
            for collision in arcade.check_for_collision_with_list(self.valid_zone,
                                                                  obstacle_list):
                collision.hit = True
                if collision.collides_with_point((self.valid_zone.center_x, collision.center_y)):
                    result = EnumAction.perfect
                elif collision.right < self.valid_zone.right and collision.left > self.valid_zone.left:
                    result = EnumAction.super
                else:
                    result = EnumAction.ok
            self.physics_engine.jump(6)
        return result

    def generate_background(self, sprite_path: str, speed: int, offset: int)->list:
        """
        Generate background sprite on the lane.
        :param sprite_path: The path to the sprite. Sprite must be the size of the Screen.
        :param speed: The scrolling speed.
        :param offset: Magic Number :c to place them 'right'. 107 for Q, -93 for W.
        """
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
