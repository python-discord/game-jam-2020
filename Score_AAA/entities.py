import arcade
from random import randint


class Character(arcade.Sprite):
    def __init__(
        self,
        image_path: str,
        starting_pixel_y: int,
        run_textures: list,
        dico_texture: dict,
    ):
        super().__init__(image_path)
        self.center_y = starting_pixel_y
        self.run_textures = run_textures
        self.cur_texture = 0
        self.refresh_animation = 8
        self.dico_texture = dico_texture

    def update(self):
        self.position = [
            self._position[0] + self.change_x,
            self._position[1] + self.change_y,
        ]
        self.angle += self.change_angle
        self.cur_texture += 1
        if self.run_textures:
            if self.cur_texture >= len(self.dico_texture) * self.refresh_animation:
                self.cur_texture = 0
            self.texture = self.run_textures[
                self.dico_texture[self.cur_texture // self.refresh_animation]
            ]


class Obstacle(arcade.Sprite):
    def __init__(self, image_path: str):
        super().__init__(image_path)
        self.hit = False

    def update(self):
        self.position = [
            self._position[0] + self.change_x,
            self._position[1] + self.change_y,
        ]
        self.angle += self.change_angle
        if self.hit is True:
            self.color = (85, 85, 85)


class Splash(arcade.Sprite):
    def __init__(self, type, position):
        if type == "ok":
            path = "../ressources/splash_ok.png"
        elif type == "super":
            path = "../ressources/splash_super.png"
        elif type == "perfect":
            path = "../ressources/splash_perfect.png"
        else:
            path = "../ressources/splash_miss.png"
        super().__init__(path)
        self.gravity = 0.5
        self.center_x = position[0]
        self.center_y = position[1]
        self.age = 0.75
        self.change_y = randint(3, 5)
        self.change_x = randint(1, 2)

    def update(self):
        self.position = [
            self._position[0] + self.change_x,
            self._position[1] + self.change_y,
        ]
        self.angle += self.change_angle
        self.change_y -= self.gravity

    def update_age(self, delta_time):
        self.age -= delta_time
        if self.age < 0:
            self.remove_from_sprite_lists()


class Background(arcade.Sprite):
    def __init__(self, sprite_path: str, SCREEN_WIDTH: int):
        super().__init__(sprite_path)
        self.SCREEN_WIDTH = SCREEN_WIDTH

    def update(self):
        self.position = [
            self._position[0] + self.change_x,
            self._position[1] + self.change_y,
        ]
        self.angle += self.change_angle
        if self.right < 0:
            self.center_x = self.SCREEN_WIDTH + self.SCREEN_WIDTH // 2
