from .constants import JUMP_FORCE, JUMP_FORCE_REDUCTION
import arcade


class Player(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.movement_x = 0
        self.previous_movement_x = 0
        self.movement_control = 0.5
        self.is_jumping = False
        self.jump_force = JUMP_FORCE
        self.jump_count = 0

    def update(self):
        if self.is_jumping:
            self.change_y += self.jump_force
            self.jump_force *= JUMP_FORCE_REDUCTION
        self.change_x = (self.movement_x * self.movement_control + self.previous_movement_x) / (1 + self.movement_control)
        self.previous_movement_x = self.change_x
