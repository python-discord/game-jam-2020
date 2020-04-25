import arcade

from triple_vision import Settings as s
from triple_vision import Tile
from triple_vision.camera import Camera
from triple_vision.engine import SlowModeSupportEngine
from triple_vision.entities import (
    ChasingEnemy,
    Enemies,
    Player,
    StationaryEnemy
)
from triple_vision.managers import CardManager, GameManager, CursorManager
from triple_vision.sound import SoundManager
from triple_vision.map import Map


class TripleVision(arcade.View):
    def __init__(self) -> None:
        super().__init__()

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

        self.physics_engine = None

        arcade.set_background_color(arcade.color.BLACK)

    def on_show(self) -> None:
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

        for _ in range(10):
            self.game_manager.create_enemy(
                ChasingEnemy,
                Enemies.big_demon,
                self.player,
                Tile.SCALED * 10,
                moving_speed=1
            )

        for _ in range(5):
            self.game_manager.create_enemy(
                StationaryEnemy,
                Enemies.imp,
                self.player,
                Tile.SCALED * 10,
                0.75
            )

        self.physics_engine = SlowModeSupportEngine(self.player, self.collision_list)

    def on_key_press(self, key, modifiers) -> None:
        self.player.process_key_press(key)

    def on_key_release(self, key, modifiers) -> None:
        self.player.process_key_release(key)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.card_manager.check_mouse_motion(
            x + self.camera.viewport_left,
            y + self.camera.viewport_bottom
        )
        self.cursor_manager.process_mouse_motion(x, y)

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
        self.physics_engine.update()
        self.map.on_update(delta_time)
        self.camera.update()
        self.card_manager.update()

        if self.time_slow_ability:
            self.player.update_health_bar(delta_time * s.ON_CARD_HOVER_SLOWDOWN_MULTIPLIER)
        else:
            self.player.update_health_bar(delta_time)

        SoundManager.update(self.slow_down or self.time_slow_ability)
        self.cursor_manager.update()
