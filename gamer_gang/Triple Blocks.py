import random
import math
import arcade
import os

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
  def __init__(self, textures, scale, x, y):
    super().__init__()

    self.textures = textures
    self.texture = self.textures[0]

    self.scaling = scale

    self.x = x
    self.y = y

  def update(self,zoom,cx,cy):
    """ Move the sprite """
    super().update()

    self.scale = zoom * self.scaling

    self.center_x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
    self.center_y = (self.y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2

class PlayerSprite(arcade.Sprite):
  def __init__(self, textures, scale, x, y, zoom, cx, cy):
    super().__init__()

    self.textures = textures
    self.texture = self.textures[0]

    self.scaling = scale

    self.x = x
    self.y = y

    self.acc_x = 0
    self.acc_y = 0

    self.center_x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2
    self.center_y = (self.y - cy - SCREEN_HEIGHT / 2) * zoom + SCREEN_HEIGHT / 2
    self.og_x = self.center_x
    self.og_y = self.center_y

  def update(self,zoom,cx,cy):
    self.scale = zoom * self.scaling
    self.og_x = self.center_x
    self.og_y = self.center_y
    #self.center_x = (self.x - cx - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2


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

    self.camera_zoom = 1
    self.camera_x = SCREEN_WIDTH / -2
    self.camera_y = SCREEN_HEIGHT / -2

    self.gravity = 0.5

    self.key_pressed = [0,0,0] #controllable

    self.ground_sprite_list = arcade.SpriteList()
    self.player_sprite_list = arcade.SpriteList()

    self.selected_player = 0

    self.ground_texture_list = [arcade.load_texture("Discord Arcade Game Jam 2020/images/Ground/Debug.png")]
    self.player_texture_list = [arcade.load_texture("Discord Arcade Game Jam 2020/images/Player/Debug.png")]

    for i in range(1,2):
      object = PlayerSprite(self.player_texture_list,1,i*32,32*1,self.camera_zoom,self.camera_x,self.camera_y)
      self.player_sprite_list.append(object)

    # a = arcade.SpriteList()
    # b = arcade.SpriteList()
    # c = arcade.SpriteList()
    # a.append(self.player_sprite_list[1])
    # a.append(self.player_sprite_list[2])
    # b.append(self.player_sprite_list[0])
    # b.append(self.player_sprite_list[2])
    # c.append(self.player_sprite_list[0])
    # c.append(self.player_sprite_list[1])

    for i in range(1,10):
      object = GroundSprite(self.ground_texture_list,1,i*32,0)
      self.ground_sprite_list.append(object)
      # a.append(object)
      # b.append(object)
      # c.append(object)

    self.physics_engines = []
    self.physics_engines.append(arcade.PhysicsEnginePlatformer(self.player_sprite_list[0], self.ground_sprite_list, gravity_constant=self.gravity))
    # self.physics_engines.append(arcade.PhysicsEnginePlatformer(self.player_sprite_list[1], self.ground_sprite_list, gravity_constant=self.gravity))
    # self.physics_engines.append(arcade.PhysicsEnginePlatformer(self.player_sprite_list[2], self.ground_sprite_list, gravity_constant=self.gravity))
    # self.physics_engines.append(arcade.PhysicsEnginePlatformer(self.player_sprite_list[0], a, gravity_constant=self.gravity))
    # self.physics_engines.append(arcade.PhysicsEnginePlatformer(self.player_sprite_list[1], b, gravity_constant=self.gravity))
    # self.physics_engines.append(arcade.PhysicsEnginePlatformer(self.player_sprite_list[2], c, gravity_constant=self.gravity))
    # self.physics_engines.append(arcade.PhysicsEngineSimple(self.player_sprite_list[0], a))
    # self.physics_engines.append(arcade.PhysicsEngineSimple(self.player_sprite_list[1], b))
    # self.physics_engines.append(arcade.PhysicsEngineSimple(self.player_sprite_list[2], c))



  def on_draw(self):
    """
    Render the screen.
    """
    arcade.start_render()

    self.ground_sprite_list.draw()
    self.player_sprite_list.draw()

  def on_key_press(self, key, modifiers):
    if key == arcade.key.LEFT or key == arcade.key.A:
      self.key_pressed[1] = -0.3
    elif key == arcade.key.RIGHT or key == arcade.key.D:
      self.key_pressed[0] = 0.3
    elif key == arcade.key.UP or key == arcade.key.W:
      self.key_pressed[2] = 8
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

    self.player_sprite_list[self.selected_player].acc_x = self.key_pressed[0] + self.key_pressed[1]
    self.player_sprite_list[self.selected_player].change_x += self.player_sprite_list[self.selected_player].acc_x if abs(self.player_sprite_list[self.selected_player].change_x) < 3.5 else 0
    self.player_sprite_list[self.selected_player].change_y = self.key_pressed[2] if self.physics_engines[self.selected_player].can_jump() else self.player_sprite_list[self.selected_player].change_y

    if self.key_pressed[0] + self.key_pressed[1] == 0:
      if abs(self.player_sprite_list[self.selected_player].change_x) < 0.4:
        self.player_sprite_list[self.selected_player].change_x = 0
      else:
        self.player_sprite_list[self.selected_player].change_x += 0.3 if self.player_sprite_list[self.selected_player].change_x < 0 else -0.3

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
      for i in self.physics_engines:
        i.update()
      for i in [self.player_sprite_list[self.selected_player]]:
        i.x += i.center_x - i.og_x
        i.y += i.center_y - i.og_y
        i.center_x,i.center_y = i.og_x,i.og_y

def main():
  """ Start the game """
  window = MyGame()
  window.start_new_game()
  arcade.run()


if __name__ == "__main__":
  main()
