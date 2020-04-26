from game import window

import random
import copy

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
        self.hitpoints = min(self.max_hitpoints, self.hitpoints)
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

""" Note for future reference: draw() stuff like setting hitbox *should* have happened above, but it's too late to adjust. """

class Effect(arcade.AnimatedTimeBasedSprite):
    # def __init__(self, center_x, center_y, change_x, change_y, hitpoints, damage, projectile, screen_number, sprites, scale):
        # super().__init__(center_x=center_x, center_y=center_y, scale=scale)
    def __init__(self, center_x, center_y, rotation, function, timespan, screen_number, state_length=None, num_states=1):
        super().__init__(center_x=center_x, center_y=center_y)
        self.screen_number = screen_number
        self.initial_x, self.initial_y = center_x, center_y
        self.change_x, self.change_y = 0, 0
        self.function = function
        self.rotation = rotation
        self.created_timestamp = window.frame
        self.timespan = timespan
        self.state_length = state_length or window.animation_length
        self.num_states = num_states
        self.state = 0
        self.draw()
    def die(self):
        self.remove_from_sprite_lists()
    def update(self):
        if window.frame-self.created_timestamp >= self.timespan:
            self.die()
        self.change_x, self.change_y, self.rotation = self.function(window.frame-self.created_timestamp)
        self.center_x, self.center_y = self.initial_x+self.change_x, self.initial_y+self.change_y
        self.state = (window.frame // self.state_length) % self.num_states
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


class Star(Effect):
    def __init__(self, center_x, center_y, screen_number, rotation, timespan):
        a, b = random.choice((-1, 1)), random.choice((-1, 1))
        def math(time):
            return (a*time**2/2, b*time*2, time)
        super().__init__(center_x, center_y, rotation, math, timespan, screen_number)
    def draw(self):
        self.text_object = arcade.draw_text('*', self.center_x, self.center_y, arcade.color.YELLOW, rotation=self.rotation, font_size=13.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())


class Boom(Effect):
    def __init__(self, center_x, center_y, screen_number, rotation, timespan):
        def math(time):
            return (0, time, 0)
        super().__init__(center_x, center_y, rotation, math, timespan, screen_number)
    def draw(self):
        self.text_object = arcade.draw_text('BOOM', self.center_x, self.center_y, arcade.color.RED, rotation=self.rotation, font_size=13.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())


class Projectile(Entity):
    def collide(self, other):
        if self.invincible > 0:
            return
        if 'Mirror' in type(other).__name__:
            self.invincible = window.invincible_length
            self.change_y = -self.change_y
            return
        window.effect_list.append(Star(self.center_x, self.center_y, self.screen_number, 45.0, 7))
        super().collide(other)


class Bullet(Projectile):
    def draw(self):
        self.text_object = arcade.draw_text('#', self.center_x, self.center_y, arcade.color.FUCHSIA, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())


class TriBullet(Projectile):
    def draw(self):
        self.text_object = arcade.draw_text('###', self.center_x, self.center_y, arcade.color.FUCHSIA, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def die(self):
        window.entity_list.append(Bullet(self.center_x, self.center_y, 3, self.change_y, self.max_hitpoints, self.damage, self.screen_number, self.state_length, self.num_states))
        window.entity_list.append(Bullet(self.center_x, self.center_y, 0, self.change_y, self.max_hitpoints, self.damage, self.screen_number, self.state_length, self.num_states))
        window.entity_list.append(Bullet(self.center_x, self.center_y, -3, self.change_y, self.max_hitpoints, self.damage, self.screen_number, self.state_length, self.num_states))
        self.remove_from_sprite_lists()
        # spawn new bullets at angle


class Heal(Projectile):
    def __init__(self, center_x, center_y, change_x, change_y, heal_amount, screen_number):
        super().__init__(center_x, center_y, change_x, change_y, 1, -heal_amount, 0, screen_number)
    def draw(self):
        self.text_object = arcade.draw_text('+', self.center_x, self.center_y, arcade.color.GREEN, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())


class TribulletPowerup(Projectile):
    def __init__(self, center_x, center_y, change_x, change_y, heal_amount, screen_number):
        super().__init__(center_x, center_y, change_x, change_y, 0, 0, screen_number)
    def draw(self):
        self.text_object = arcade.draw_text('%', self.center_x, self.center_y, arcade.color.YELLOW, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def collide(self, other):
        try:
            if other.projectile != None:
                other.projectile['type'] = TriBullet
            self.die()
        except:
            return


class AttackPowerup(Projectile):
    def __init__(self, center_x, center_y, change_x, change_y, heal_amount, screen_number):
        super().__init__(center_x, center_y, change_x, change_y, 0, 0, screen_number)
    def draw(self):
        self.text_object = arcade.draw_text('@', self.center_x, self.center_y, arcade.color.YELLOW, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def collide(self, other):
        try:
            if other.projectile != None:
                other.projectile['damage'] += 25
            self.die()
        except:
            return


class SpeedPowerup(Projectile):
    def __init__(self, center_x, center_y, change_x, change_y, heal_amount, screen_number):
        super().__init__(center_x, center_y, change_x, change_y, 0, 0, screen_number)
    def draw(self):
        self.text_object = arcade.draw_text('$', self.center_x, self.center_y, arcade.color.YELLOW, font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def collide(self, other):
        try:
            if other.projectile != None:
                if other.projectile['change_y'] > 0:
                    other.projectile['change_y'] += 1
                else:
                    other.projectile['change_y'] -= 1
                self.die()
        except:
            return


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
        if self.cooldown <= 0 and type(self).__name__ != 'Player' and self.projectile is not None:
            self.fire_projectile()
    def die(self):
        self.remove_from_sprite_lists()
        window.effect_list.append(Boom(self.center_x, self.center_y, self.screen_number, 0, 10))


class Player(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 100, 100, screen_number, projectile={'type': Bullet, 'change_x': 0, 'change_y': 10, 'max_hitpoints': 25, 'damage': 25}, fire_rate=10)
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
            self.text_object = arcade.draw_text('(@@@)', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 1:
            self.text_object = arcade.draw_text('(-->)', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 2:
            self.text_object = arcade.draw_text('(<--)', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 3:
            self.text_object = arcade.draw_text('(===)', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
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
        self.text_object = arcade.draw_text('-PEW-', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
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
            self.text_object = arcade.draw_text('#POW#', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 1:
            self.text_object = arcade.draw_text('#P-W#', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
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


class Mirror(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 150, 150, screen_number)
    def draw(self):
        self.text_object = arcade.draw_text('^___^', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    # def collide(self, other):
    #     projectile = copy.copy(other)
    #     projectile.invincible = window.invincible_length
    #     projectile.change_y = -projectile.change_y
    #     window.entity_list.append(projectile)
    #     super().collide(other)
    def update(self):
        self.change_y = -2
        super().update(no_set_state=True)
        if window.frame % self.state_length == 0:
            self.state = random.randint(0, 3)


class PortableHandMirror(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 100, 100, screen_number, 125, 2, None, None)
    def draw(self):
        if self.state == 0:
            self.text_object = arcade.draw_text('/___/', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        elif self.state == 1:
            self.text_object = arcade.draw_text('\\___\\', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    # def collide(self, other):
    #     projectile = copy.copy(other)
    #     projectile.change_y = -projectile.change_y
    #     window.entity_list.append(projectile)
    #     super().collide(other)
    def update(self):
        if self.state == 0:
            self.change_x = 3
        elif self.state == 1:
            self.change_x = -3
        self.change_y = -2
        super().update()


class Wall(AI):
    def __init__(self, center_x, center_y, screen_number):
        super().__init__(center_x, center_y, 0, 0, 500, 500, screen_number)
    def draw(self):
        self.text_object = arcade.draw_text('----', self.center_x, self.center_y, self.ramped_color(), font_size=15.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
    def update(self):
        self.change_y = -1
        super().update(no_set_state=True)
        if window.frame % self.state_length == 0:
            self.state = random.randint(0, 3)
