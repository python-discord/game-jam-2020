from game import SpriteList

import arcade

import os


class Game(arcade.Window):
    """ This is the main application, stores handy globals. """
    def __init__(self):
        self._each_screen_width = 400
        self._height = 800
        self._width = 1200
        self.bottom_height = 150
        self.padding = 10
        self.invincible_length = 5
        self.animation_length = 50
        super().__init__(self._width, self._height, 'qaqe')
        self.entity_list = SpriteList()
        self.players = SpriteList()
        self.keypressed = {}
        self.textures = {}
        self.frame = 0
        self.classes = {}
        for root, directories, files in os.walk('./game/resources/'):
            for file in files:
                if file.split('.')[-1] != 'png':
                    continue
                self.textures['.'.join(file.split('.')[:-1])] = arcade.load_texture(os.path.join(root, file))
    def setup(self):
        for i in range(3):
            self.players.append(self.classes['Player'](
                center_x=i*self._each_screen_width+self._each_screen_width/2, center_y = self.bottom_height+self.padding*2,
                screen_number=i
            ))
    def on_key_press(self, key, modifiers):
        self.keypressed[key] = True
    def on_key_release(self, key, modifiers):
        self.keypressed[key] = False
    def on_draw(self):
        arcade.start_render()
        self.players.draw()
        self.entity_list.draw()
        for i in range(2):
            arcade.draw_text('* '*100, self._each_screen_width*(i+1), self.bottom_height, arcade.color.WHITE, font_size=15.0, rotation=90.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
        for i, player in enumerate(self.players):
            arcade.draw_text(f'hp: {player.hitpoints}', self._each_screen_width*(i+0.5), 0, arcade.color.RED, font_size=15.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
    def on_update(self, delta_time):
        self.frame += 1
        if self.frame == 100:
            self.entity_list.append(self.classes['Oontz'](50, 700, 0))
        self.players.update()
        self.entity_list.update()
        for player in self.players:
            player.change_x = 0
            player.change_y = 0
        if self.keypressed.get(arcade.key.K, False):
            self.players[2].change_x = 5
        if self.keypressed.get(arcade.key.J, False):
            self.players[2].change_x = -5
        if self.keypressed.get(arcade.key.F, False):
            self.players[1].change_x = 5
        if self.keypressed.get(arcade.key.D, False):
            self.players[1].change_x = -5
        if self.keypressed.get(arcade.key.S, False):
            self.players[0].change_x = 5
        if self.keypressed.get(arcade.key.A, False):
            self.players[0].change_x = -5
        if self.keypressed.get(arcade.key.SPACE, False):
            for i in range(3):
                self.players[i].fire_projectile()
        for player in self.players:
            for other in player.collides_with_list(self.entity_list):
                player.collide(other)
                other.collide(player)
        for entity in self.entity_list:
            for other in entity.collides_with_list(self.entity_list):
                if other is entity:
                    continue
                entity.collide(other)
                other.collide(entity)
