from game import SpriteList

import arcade

import os


class Game(arcade.Window):
    """ This is the main application, stores handy globals. """
    def __init__(self):
        self._each_screen_height = 300
        self._width = 900
        self.animation_length = 5
        super().__init__(self._width, self._each_screen_height*3, 'qaqe')
        self.entity_list = SpriteList()
        self.bullet_list = SpriteList()
        self.players = SpriteList()
        self.keypressed = {}
        self.textures = {}
        self.frame = 0
        for root, directories, files in os.walk('./game/resources/'):
            for file in files:
                if file.split('.')[-1] != 'png':
                    continue
                self.textures['.'.join(file.split('.')[:-1])] = arcade.load_texture(os.path.join(root, file))
    def setup(self):
        from game import Player, Bullet
        for i in range(3):
            self.players.append(Player(
                center_x=50, center_y=i*300+150, change_x=0, change_y=0,
                hitpoints=100, damage=50,
                projectile={'type': Bullet, 'change_x': 10, 'change_y': 0},
                screen_number=i,
            ))
    def on_key_press(self, key, modifiers):
        self.keypressed[key] = True
    def on_key_release(self, key, modifiers):
        self.keypressed[key] = False
    def on_draw(self):
        arcade.start_render()
        self.players.draw()
    def on_update(self, delta_time):
        self.frame += 1
        for player in self.players:
            player.change_x = 0
            player.change_y = 0
        if self.keypressed.get(arcade.key.A, False):
            self.players[0].change_y = 10
        if self.keypressed.get(arcade.key.S, False):
            self.players[0].change_y = -10
        self.players.update()
