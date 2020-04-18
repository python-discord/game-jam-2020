import arcade

from constants import ASSETS, WIDTH, HEIGHT, SPEED, SCALING


class Player(arcade.Sprite):
    TEXTURES = [
        'jump_0', 'jump_1', 'jump_2', 'jump_3', 'walk_forward',
        'walk_right_0', 'walk_right_1', 'walk_right_2', 'walk_right_3',
        'walk_forward_u', 'walk_right_0_u', 'walk_right_1_u',
        'walk_right_2_u', 'walk_right_3_u'
    ]

    def __init__(
            self, game, x=WIDTH//5, y=HEIGHT//2, speed=SPEED,
            image=ASSETS+'player_{}.png'
            ):
        super().__init__(
            image.format('jump_0'), center_x=x, center_y=y, 
            scale=SCALING*0.25
        )
        self.image = image
        self.textures = []
        for texture in Player.TEXTURES:
            self.textures.append(arcade.load_texture(
                image.format(texture)
            ))
        self.scale = SCALING * 0.25
        self.game = game
        self.speed = speed
        self.time_since_change = 0
        self.num = 0
        self.cooldown = 1

    def can_move(self):
        return True

    def update(self, timedelta):
        self.cooldown -= timedelta
        # check touching sprites
        gems = arcade.check_for_collision_with_list(self, self.game.gems)
        for gem in gems:
            for box in self.game.boxes:
                if not box.colour:
                    box.add_gem(gem.colour)
                    break
            gem.place()

        # check key presses
        if arcade.key.SPACE in self.game.pressed:
            if not self.change_y and self.cooldown < 0:
                if self.game.engine.can_jump():
                    self.game.engine.gravity_constant *= -1
                    self.cooldown = 1

        if self.can_move():
            self.change_x = self.speed
            if self.center_x < self.game.left + WIDTH//5:
                self.change_x *= 1.5

        self.time_since_change += timedelta
        if self.time_since_change > 0.1:
            self.time_since_change = 0
            self.num += 1
            self.num %= 4

        if not self.can_move():
            name = 'walk_forward'
        elif self.game.engine.can_jump():
            name = f'walk_right_{self.num}'
            if self.game.engine.gravity_constant < 0:
                name += '_u'
        else:
            name = f'jump_{self.num}'
        self.texture = self.textures[Player.TEXTURES.index(name)]
