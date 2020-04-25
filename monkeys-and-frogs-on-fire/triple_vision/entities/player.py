import random
import time
from enum import Enum

import arcade

from triple_vision import Settings as s
from triple_vision import Tile
from triple_vision.entities.entities import LivingEntity
from triple_vision.entities.sprites import ManaBar, MovingSprite
from triple_vision.entities.weapons import ChargedLaserProjectile, Melee
from triple_vision.pathfinding import PathFinder
from triple_vision.utils import pixels_to_tile, tile_to_pixels
from triple_vision.sound import SoundManager
from triple_vision.entities.abilities import Abilities


class States(Enum):
    IDLE = 0
    # MOVING = 1
    ATTACKING_RANGED = 2
    ATTACKING_MELEE = 3
    AIMING_BLOCKED = 4
    AIMING_NOT_BLOCKED = 5


class Player(LivingEntity, MovingSprite):
    MAX_HP = 1000
    DEFAULT_HP_REGENERATION_PER_S = 1

    def __init__(self, view: arcade.View, gender: str) -> None:
        super().__init__(
            sprite_name='wizzard',
            assets_path='assets/wizard',
            is_colored=True,
            has_hit_frame=True,
            gender=gender,
            scale=s.SCALING,
            hp=self.MAX_HP,
            ctx=view.game_manager,
            moving_speed=3,
            rotate=False
        )

        self.view = view
        self.last_shot = time.time()

        self.max_hp = self.MAX_HP
        self.state = States.IDLE

        self.is_alive = True
        self.attack_multiplier = 1
        self.dexterity = 0.75

        self._curr_color = self.curr_color

        self.path_finder = PathFinder()
        self.path = None

        self.mana_bar: ManaBar = None
        self.health_bar: PlayerLiveManager = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.colors = {
            "red": (255, 20, 20),
            "green": (0, 204, 0),
            "blue": (0, 128, 255),
        }

        self.selected_ability = None
        self.current_cool_down = 0.0
        self._ability_duration_left = 0.0

        self.regenerating_hp = False
        self.regeneration_hp_value = self.DEFAULT_HP_REGENERATION_PER_S
        self._regeneration_tick = 0.0
        self._regeneration_interval = 1  # in seconds

    @property
    def curr_color(self):
        return self._curr_color

    @curr_color.setter
    def curr_color(self, value):
        if value == 'red':
            self.resistance = 0.1
            self.attack_multiplier = 1.5
            self.speed_multiplier = 1.1
            self.dexterity = 0.6
            self.selected_ability = Abilities.red.value

        elif value == 'green':
            self.resistance = 0.5
            self.attack_multiplier = 1.1
            self.speed_multiplier = 1
            self.dexterity = 0.75
            self.selected_ability = Abilities.green.value

        elif value == 'blue':
            self.resistance = 0
            self.attack_multiplier = 1
            self.speed_multiplier = 1.5
            self.dexterity = 0.5
            self.selected_ability = Abilities.blue.value

        else:
            raise ValueError('Color can only be red, green, or blue.')

        self._curr_color = value

    def reset_stats(self):
        self.curr_color = self._curr_color

    def setup(self) -> None:
        self.set_hit_box([
            (-4.0, -1.0),
            (4.0, -1.0),
            (6.0, -3.0),
            (6.0, -11.0),
            (4.0, -13.0),
            (-4.0, -13.0),
            (-6.0, -11.0),
            (-6.0, -3.0)
        ])
        self.curr_color = 'red'
        self.selected_ability = Abilities.red.value

        self.mana_bar = ManaBar(
            self.view,
            fill_part_filename="assets/healthbar/mana_fill_part.png",
            fill_part_width=44.0,
            filename="assets/healthbar/mana_bar_border_white.png",
            center_x=420,
            center_y=18,
            scale=1,
            auto_filling_speed=2
        )
        self.health_bar = PlayerLiveManager(self.view, self.hp)

        while True:
            center = tile_to_pixels(random.randrange(0, s.MAP_SIZE[0]), random.randrange(0, s.MAP_SIZE[1]))

            if (
                    len(arcade.get_sprites_at_point(center, self.view.collision_list)) == 0 and
                    len(arcade.get_sprites_at_point(center, self.view.map.sprites)) > 0
            ):
                break

        self.center_x = center[0]
        self.center_y = center[1] + s.PLAYER_CENTER_Y_COMPENSATION

    def process_key_press(self, key) -> None:
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

    def process_key_release(self, key) -> None:
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

    def process_left_mouse_press(self, x, y, charge) -> None:
        if time.time() - self.last_shot < self.dexterity:
            SoundManager.add_sound("empty_gun.wav")
            SoundManager.play_sound("empty_gun.wav")
            return

        if len(self.mana_bar) == 0:
            # TODO empty mana sound
            return

        bullet = ChargedLaserProjectile(
            charge=charge,
            center_x=self.center_x,
            center_y=self.center_y,
            rotate=True,
        )
        bullet.color = self.curr_color_to_rgb()
        bullet.move_to(x, y, set_target=False)
        bullet.play_activate_sound()
        self.view.game_manager.player_projectiles.append(bullet)
        self.last_shot = time.time()
        self.mana_bar.remove_filling_part()
        self.state = States.ATTACKING_RANGED

    def process_right_mouse_press(self, x, y) -> None:
        if len(self.mana_bar) == self.mana_bar.max_fillers:
            self.mana_bar.clear()
            self.selected_ability.activate(x, y, self.view)
        else:
            # TODO empty mana sound
            pass

    def kill(self):
        self.is_alive = False
        super().kill()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        change_x = 0
        change_y = 0

        if self.up_pressed and not self.down_pressed:
            change_y = 1
        elif self.down_pressed and not self.up_pressed:
            change_y = -1

        if self.left_pressed and not self.right_pressed:
            change_x = -1
        elif self.right_pressed and not self.left_pressed:
            change_x = 1

        if self.regenerating_hp:
            self._regeneration_tick += delta_time
            if self._regeneration_tick >= self._regeneration_interval:
                self._regeneration_tick = 0.0

                if self.hp < self.max_hp:
                    self.hp += self.regeneration_hp_value
                else:
                    self.hp = self.MAX_HP

        dest = tile_to_pixels(
            *pixels_to_tile(
                self.center_x + change_x * Tile.SCALED,
                self.center_y + change_y * Tile.SCALED
            )
        )
        if not arcade.get_sprites_at_exact_point(dest, self.view.collision_list):
            self.move_to(dest[0], dest[1] + s.PLAYER_CENTER_Y_COMPENSATION)
            # self.state = States.MOVING
        if self.current_cool_down > 0:
            self.current_cool_down -= delta_time
            self._ability_duration_left -= delta_time

        if self._ability_duration_left < 0:
            self._ability_duration_left = 0
            self.selected_ability.deactivate(self.view)

        if self.current_cool_down < 0:
            self.current_cool_down = 0.0

        super().on_update(delta_time)

    def update_health_bars(self, delta_time):
        self.mana_bar.on_update(delta_time)
        self.health_bar.update()

    def curr_color_to_rgb(self):
        return self.colors[self.curr_color]

    def draw(self):
        super().draw()
        self.mana_bar.draw()
        self.health_bar.draw()


