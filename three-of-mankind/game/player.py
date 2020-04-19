import arcade


class Player(arcade.Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.movement_x = 0
        self.previous_movement_x = 0
        self.movement_control = 0.5

    def update(self):
        self.change_x = (self.movement_x * self.movement_control + self.previous_movement_x) / (1 + self.movement_control)
        self.previous_movement_x = self.change_x
