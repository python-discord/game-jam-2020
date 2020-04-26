from game import SpriteList

import arcade

import os
import random


class Game(arcade.Window):
    """ This is the main application, stores handy globals. """
    def __init__(self):
        self._each_screen_width = 400
        self._height = 800
        self._width = self._each_screen_width*3
        self.bottom_height = 150
        self.padding = 10
        self.invincible_length = 5
        self.animation_length = 50
        super().__init__(self._width, self._height, 'qaqe')
        self.keypressed = {}
        self.classes = {}
        self.state = 'title_screen'
    def on_key_press(self, key, modifiers):
        self.keypressed[key] = True
    def on_key_release(self, key, modifiers):
        self.keypressed[key] = False
    def on_draw(self):
        arcade.start_render()
        if self.state == 'title_screen':
            arcade.draw_text(f'not ducky', self._width/2, self._height/2+100, arcade.color.GREEN, font_size=25.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
            arcade.draw_text(f'[1] start the game', self._width/2, self._height/2+25, arcade.color.WHITE, font_size=15.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
            arcade.draw_text(f'[2] host multiplayer', self._width/2, self._height/2, arcade.color.WHITE, font_size=15.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
            arcade.draw_text(f'[3] join multiplayer', self._width/2, self._height/2-25, arcade.color.WHITE, font_size=15.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
        elif self.state == 'game_running':
            self.players.draw()
            self.entity_list.draw()
            self.effect_list.draw()
            for i in range(2):
                arcade.draw_text('* '*100, self._each_screen_width*(i+1), self.bottom_height, arcade.color.WHITE, font_size=15.0, rotation=90.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
            for i, player in enumerate(self.players):
                arcade.draw_text(f'hp: {player.hitpoints}', self._each_screen_width*(i+0.5), self.bottom_height/2, arcade.color.RED, font_size=15.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
            for i in range(3):
                arcade.draw_text(f'{self.scores[i]}', self._each_screen_width*(i+0.5), self.bottom_height/2-20, arcade.color.WHITE, font_size=15.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
        elif self.state == 'game_over':
            arcade.draw_text(f'Game Over', self._width/2, self._height/2+100, arcade.color.WHITE, font_size=25.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
            arcade.draw_text(f'Scores:', self._width/2, self._height/2+25, arcade.color.WHITE, font_size=15.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
            for i in range(3):
                arcade.draw_text(f'{self.scores[i]}', self._width/2-(40*(i-1)), self._height/2, arcade.color.WHITE, font_size=15.0, anchor_x='center', anchor_y='bottom', font_name='./game/resources/uni0553.ttf')
    def on_update(self, delta_time):
        if self.state == 'title_screen':
            if self.keypressed.get(arcade.key.KEY_1, False):
                self.state = 'game_running'
                self.entity_list = SpriteList()
                self.effect_list = SpriteList()
                self.players = SpriteList()
                self.frame = 0
                self.next_spawn = {0: 0, 1: 0, 2: 0}
                self.next_spawn_powerup = {0: 500, 1: 500, 2: 500}
                self.pool = ['Waffle', 'Sniper']
                self.pool_powerup = ['Heal', 'TribulletPowerup', 'AttackPowerup', 'SpeedPowerup']
                self.scores = {0: 0, 1: 0, 2: 0}
                for i in range(3):
                    self.players.append(self.classes['Player'](
                        center_x=i*self._each_screen_width+self._each_screen_width/2, center_y = self.bottom_height+self.padding*2,
                        screen_number=i
                    ))
            return
        elif self.state == 'game_over':
            return
        # if self.frame == 20:
        #     self.entity_list.append(self.classes['Wall'](150, self._height-50, 0))
        self.frame += 1
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
        self.players.update()
        self.entity_list.update()
        self.effect_list.update()
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
        if self.frame == 1000:
            self.pool.append('Whiffle')
        if self.frame == 1500:
            self.pool.append('Reggae')
        if self.frame == 2500:
            self.pool.append('Oontz')
            self.pool.append('Mirror')
            self.pool.append('PortableHandMirror')
        for i in range(3):
            bounds = (self._each_screen_width*i, self._each_screen_width*(i+1))
            if self.next_spawn[i] == 0:
                self.entity_list.append(self.classes[random.choice(self.pool)](random.randint(*bounds), self._height, i))
                self.entity_list[-1].top=self._height
                self.next_spawn[i] = random.randint(int(max(500-self.frame/4, 150)), int(max(750-self.frame/3, 200)))
            self.next_spawn[i] -= 1
            if self.next_spawn_powerup[i] == 0:
                self.entity_list.append(self.classes[random.choice(self.pool_powerup)](random.randint(*bounds), self._height, 0, -5, 50, i))
                self.entity_list[-1].top=self._height
                self.next_spawn_powerup[i] = random.randint(int(max(500-self.frame/4, 150)), int(max(750-self.frame/3, 200)))
            self.next_spawn_powerup[i] -= 1
        if len(self.players) != 3:
            self.state = 'game_over'
