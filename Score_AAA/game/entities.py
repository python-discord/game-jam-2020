import arcade

class Character(arcade.Sprite):

    def __init__(self, image_path: str, starting_pixel_y: int, run_textures: list):
        super().__init__(image_path)
        self.center_y = starting_pixel_y
        self.run_textures = run_textures
        self.cur_texture = 0
        self.refresh_animation = 8
        self.dico_texture = {0: 0, 1: 1, 2: 2, 3: 3, 4: 2, 5: 1}

    def update(self):
        self.position = [self._position[0] + self.change_x, self._position[1] + self.change_y]
        self.angle += self.change_angle
        self.cur_texture += 1
        if self.run_textures:
            if self.cur_texture >= 5 * self.refresh_animation:
                self.cur_texture = 0
            self.texture = self.run_textures[self.dico_texture[self.cur_texture // self.refresh_animation]]

class Obstacle(arcade.Sprite):

    def __init__(self, image_path: str):
        super().__init__(image_path)
        self.hit = False

    def update(self):
        self.position = [self._position[0] + self.change_x, self._position[1] + self.change_y]
        self.angle += self.change_angle
        if self.hit is True:
            self.color = (85, 85, 85)

class Splash(arcade.Sprite):

    def __init__(self, type, position):
        if type == "super":
            path = "../ressources/splash_super.png"
        else:
            path = "../ressources/splash_super.png"
        super().__init__(path)
        self.center_x = position[0]
        self.center_y = position[1]
        self.age = 1.5

    def update_age(self, delta_time):
        self.age -= delta_time
        if self.age < 0:
            self.remove_from_sprite_lists()
