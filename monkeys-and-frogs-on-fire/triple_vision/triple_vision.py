import time
import random

import arcade

from triple_vision import Settings as s
from triple_vision import Tile
from triple_vision.camera import Camera
from triple_vision.entities import (
    ChasingEnemy,
    Enemies,
    Player,
    StationaryEnemy
)
from triple_vision.managers import CardManager, GameManager, CursorManager
from triple_vision.map import Map
from triple_vision.sound import SoundManager


class TripleVision(arcade.View):
    def __init__(self, main_view) -> None:
        super().__init__()
        self.level = 1
        self.seed = None

        self.main_view = main_view

        self.slow_down = False
        self.time_slow_ability = False

        self.map = None

        self.collision_list = None
        self.bullet_list = None

        self.player = None
        self.charge = None
        self.charging = None

        self.camera = None

        self.card_manager = None
        self.game_manager = None
        self.cursor_manager: CursorManager = None

        arcade.set_background_color(arcade.color.BLACK)

    def on_show(self) -> None:
        self.crete_level()

    def crete_level(self, *, seed=None):
        if seed is None:
            self.seed = time.time()
            random.seed(self.seed)
        else:
            self.seed = seed
            random.seed(seed)

        self.bullet_list = arcade.SpriteList()

        self.player = Player(self, 'm')
        self.camera = Camera(self, s.WINDOW_SIZE[0] / 2.5, s.WINDOW_SIZE[1] / 2.5)

        self.card_manager = CardManager(self)
        self.game_manager = GameManager(self)
        self.cursor_manager = CursorManager(self, self.player)

        self.map = Map(self, s.MAP_SIZE)
        self.map.setup()

        self.player.setup()
        self.charge = 0.0
        self.charging = False

        # Deals with how many enemies and what types spawn
        # No time for additional manager an code is a bit tangled.

        low_speed = 0.75
        normal_speed = 1.0
        fast_speed = 1.5
        very_fast_speed = 2.0

        # For melee
        low_damage = random.randrange(15, 30)
        normal_damage = random.randrange(30, 60)
        high_damage = random.randrange(60, 120)

        normal_detection_radius = Tile.SCALED * 15
        big_detection_radius = Tile.SCALED * 20
        huge_detection_radius = Tile.SCALED * 25

        fast_shoot_interval = 0.75
        medium_shoot_interval = 1.25
        slow_shoot_interval = 2.0

        low_projectile_dmg = random.randrange(20, 40)
        medium_projectile_dmg = random.randrange(40, 60)
        high_projectile_damage = random.randrange(60, 90)

        # Goblins have low hp but are fast and big in numbers.
        # Very small dmg
        # level1 3
        # level2 5
        # level3 7
        # level4 9
        # etc
        for _ in range(self.level * 3 - (self.level-1)*1):
            self.game_manager.create_enemy(
                ChasingEnemy,
                Enemies.goblin,
                self.player,
                normal_detection_radius,
                moving_speed=very_fast_speed
            )

        # Chorts are similar to goblins
        # level1 3
        # level2 5
        # level3 7
        # level4 9
        # etc
        for _ in range(self.level * 3 - (self.level - 1) * 1):
            self.game_manager.create_enemy(
                ChasingEnemy,
                Enemies.chort,
                self.player,
                normal_detection_radius,
                moving_speed=very_fast_speed
            )

        # Tiny zombies are similar to goblins
        # level1 3
        # level2 5
        # level3 7
        # level4 9
        # etc
        for _ in range(self.level * 3 - (self.level - 1) * 1):
            self.game_manager.create_enemy(
                ChasingEnemy,
                Enemies.tiny_zombie,
                self.player,
                normal_detection_radius,
                moving_speed=very_fast_speed
            )

        # Ice zombies demons are fast and not insta killable
        # level1 2
        # level2 4
        # level3 6
        # level4 8
        # etc
        for _ in range(self.level * 2):
            self.game_manager.create_enemy(
                ChasingEnemy,
                Enemies.ice_zombie,
                self.player,
                big_detection_radius,
                moving_speed=fast_speed
            )

        # Big demons are tough foes, normal speed but lot HP.
        # Huge dmg and big detection radius
        # level1 3
        # level2 6
        # level3 9
        # level4 12
        # etc
        for _ in range(self.level * 3):
            self.game_manager.create_enemy(
                ChasingEnemy,
                Enemies.big_demon,
                self.player,
                big_detection_radius,
                moving_speed=1
            )

        # Imps are shooting
        # level1 2
        # level2 4
        # level3 6
        # level4 8
        for _ in range(self.level * 2):
            self.game_manager.create_enemy(
                StationaryEnemy,
                Enemies.imp,
                self.player,
                normal_detection_radius,
                shoot_interval=fast_shoot_interval,
                dmg=low_projectile_dmg
            )

        # Necromancers are shooting
        # level1 0
        # level2 0
        # level3 1
        # level4 2
        for _ in range(self.level - 2):
            self.game_manager.create_enemy(
                StationaryEnemy,
                Enemies.necromancer,
                self.player,
                big_detection_radius,
                shoot_interval=slow_shoot_interval,
                dmg=high_projectile_damage
            )

        # Muddy is slow mowing tank
        # level1 0
        # level2 1
        # level3 2
        # level4 3
        for _ in range(self.level - 1):
            self.game_manager.create_enemy(
                ChasingEnemy,
                Enemies.muddy,
                self.player,
                huge_detection_radius,
                moving_speed=low_speed
            )



    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            arcade.set_viewport(0, s.WINDOW_SIZE[0], 0, s.WINDOW_SIZE[1])
            self.window.set_mouse_visible(True)
            self.window.show_view(self.main_view)
        elif key == arcade.key.R:
            self.crete_level(seed=self.seed)
        else:
            self.player.process_key_press(key)

    def on_key_release(self, key, modifiers) -> None:
        self.player.process_key_release(key)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.card_manager.check_mouse_motion(
            x + self.camera.viewport_left,
            y + self.camera.viewport_bottom
        )
        self.cursor_manager.set_cursor_position(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if not self.player.is_alive:
            return

        x += self.camera.viewport_left
        y += self.camera.viewport_bottom

        if not self.card_manager.process_mouse_press(x, y, button):
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.charging = True
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                self.player.process_right_mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if not self.player.is_alive:
            return

        x += self.camera.viewport_left
        y += self.camera.viewport_bottom

        if button == arcade.MOUSE_BUTTON_LEFT and self.charging:
            self.player.process_left_mouse_press(x, y, self.charge)
            self.charging = False
            self.charge = 0

    # def on_key_press(self, key, modifiers):
    #     """Called whenever a key is pressed. """
    #
    #     vec = [0, 0]
    #     if time.time() - self.last_key_data[1] < PRESSING_DELAY:
    #         last_key = self.last_key_data[0]
    #         if sorted((key, last_key)) == [arcade.key.LEFT, arcade.key.UP]:
    #             vec = [-1, 1]
    #         if sorted((key, last_key)) == [arcade.key.UP, arcade.key.RIGHT]:
    #             vec = [1, 1]
    #         if sorted((key, last_key)) == [arcade.key.LEFT, arcade.key.DOWN]:
    #             vec = [-1, -1]
    #         if sorted((key, last_key)) == [arcade.key.RIGHT, arcade.key.DOWN]:
    #             vec = [1, -1]
    #     elif key == arcade.key.UP:
    #         vec[1] = 1
    #     elif key == arcade.key.DOWN:
    #         vec[1] = -1
    #     elif key == arcade.key.LEFT:
    #         vec[0] = -1
    #     elif key == arcade.key.RIGHT:
    #         vec[0] = 1
    #
    #     print(f"Vec: {vec}")
    #
    #     self.last_key_data = [key, time.time()]
    #
    #     bullet = Bullet(
    #         BULLET_LIFETIME,
    #         BULLET_SPEED,
    #         ":resources:images/space_shooter/laserBlue01.png",
    #         center_x=self.player.center_x, center_y=self.player.center_y
    #     )
    #     bullet.move_to_angle(math.atan2(vec[1], vec[0]))
    #     self.bullet_list.append(bullet)

    def on_draw(self) -> None:
        arcade.start_render()

        self.map.draw()
        self.game_manager.draw()

        if self.player.is_alive:
            self.player.draw()

        self.card_manager.draw()
        self.cursor_manager.draw()

    def on_update(self, delta_time: float) -> None:
        if self.slow_down or self.time_slow_ability:
            delta_time = delta_time / s.ON_CARD_HOVER_SLOWDOWN_MULTIPLIER

        if self.charging and self.charge < 100:
            if self.time_slow_ability:
                self.charge += delta_time * 60 * s.ON_CARD_HOVER_SLOWDOWN_MULTIPLIER
            else:
                self.charge += delta_time*60

        if self.player.is_alive:
            if self.time_slow_ability:
                self.player.on_update(delta_time * s.ON_CARD_HOVER_SLOWDOWN_MULTIPLIER)
            else:
                self.player.on_update(delta_time)

        self.game_manager.on_update(delta_time)
        self.map.on_update(delta_time)
        self.camera.update()
        self.card_manager.update()

        if self.time_slow_ability:
            self.player.update_health_bars(delta_time * s.ON_CARD_HOVER_SLOWDOWN_MULTIPLIER)
        else:
            self.player.update_health_bars(delta_time)

        SoundManager.update(self.slow_down or self.time_slow_ability)
        self.cursor_manager.update()
        self.player.update_health_bars(delta_time)
