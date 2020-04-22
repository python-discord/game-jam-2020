import arcade

key = {
    119: "W",
    97: "A",
    115: "S",
    100: "D",
    105: "I",
    106: "J",
    107: "K",
    108: "L",
    65361: "←",
    65362: "↑",
    65363: "→",
    65364: "↓",
}


class PlayerText:
    def __init__(self, player_sprite):

        self.player_sprite = player_sprite
        self.text = key[self.player_sprite.get_direction(key=True)]
        self.x_pos = self.player_sprite.center_x
        self.y_pos = self.player_sprite.center_y

    def draw(self):
        arcade.draw_text(self.text, self.x_pos, self.y_pos, arcade.color.BLACK, 100)

    def update(self):
        self.text = key[self.player_sprite.get_direction(key=True)]
        self.x_pos = self.player_sprite.center_x
        self.y_pos = self.player_sprite.center_y


class PlayerSprite(arcade.Sprite):
    def __init__(self, idle_dict, up_frames, down_frames, left_frames, right_frames, x, y, default_direction, up_key,
                 down_key, left_key, right_key):
        super().__init__()
        self.player_speed = 10

        self.current_texture_counter = 0
        self.idle_dict = idle_dict
        self.up_frames = up_frames
        self.down_frames = down_frames
        self.left_frames = left_frames
        self.right_frames = right_frames
        self.center_x = x
        self.center_y = y
        self.scale = 0.4
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key

        test = True
        self.texture = idle_dict[default_direction]
        if test:
            self.set_hit_box([(0, -0), (0, -0)])
        else:
            self.set_hit_box([(40, -20), (40, -100), (-40, -100), (-40, -20)])

        if default_direction == "up":
            self.change_y = self.player_speed
        elif default_direction == "down":
            self.change_y = -self.player_speed
        elif default_direction == "left":
            self.change_x = -self.player_speed
        elif default_direction == "right":
            self.change_x = self.player_speed

    def on_key_press_control(self, key, modifiers):
        if key == self.up_key:
            self.change_x = 0
            self.change_y = self.player_speed
        elif key == self.down_key:
            self.change_x = 0
            self.change_y = -self.player_speed
        elif key == self.left_key:
            self.change_y = 0
            self.change_x = -self.player_speed
        elif key == self.right_key:
            self.change_y = 0
            self.change_x = self.player_speed

    def get_direction(self, key=False):
        if self.change_x != 0:
            if self.change_x > 0:
                return self.right_key if key else "right"
            else:
                return self.left_key if key else "left"

        if self.change_y != 0:
            if self.change_y > 0:
                return self.up_key if key else "up"
            else:
                return self.down_key if key else "down"

    def update_animation(self, delta_time: float = 1 / 60):
        if self.get_direction() == "up":
            self.texture = self.up_frames[int(self.current_texture_counter / (10 / self.player_speed)) % len(self.up_frames)]
        elif self.get_direction() == "down":
            self.texture = self.down_frames[
                int(self.current_texture_counter / (10 / self.player_speed)) % len(self.down_frames)]
        elif self.get_direction() == "left":
            self.texture = self.left_frames[
                int(self.current_texture_counter / (10 / self.player_speed)) % len(self.left_frames)]
        elif self.get_direction() == "right":
            self.texture = self.right_frames[
                int(self.current_texture_counter / (10 / self.player_speed)) % len(self.right_frames)]

        self.current_texture_counter += 1

    def increase_speed(self, increase):
        self.player_speed += increase

        if self.get_direction() == 'up':
            self.change_x = 0
            self.change_y = self.player_speed
        elif self.get_direction() == 'down':
            self.change_x = 0
            self.change_y = -self.player_speed
        elif self.get_direction() == 'left':
            self.change_y = 0
            self.change_x = -self.player_speed
        elif self.get_direction() == 'right':
            self.change_y = 0
            self.change_x = self.player_speed

    def create_game_sprite_events(self):
        pass