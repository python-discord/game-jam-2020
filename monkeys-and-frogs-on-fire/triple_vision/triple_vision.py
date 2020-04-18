import random
import time

import arcade

from triple_vision.constants import (
    SCALED_TILE,
    SCALING,
    WINDOW_SIZE,
)
from triple_vision.entities import (
    ChasingEnemy,
    Enemies,
    Player,
    LaserProjectile,
    StationaryEnemy
)
from triple_vision.managers import CardManager, GameManager


class TripleVision(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.paused = False

        self.tiles = None

        self.player = None

        self.card_manager = None
        self.game_manager = None

        self.physics_engine = None

    def setup(self) -> None:
        self.tiles = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        for y in range(0, WINDOW_SIZE[1], SCALED_TILE):
            for x in range(0, WINDOW_SIZE[0], SCALED_TILE):
                self.tiles.append(
                    arcade.Sprite(
                        filename=f'assets/dungeon/frames/floor_{random.randint(1, 8)}.png',
                        scale=SCALING,
                        center_x=x + SCALED_TILE / 2,
                        center_y=y + SCALED_TILE / 2
                    )
                )

        self.player = Player('m')
        self.card_manager = CardManager(self)
        self.game_manager = GameManager(self)

        self.game_manager.create_enemy(
            ChasingEnemy,
            Enemies.big_demon,
            self.player,
            SCALED_TILE * 10,
            center_x=50,
            center_y=500,
            moving_speed=2
        )
        self.game_manager.create_enemy(
            StationaryEnemy,
            Enemies.imp,
            self.player,
            SCALED_TILE * 10,
            center_x=50,
            center_y=500
        )

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.card_manager.check_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if not self.card_manager.check_mouse_press(x, y, button):
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.player.move_to(x, y, rotate=False)

            elif button == arcade.MOUSE_BUTTON_RIGHT:
                if time.time() - self.player.last_shot < 0.75:  # TODO hardcoded
                    # TODO Play empty gun sound or something similar
                    return

                bullet = LaserProjectile(
                    center_x=self.player.center_x,
                    center_y=self.player.center_y
                )
                bullet.move_to(x, y, rotate=True, set_target=False)
                self.game_manager.player_projectiles.append(bullet)
                self.player.last_shot = time.time()

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
        self.tiles.draw()
        self.player.draw()

        self.game_manager.draw()
        self.card_manager.draw()

    def on_update(self, delta_time: float) -> None:
        if not self.paused:
            self.player.update(delta_time)
            self.game_manager.update(delta_time)

        self.card_manager.update()
