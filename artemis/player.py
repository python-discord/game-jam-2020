import arcade

from constants import ASSETS, WIDTH, HEIGHT, SPEED, SCALING


class Player(arcade.Sprite):
    TEXTURES = [
        'jump_0', 'jump_1', 'jump_2', 'jump_3', 'walk_forward_up',
        'walk_right_0_up', 'walk_right_1_up', 'walk_right_2_up',
        'walk_right_3_up', 'walk_forward_down', 'walk_right_0_down',
        'walk_right_1_down', 'walk_right_2_down', 'walk_right_3_down'
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
        self.last_x = -1

    def switch(self):
        if self.game.engine.can_jump():
            self.game.engine.gravity_constant *= -1

    def update(self, timedelta):
        direction = ['up', 'down'][self.game.engine.gravity_constant < 0]
        if abs(self.center_x - self.last_x) < 1:
            name = f'walk_forward_{direction}'
        elif self.game.engine.can_jump():
            name = f'walk_right_{self.num}_{direction}'
        else:
            name = f'jump_{self.num}'
        self.texture = self.textures[Player.TEXTURES.index(name)]

        self.last_x = self.center_x

        # check touching sprites
        gems = arcade.check_for_collision_with_list(self, self.game.gems)
        for gem in gems:
            for box in self.game.boxes:
                if not box.colour:
                    box.add_gem(gem.colour)
                    break
            gem.place()

        spikes = arcade.check_for_collision_with_list(self, self.game.spikes)
        if spikes:
            self.game.game_over('Hit a Spike')
            return

        self.change_x = self.speed
        if self.center_x < self.game.left + WIDTH//5:
            self.change_x *= 1.5

        self.time_since_change += timedelta
        if self.time_since_change > 0.1:
            self.time_since_change = 0
            self.num += 1
            self.num %= 4
