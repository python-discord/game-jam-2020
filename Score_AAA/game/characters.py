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

