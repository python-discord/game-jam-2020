import arcade

class Character(arcade.Sprite):

    def __init__(self, image_path: str, starting_pixel_y):
        super().__init__(image_path)
        self.center_y = starting_pixel_y
        self.starting_pixel_y = starting_pixel_y


    def action(self):
        self.change_y += 35
