from game import window

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
    def __init__(self, center_x, center_y, change_x, change_y, hitpoints, damage, projectile, screen_number):
        super().__init__(center_x=center_x, center_y=center_y)
        self.hitpoints = hitpoints
        self.damage = damage
        self.projectile = projectile
        self.screen_number = screen_number
        # self.sprite = sprites[0] # Sprites is tuple of base name and number of frames.
        # self.frames = sprites[1]
        # self.texture = window.textures[self.sprite+'0']
    def take_damage(self, damage):
        self.hitpoints -= damage
    def die(self):
        self.remove_from_sprite_lists()
    def collide(self, other):
        self.take_damage(other.damage)
    def fire_projectile(self):
        window.projectile_list.append(self.projectile['type'](self.center_x, self.center_y, self.projectile['change_x'], self.projectile['change_y']))
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        if self.right > window._width:
            self.right = window._width
        if self.bottom < self.screen_number*window._each_screen_height:
            self.bottom = 0
        if self.top > (self.screen_number+1)*window._each_screen_height:
            self.top = (self.screen_number+1)*window._each_screen_height
    def draw(self):
        pass
    # def update_animation(self, delta_time: float = 1/60):
    #     self.texture = window.textures[self.sprite+str((window.frame//window.animation_length)%self.frames)]

class Projectile(Entity):
    pass


class Bullet(Projectile):
    # @classmethod
    # def get_bullet_constructor(cls, hitpoints, damage):
    #     def create_bullet(center_x, center_y, change_x, change_y):
    #         return cls(center_x, center_y, change_x, change_y, hitpoints, damage)
    #     return create_bullet
    pass


class TriBullet(Projectile):
    def die(self):
        self.remove_from_sprite_lists()
        # spawn new bullets at angle


class Player(Entity):
    def __init__(self, center_x, center_y, change_x, change_y, hitpoints, damage, projectile, screen_number):
        super().__init__(center_x, center_y, change_x, change_y, hitpoints, damage, projectile, screen_number)
        self.set_hit_box(((-1.0, -1.0), (100.0, 1.0), (1.0, 1.0), (1.0, -1.0)))
        self.angle = 90.0
    def draw(self):
        self.text_object = arcade.draw_text('@#@', self.center_x, self.center_y, arcade.color.WHITE, font_size=15.0, rotation=90.0, anchor_x='center', anchor_y='center', font_name='./game/resources/uni0553.ttf')
        self.texture = self.text_object.texture
        self.set_hit_box(self.text_object.get_hit_box())
        # self.set_hit_box(self.text_object.get_adjusted_hit_box())
