import random
import math
import arcade
import os
import pymunk
from PIL import Image

from typing import cast

SCALE = 1
OFFSCREEN_SPACE = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Triple Blocks"
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE
SCREEN_DIST = math.sqrt(SCREEN_HEIGHT**2+SCREEN_WIDTH**2)/2

class GroundSprite(arcade.Sprite):
  def __init__(self, pymunk_shape, textures, scale, x, y):
    super().__init__()
    self.pymunk_shape = pymunk_shape

    self.textures = textures
    self.texture = self.textures[0]

    self.scaling = scale

    self.x = x
    self.y = y

  def update(self,zoom,cx,cy):
    """ Move the sprite """
    super().update()

    self.scale = zoom * self.scaling

    self.center_x = self.pymunk_shape.body.position.x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
    self.center_y = self.pymunk_shape.body.position.y = (self.y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2

class PlayerSprite(arcade.Sprite):
  def __init__(self, pymunk_shape, textures, scale, x, y):
    super().__init__()
    self.pymunk_shape = pymunk_shape
    self.can_jump = True

    self.textures = textures
    self.texture = self.textures[0]

    self.scaling = scale

    self.x = x
    self.y = y

    self.acc_x = 0
    self.acc_y = 0

    self.center_x = self.pymunk_shape.body.position.x
    self.center_y = self.pymunk_shape.body.position.y

    self.og_x = self.center_x
    self.og_y = self.center_y

  def update(self,zoom,cx,cy):
    self.scale = zoom * self.scaling
    self.og_x = self.center_x
    self.og_y = self.center_y

def make_player_sprite(mass,space, textures, scale, x,y, zoom, cx, cy):
  pos_x = (x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
  pos_y = (y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2

  width, height = textures[0].width, textures[0].height
  mass = mass
  moment = pymunk.moment_for_box(mass, (width, height))
  body = pymunk.Body(mass, moment)
  body.position = pymunk.Vec2d((pos_x,pos_y))
  shape = pymunk.Poly.create_box(body, (width, height))
  shape.friction = 0.5
  space.add(body, shape)
  sprite = PlayerSprite(shape, textures, scale,x,y)
  return sprite

def make_ground_sprite(space, textures, scale, x, y, zoom, cx, cy):
  pos_x = (x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
  pos_y = (y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2

  width, height = textures[0].width, textures[0].height
  body = pymunk.Body(body_type=pymunk.Body.STATIC)
  body.position = pymunk.Vec2d((pos_x-width, pos_y-height))
  shape = pymunk.Poly.create_box(body, (width, height))
  shape.friction = 0.5
  space.add(body, shape)
  sprite = GroundSprite(shape, textures, scale, x, y)
  return sprite


class MyGame(arcade.Window):
  """ Main application class. """

  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)

  def start_new_game(self):
    """ Set up the game and initialize the variables. """
    self.frame_count = 0
    self.total_time = 0
    self.game_over = False
    self.debug_mode = False
    self.set_location(0,0)
    self.space = pymunk.Space()
    self.space.gravity = (0.0, -900.0)

    self.camera_zoom = 1
    self.camera_x = SCREEN_WIDTH / -2
    self.camera_y = SCREEN_HEIGHT / -2

    self.key_pressed = [0,0,0] #controllable

    self.ground_sprite_list = arcade.SpriteList()
    self.player_sprite_list = arcade.SpriteList()

    self.selected_player = 0

    self.ground_texture_list = [arcade.load_texture("images/ground/debug.png")]
    self.player_texture_list = [arcade.load_texture("images/player/debug.png")]

    for i in range(1,4):
      object = make_player_sprite(5,self.space,self.player_texture_list,1,i*32,32*1,self.camera_zoom,self.camera_x,self.camera_y)
      object.set_hit_box([[object.width / -2, object.height / -2-1], [object.width /2, object.height / -2-1], [object.width / 2, object.height / 2], [object.width / -2, object.height / 2]])
      self.player_sprite_list.append(object)

    for i in range(1,10):
      object = make_ground_sprite(self.space,self.ground_texture_list,1,i*32,32*-1,self.camera_zoom,self.camera_x,self.camera_y)
      self.ground_sprite_list.append(object)

  def on_draw(self):
    arcade.start_render()

    self.ground_sprite_list.draw()
    self.player_sprite_list.draw()
    if self.debug_mode == True:
      for i in self.player_sprite_list:
        i.draw_hit_box((100,100,100),3)

  def on_key_press(self, key, modifiers):
    if key == arcade.key.LEFT or key == arcade.key.A:
      self.key_pressed[1] = -6
    elif key == arcade.key.RIGHT or key == arcade.key.D:
      self.key_pressed[0] = 6
    elif key == arcade.key.UP or key == arcade.key.W:
      self.key_pressed[2] = 450
    elif key == arcade.key.NUM_1 or key == arcade.key.KEY_1:
      self.selected_player = 0
    elif key == arcade.key.NUM_2 or key == arcade.key.KEY_2:
      self.selected_player = 1
    elif key == arcade.key.NUM_3 or key == arcade.key.KEY_3:
      self.selected_player = 2

  def on_key_release(self, key, modifiers):
    if key == arcade.key.LEFT or key == arcade.key.A:
      self.key_pressed[1] = 0
    elif key == arcade.key.RIGHT or key == arcade.key.D:
      self.key_pressed[0] = 0
    elif key == arcade.key.UP or key == arcade.key.W:
      self.key_pressed[2] = 0

  def on_update(self, x):
    """ Move everything """

    self.frame_count += 1
    self.space.step(1 / 60.0)

    self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity += pymunk.Vec2d((sum(self.key_pressed[:2]), 0))
    if self.player_sprite_list[self.selected_player].can_jump == True:
      self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity += pymunk.Vec2d((0,self.key_pressed[2]))
      self.player_sprite_list[self.selected_player].can_jump = False
    if self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity.x > 125:
      self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity = pymunk.Vec2d((125, self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity.y))
    if self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity.x < -125:
      self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity = pymunk.Vec2d((-125, self.player_sprite_list[self.selected_player].pymunk_shape.body.velocity.y))

    x,y = [self.player_sprite_list[0].x for i in range(2)],[self.player_sprite_list[0].y for i in range(2)]
    for i in self.player_sprite_list[1:]:
      x[0] = i.x if i.x < x[0] else x[0]
      y[0] = i.y if i.y < y[0] else y[0]
      x[1] = i.x if i.x > x[1] else x[1]
      y[1] = i.y if i.y > y[1] else y[1]
    self.camera_x = sum(x)/2 + SCREEN_WIDTH / -2
    self.camera_y = sum(y)/2 + SCREEN_HEIGHT / -2

    if not self.game_over:
      for i in self.ground_sprite_list:
        i.update(self.camera_zoom,self.camera_x,self.camera_y)
      for i in self.player_sprite_list:
        i.update(self.camera_zoom,self.camera_x,self.camera_y)
        boxes = arcade.check_for_collision_with_list(i,self.ground_sprite_list)
        if_collide = [True for char in self.player_sprite_list if arcade.check_for_collision(i,char) == True and char != i]
        if (boxes != [] or True in if_collide) and abs(i.pymunk_shape.body.velocity.y) < 3:
          i.can_jump = True
      for i in self.player_sprite_list:
        i.center_x = i.pymunk_shape.body.position.x
        i.center_y = i.pymunk_shape.body.position.y
        i.angle = math.degrees(i.pymunk_shape.body.angle)
        # print(i.pymunk_shape.body.angle)
        # print(i.pymunk_shape.body.rotation_vector)
      # for x, i in enumerate(self.player_sprite_list):
      #   if x != self.selected_player:
      #     i.change_y = 0
      #     i.change_x = 0
      # for i in [self.player_sprite_list[self.selected_player]]:
      #   i.x += i.center_x - i.og_x
      #   i.y += i.center_y - i.og_y
      #   i.center_x,i.center_y = i.og_x,i.og_y

def main():
  """ Start the game """
  window = MyGame()
  window.start_new_game()
  arcade.run()


if __name__ == "__main__":
  main()
