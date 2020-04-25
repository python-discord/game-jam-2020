from game import window

import random

import arcade

# class Entity():
#     def __init__(self, attributes):
#         """ Main things necessary: sprite and position. """
#         self.__dict__.update(attributes)
#     @classmethod
#     def from_file(cls, *args):
#         return Unit(get_resource(*args))
#     def update(self, )

class Entity(arcade.AnimatedTimeBasedSprite):
    # def __init__(self, center_x, center_y, change_x, change_y, hitpoints, damage, projectile, screen_number, sprites, scale):
        # super().__init__(center_x=center_x, center_y=center_y, scale=scale)
    def __init__(self, center_x, center_y, change_x, change_y, max_hitpoints, damage, screen_number, state_length=None, num_states=1):
        super().__init__(center_x=center_x, center_y=center_y)
        self.screen_number = screen_number
        self.change_x, self.change_y = change_x, change_y
        self.max_hitpoints = max_hitpoints
        self.hitpoints = max_hitpoints
        self.damage = damage
        self.invincible = window.invincible_length
        self.state_length = state_length or window.animation_length
        self.num_states = num_states
        self.state = 0
        # self.sprite = sprites[0] # Sprites is tuple of base name and number of frames.
        # self.frames = sprites[1]
        # self.texture = window.textures[self.sprite+'0']
        self.draw()
    def take_damage(self, damage):
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            self.die()
        else:
            self.invincible = window.invincible_length
    def ramped_color(self):
        if self.hitpoints <= self.max_hitpoints/4:
            return arcade.color.AMERICAN_ROSE
        elif self.hitpoints <= self.max_hitpoints/2:
            return arcade.color.AUREOLIN
        return arcade.color.WHITE
    def die(self):
        self.remove_from_sprite_lists()
    def collide(self, other):
        if self.invincible > 0:
            return
        self.take_damage(other.damage)
    def update(self, no_set_state=False):
        if not no_set_state:
            self.state = (window.frame // self.state_length) % self.num_states
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.invincible -= 1
        if self.bottom < window.bottom_height:
            self.die()
        if self.top > window._height:
            self.die()
        if self.left < self.screen_number*window._each_screen_width+window.padding:
            self.left = self.screen_number*window._each_screen_width+window.padding
        if self.right > (self.screen_number+1)*window._each_screen_width-window.padding:
            self.right = (self.screen_number+1)*window._each_screen_width-window.padding
    def draw(self):
        pass
    # def update_animation(self, delta_time: float = 1/60):
    #     self.texture = window.textures[self.sprite+str((window.frame//window.animation_length)%self.frames)]

class Projectile(Entity):
    pass


class Bullet(Projectile):
    def draw(self):
        self.text_object = arcade.draw_text('#', self.center_x, self.center_y, arcade.color.FUCHSIA, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())

class TriBullet(Projectile):
    def draw(self):
        self.text_object = arcade.draw_text('^^^', self.center_x, self.center_y, arcade.color.FUCHSIA, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def die(self):
        window.entity_list.append(Bullet(self.center_x, self.center_y, 3, self.change_y, self.max_hitpoints, self.damage, self.screen_number, self.state_length, self.num_states))
        window.entity_list.append(Bullet(self.center_x, self.center_y, 0, self.change_y, self.max_hitpoints, self.damage, self.screen_number, self.state_length, self.num_states))
        window.entity_list.append(Bullet(self.center_x, self.center_y, -3, self.change_y, self.max_hitpoints, self.damage, self.screen_number, self.state_length, self.num_states))
        self.remove_from_sprite_lists()
        # spawn new bullets at angle


class AI(Entity):
    # Entities specifically with actual movements, firing, etc.
    def __init__(self, center_x, center_y, change_x, change_y, max_hitpoints, damage, screen_number, state_length=None, num_states=1, projectile=None, fire_rate=25):
        super().__init__(center_x, center_y, change_x, change_y, max_hitpoints, damage, screen_number, state_length, num_states)
        self.projectile = projectile
        self.fire_rate = fire_rate
        self.cooldown = 0
    def fire_projectile(self, x=None, y=None):
        if self.cooldown > 0:
            return
        window.entity_list.append(self.projectile['type'](
            x or self.center_x, y or self.center_y,
            self.projectile['change_x'], self.projectile['change_y'],
            self.projectile['max_hitpoints'], self.projectile['damage'],
            self.screen_number
        ))
        self.cooldown = self.fire_rate
        self.invincible = window.invincible_length
    def update(self, no_set_state=False):
        super().update(no_set_state)
        self.cooldown -= 1
        if self.cooldown <= 0 and type(self).__name__ != 'Player':
            self.fire_projectile()


class Player(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 100, 100, screen_number, projectile={'type': Bullet, 'change_x': 0, 'change_y': 10, 'max_hitpoints': 1, 'damage': 25}, fire_rate=10)
    def draw(self):
        self.text_object = arcade.draw_text('shp', self.center_x, self.center_y, arcade.color.GREEN, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
        # self.set_hit_box(self.text_object.get_adjusted_hit_box())


class Waffle(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 100, 100, screen_number, 125, 2, None, None)
    def draw(self):
        if self.state == 0:
            self.text_object = arcade.draw_text('/wfl/', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 1:
            self.text_object = arcade.draw_text('\\wfl\\', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def update(self):
        if self.state == 0:
            self.change_x = 3
        elif self.state == 1:
            self.change_x = -3
        self.change_y = -3
        super().update()


class Reggae(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 50, 50, screen_number, 25, 2, None, None)
    def draw(self):
        if self.state == 0:
            self.text_object = arcade.draw_text(f'{self.state}|stp|', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 1:
            self.text_object = arcade.draw_text(f'{self.state}|-*->', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 2:
            self.text_object = arcade.draw_text(f'{self.state}<-*-|', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 3:
            self.text_object = arcade.draw_text(f'{self.state}/bck\\', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def update(self):
        if self.state == 0:
            self.change_x, self.change_y = 0, 0
        elif self.state == 1:
            self.change_x, self.change_y = 5, -5
        elif self.state == 2:
            self.change_x, self.change_y = -5, -5
        elif self.state == 3:
            if self.top > window._height - 10:
                self.change_x, self.change_y = 5, 0
            else:
                self.change_x, self.change_y = 5, 5
        super().update(no_set_state=True)
        if window.frame % self.state_length == 0:
            self.state = random.randint(0, 3)


class Sniper(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 100, 100, screen_number, projectile={'type': Bullet, 'change_x': 0, 'change_y': -10, 'max_hitpoints': 50, 'damage': 25}, fire_rate=50)
    def draw(self):
        self.text_object = arcade.draw_text('PEW', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def update(self):
        self.change_y = -2
        super().update()


class Whiffle(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 150, 150, screen_number, projectile={'type': Bullet, 'change_x': 0, 'change_y': -20, 'max_hitpoints': 50, 'damage': 25}, fire_rate=75)
    def draw(self):
        if self.state == 0:
            self.text_object = arcade.draw_text('POW', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 1:
            self.text_object = arcade.draw_text('POW', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def update(self):
        if self.state == 0:
            self.change_x = 1
        elif self.state == 1:
            self.change_x = -1
        self.change_y = -1
        super().update()


class Oontz(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 100, 100, screen_number, 15, 2, projectile={'type': Bullet, 'change_x': 0, 'change_y': -20, 'max_hitpoints': 50, 'damage': 25}, fire_rate=35)
    def draw(self):
        if self.state == 0:
            self.text_object = arcade.draw_text('[@@@]', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 1:
            self.text_object = arcade.draw_text('[-->]', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 2:
            self.text_object = arcade.draw_text('[<--]', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 3:
            self.text_object = arcade.draw_text('[===]', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def update(self):
        if self.state == 0:
            self.change_x, self.change_y = 0, 0
        elif self.state == 1:
            self.change_x, self.change_y = 5, -5
        elif self.state == 2:
            self.change_x, self.change_y = -5, -5
        elif self.state == 3:
            if self.top > window._height - 10:
                self.change_x, self.change_y = 5, 0
            else:
                self.change_x, self.change_y = 5, 5
        super().update(no_set_state=True)
        if window.frame % self.state_length == 0:
            self.state = random.randint(0, 3)