class PlayerLiveManager:
    def __init__(
        self,
        view,
        life_count: int = 10,
        is_filled: bool = True,
        scale: float = 1,
    ) -> None:

        self.view = view
        self.margin = 30
        self.hearts = arcade.SpriteList()
        self.heart_map = [2, 2, 2]
        self.half_heart_value = self.view.player.hp / sum(self.heart_map)
        self.scaling = scale
        self.prev_viewport = self.view.camera.viewport_left, self.view.camera.viewport_bottom
        self._previous_player_hp = None

        if not is_filled:
            return

        for i in range(3):
            self.hearts.append(
                arcade.Sprite(
                    "assets/hearts/heart_2.png",
                    center_x=(i + 1) * 60 + self.view.camera.viewport_left - 20,
                    center_y=30 + self.view.camera.viewport_bottom,
                    scale=self.scaling
                )
            )

    def update(self):
        if self._previous_player_hp is None:
            self._previous_player_hp = self.view.player.hp

        viewport = (self.view.camera.viewport_left, self.view.camera.viewport_bottom)

        if self.prev_viewport != viewport:
            for heart in self.hearts:
                heart.center_x += viewport[0] - self.prev_viewport[0]
                heart.center_y += viewport[1] - self.prev_viewport[1]

            self.prev_viewport = viewport

        if self._previous_player_hp == self.view.player.hp:
            return

        self._previous_player_hp = self.view.player.hp

        total_hearts = sum(self.heart_map)
        if total_hearts > 0:
            # +1 so we don't loose half hearth on first hit
            player_hearts = int(self.view.player.hp // self.half_heart_value + 1)
            self._update_heart_map(player_hearts)
            self._update_hearts_icons()

    def _update_heart_map(self, player_hearts: int):
        temp_hearth_map = [0, 0, 0]
        index = 0
        for hearth_i in range(player_hearts):
            if temp_hearth_map[index] == 2:
                index += 1
                if index == len(temp_hearth_map) - 1:
                    # HP is full
                    return

            temp_hearth_map[index] += 1

        self.heart_map = temp_hearth_map

    def _update_hearts_icons(self):
        for idx, heart_val in enumerate(self.heart_map):
            self.hearts.pop(idx)
            self.hearts.insert(idx, arcade.Sprite(
                f"assets/hearts/heart_{heart_val}.png",
                center_x=(idx + 1) * 60 + self.view.camera.viewport_left - 20,
                center_y=30 + self.view.camera.viewport_bottom,
                scale=self.scaling
            ))

    def draw(self):
        self.hearts.draw()
