
from Enemy import Enemy

class Slime(Enemy):
    def __init__(self, texture, x, y):
        super().__init__(texture, x, y)

        self.movespeed = 2
        self.jump_height = 4

        self.curr_move_cd = 0
        self.move_cd = 24

    def update(self):

        super().update()

    def move_to(self, entity):
        if self.curr_move_cd == 0:
            if not self.jumping:
                self.change_y = self.jump_height

                if self.center_x > entity.center_x:
                    self.change_x = -self.movespeed
                elif self.center_x < entity.center_x:
                    self.change_x = self.movespeed
            self.jumping = True
            self.curr_move_cd = self.move_cd
        else:
            self.curr_move_cd -= 1

