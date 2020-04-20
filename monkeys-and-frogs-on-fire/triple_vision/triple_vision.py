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
from triple_vision.managers import CardManager, GameManager
from triple_vision.map import Map


class TripleVision(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.paused = False

        self.map = None

        self.collision_list = None
        self.bullet_list = None

        self.player = None
        self.camera = None

        self.card_manager = None
        self.game_manager = None

        self.physics_engine = None

    def setup(self) -> None:
        self.collision_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.map = Map(self, s.MAP_SIZE)
        self.map.setup()

        self.player = Player(self, 'm')
        self.player.setup()

        self.camera = Camera(self, s.WINDOW_SIZE[0] / 2.5, s.WINDOW_SIZE[1] / 2.5)

        self.card_manager = CardManager(self)
        self.game_manager = GameManager(self)

        for y in range(1, 3):
            self.game_manager.create_enemy(
                ChasingEnemy,
                Enemies.big_demon,
                self.player,
                Tile.SCALED * 10,
                center_x=50,
                center_y=y * 250,
                moving_speed=1
            )

        for y in range(1, 4):
            self.game_manager.create_enemy(
                StationaryEnemy,
                Enemies.imp,
                self.player,
                Tile.SCALED * 10,
                center_x=50,
                center_y=y * 200
            )

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.collision_list)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.card_manager.check_mouse_motion(
            x + self.camera.viewport_left,
            y + self.camera.viewport_bottom
        )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if not self.player.is_alive:
            return

        x += self.camera.viewport_left
        y += self.camera.viewport_bottom

        if not self.card_manager.process_mouse_press(x, y, button):
            self.player.process_mouse_press(x, y, button)

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

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.KEY_1:
            self.player.cur_color = 'red'
        elif key == arcade.key.KEY_2:
            self.player.cur_color = 'green'
        elif key == arcade.key.KEY_3:
            self.player.cur_color = 'blue'

    def on_draw(self) -> None:
        arcade.start_render()

        self.map.draw()
        self.game_manager.draw()

        if self.player.is_alive:
            self.player.draw()

        self.card_manager.draw()

    def on_update(self, delta_time: float = 1/60) -> None:
        if not self.paused:
            if self.player.is_alive:
                self.player.update(delta_time)

            self.game_manager.update(delta_time)
            self.physics_engine.update()
            self.map.update()
            self.camera.update()

        self.card_manager.update()