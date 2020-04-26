import random
from typing import Optional, Tuple

import arcade

from triple_vision import Settings as s
from triple_vision import Tile
from triple_vision.entities import (
    ChasingEnemy,
    Enemies,
    StationaryEnemy
)
from triple_vision.entities import TextIndicator, States
from triple_vision.entities.sprites import Potion, PotionEffect
from triple_vision.networking import client
from triple_vision.entities import Melee
from triple_vision.sound import SoundManager


class GameManager:

    def __init__(self, view) -> None:
        self.view = view

        self.enemies = arcade.SpriteList(use_spatial_hash=True)
        self.player_projectiles = arcade.SpriteList(use_spatial_hash=True)
        self.player_melee_attacks = arcade.SpriteList(use_spatial_hash=True)
        self.effects = arcade.SpriteList()
        self.enemy_projectiles = arcade.SpriteList(use_spatial_hash=True)
        self.damage_indicators = arcade.SpriteList()
        self.potions = arcade.SpriteList()
        self.hidden_active_potions: list = []

        self.spikes: Optional[arcade.SpriteList] = None

        self.points = 0
        self.prev_sent = False

    def draw(self) -> None:
        self.player_melee_attacks.draw()
        self.effects.draw()
        self.enemies.draw()
        self.player_projectiles.draw()
        self.enemy_projectiles.draw()
        self.damage_indicators.draw()
        self.potions.draw()

    def create_potion(self, effect: PotionEffect, *args, **kwargs):
        potion = Potion(self, self.view.player, effect, *args, scale=2, **kwargs)
        potion.setup()
        self.potions.append(potion)

    def create_enemy(self, enemy_class, *args, **kwargs) -> None:
        enemy = enemy_class(ctx=self, *args, **kwargs)
        enemy.setup()
        self.enemies.append(enemy)

    def create_dmg_indicator(self, dmg: float, position: Tuple[float, float]) -> None:
        dmg_indicator = TextIndicator(str(int(dmg)), *position)
        self.damage_indicators.append(dmg_indicator)

    def create_text_indicator(self, text: str, position: Tuple[float, float]) -> None:
        indicator = TextIndicator(text, *position)
        self.damage_indicators.append(indicator)

    def on_update(self, delta_time) -> None:
        for enemy in self.enemies:

            projectile_hit_enemy = arcade.check_for_collision_with_list(
                enemy,
                self.player_projectiles
            )

            for projectile in projectile_hit_enemy:
                self.create_dmg_indicator(
                    projectile.dmg * self.view.player.attack_multiplier,
                    enemy.position
                )
                enemy.hit(projectile, self.view.player.attack_multiplier)
                projectile.destroy()

            melee_attacks_hit_enemy = arcade.check_for_collision_with_list(
                enemy,
                self.player_melee_attacks
            )

            for player_melee_attack in melee_attacks_hit_enemy:
                self.create_dmg_indicator(
                    player_melee_attack.dmg * self.view.player.attack_multiplier,
                    enemy.position
                )
                enemy.hit(player_melee_attack, self.view.player.attack_multiplier)

        projectiles_hit_player = arcade.check_for_collision_with_list(
            self.view.player,
            self.enemy_projectiles
        )

        for projectile in projectiles_hit_player:
            self.view.player.hit(projectile)
            projectile.destroy()

        spikes_hit = arcade.check_for_collision_with_list(self.view.player, self.spikes)
        for spike in spikes_hit:
            if 0 < spike.ticks < 7:
                if spike.can_deal_dmg:
                    self.view.player.hit(spike)
                    spike.can_deal_dmg = False

        enemy_collision_with_player = arcade.check_for_collision_with_list(
            self.view.player,
            self.enemies
        )

        for enemy in enemy_collision_with_player:
            if enemy.can_melee_attack:
                self.view.player.hit(enemy.melee_weapon)
                enemy.can_melee_attack = False

        self.enemies.on_update(delta_time)

        if self.view.time_slow_ability:
            self.player_projectiles.on_update(delta_time * s.ON_CARD_HOVER_SLOWDOWN_MULTIPLIER)
            self.player_melee_attacks.on_update(delta_time * s.ON_CARD_HOVER_SLOWDOWN_MULTIPLIER)
        else:
            self.player_projectiles.on_update(delta_time)
            self.player_melee_attacks.on_update(delta_time)

        self.enemy_projectiles.on_update(delta_time)
        self.damage_indicators.on_update(delta_time)

        if not self.view.player.is_alive and not self.prev_sent:
            client.new_score(self.points)
            self.prev_sent = True

        hit_list = arcade.check_for_collision_with_list(self.view.player, self.potions)
        for potion in hit_list:
            potion.collected()
            potion.kill()
            self.hidden_active_potions.append(potion)

        for potion in self.hidden_active_potions:
            potion.on_update(delta_time)

        if len(self.enemies) == 0:
            self.view.level += 1
            self.view.soundtrack_manager.play_external_sound("assets/audio/sounds/win.wav")
            self.view.soundtrack_manager.play_song()  # plays the next soundtrack
            self.view.create_level()
        elif not self.view.player.is_alive:
            self.view.level += 0
            self.view.soundtrack_manager.play_external_sound("assets/audio/sounds/death.wav")
            self.view.soundtrack_manager.play_song()  # plays the next soundtrack
            self.view.create_level()

    def enemy_killed(self, enemy) -> None:
        self.points += enemy.kill_value


class CardManager:

    def __init__(self, view) -> None:
        self.view = view

        self.cards = arcade.SpriteList()
        self.colors = ('red', 'green', 'blue')
        self.card_manager_enabled = True

        card_scale = s.SCALING / 5.75

        self.MIN_CARD_HEIGHT = -242 * card_scale
        self.MAX_CARD_HEIGHT = 108 * card_scale
        self.MAX_CARD_HOVER_HEIGHT = 280 * card_scale
        self.DISABLED_COLOR = (255, 0, 0)
        self.ENABLED_COLOR = (255, 255, 255)

        for idx, color in enumerate(self.colors):
            self.cards.append(
                arcade.Sprite(
                    filename=f'assets/wizard/{color}_card.png',
                    scale=card_scale,
                    center_x=20 + s.WINDOW_SIZE[0] / 1.35 + (idx - 1) * 400 * card_scale,
                    center_y=self.MIN_CARD_HEIGHT
                )
            )

        self.show_cards = False
        self.hover_card = None
        self.prev_hover_card = None

        self.prev_viewport = self.view.camera.viewport_left, self.view.camera.viewport_bottom

    def set_hover_card(self, card):
        if card != self.hover_card:
            self.prev_hover_card = self.hover_card
            self.hover_card = card

    def check_mouse_motion(self, x, y) -> None:
        if not self.card_manager_enabled:
            return

        if (
            self.cards[0].left < x < self.cards[-1].right and
            self.cards[0].bottom < y < self.cards[-1].top
        ):
            for card in self.cards:
                if (
                    card.left < x < card.right and
                    card.bottom < y < card.top
                ):
                    self.set_hover_card(card)
                    break

            self.show_cards = True
            self.view.slow_down = True

        else:
            self.show_cards = False
            self.view.slow_down = False

    def process_mouse_press(self, x, y, button) -> bool:
        mouse_over_cards = (
            self.cards[0].left < x < self.cards[-1].right and
            self.cards[0].bottom < y < self.cards[-1].top
        )

        if button == arcade.MOUSE_BUTTON_LEFT:
            if mouse_over_cards:

                for idx, card in enumerate(self.cards):
                    if (
                        card.left < x < card.right and
                        card.bottom < y < card.top
                    ):
                        if self.card_manager_enabled:
                            # Only allow player to change players if it's enabled
                            self.view.player.curr_color = self.colors[idx]

                        self.show_cards = False
                        self.view.slow_down = False

                return True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            # Ignore ability activation if we click on card
            if mouse_over_cards:
                return True

        return False

    def draw(self) -> None:
        self.cards.draw()

    def _update_colors(self):
        for card in self.cards:
            if self.card_manager_enabled:
                if card.color == self.DISABLED_COLOR:  # don't change color if not necessary
                    card.color = self.ENABLED_COLOR
            else:
                if card.color == self.ENABLED_COLOR:  # don't change color if not necessary
                    card.color = self.DISABLED_COLOR

    def update(self, delta_time: float = 1/60):
        viewport = (self.view.camera.viewport_left, self.view.camera.viewport_bottom)

        if self.prev_viewport != viewport:
            for card in self.cards:
                card.center_x += viewport[0] - self.prev_viewport[0]
                card.center_y += viewport[1] - self.prev_viewport[1]

            self.prev_viewport = viewport

        max_hover_height = self.MAX_CARD_HOVER_HEIGHT + viewport[1]
        max_height = self.MAX_CARD_HEIGHT + viewport[1]
        min_height = self.MIN_CARD_HEIGHT + viewport[1]

        for card in self.cards:
            max_card_height = max_hover_height if card == self.hover_card else max_height

            if (
                self.show_cards and
                card == self.prev_hover_card and
                card.center_y >= max_height
            ):
                card.change_y = -10

            elif (
                (self.show_cards and card.center_y >= max_card_height) or
                (not self.show_cards and card.center_y <= min_height)
            ):
                card.change_y = 0

            elif card == self.prev_hover_card:
                self.prev_hover_card = None

            elif self.show_cards:
                card.change_y = 10

            else:
                card.change_y = -10

        self._update_colors()
        self.cards.update()


class CursorManager:
    def __init__(self, view: arcade.View, player):
        self.view = view
        self.window = view.window
        self.player = player

        self.cursors = {
            "moving": arcade.Sprite("assets/crosshairs/moving.png"),
            "ranged": arcade.Sprite("assets/crosshairs/ranged.png"),
        }
        self._curr_cursor: arcade.Sprite = self.cursors["ranged"]
        self.window.set_mouse_visible(False)

        self.prev_viewport = self.view.camera.viewport_left, self.view.camera.viewport_bottom

    def set_curr_cursor(self, value):
        last_position = self._curr_cursor.center_x, self._curr_cursor.center_y
        self._curr_cursor = self.cursors.get(value, None)
        self._curr_cursor.center_x, self._curr_cursor.center_y = last_position[0],  last_position[1]

    def get_curr_cursor(self):
        return self._curr_cursor

    curr_cursor = property(get_curr_cursor, set_curr_cursor)

    def set_cursor_position(self, x, y):
        self._curr_cursor.center_x = x + self.view.camera.viewport_left
        self._curr_cursor.center_y = y + self.view.camera.viewport_bottom

    def update(self):
        if self.player.is_moving():
            self.curr_cursor = "moving"
            self._curr_cursor.angle += 1
        elif self.player.state in (States.ATTACKING_RANGED, States.IDLE):
            self.curr_cursor = "ranged"

        viewport = (self.view.camera.viewport_left, self.view.camera.viewport_bottom)
        if self.prev_viewport != viewport:
            self._curr_cursor.center_x += viewport[0] - self.prev_viewport[0]
            self._curr_cursor.center_y += viewport[1] - self.prev_viewport[1]
            self.prev_viewport = viewport

        self._curr_cursor.color = self.player.colors[self.player.curr_color]

    def draw(self):
        if self._curr_cursor is not None:
            self._curr_cursor.draw()


class LevelManager:
    LOW_SPEED = 0.75
    NORMAL_SPEED = 1.0
    FAST_SPEED = 1.5
    VERY_FAST_SPEED = 2.0

    LOW_MELEE_DMG = random.randrange(15, 30)
    NORMAL_MELEE_DMG = random.randrange(30, 60)
    HIGH_MELEE_DMG = random.randrange(60, 120)

    NORMAL_CHASING_DETECTION_RADIUS = Tile.SCALED * 10
    BIG_CHASING_DETECTION_RADIUS = Tile.SCALED * 12
    HUGE_CHASING_DETECTION_RADIUS = Tile.SCALED * 14

    FAST_SHOOT_INTERVAL = 0.75
    MEDIUM_SHOOT_INTERVAL = 1.25
    SLOW_SHOOT_INTERVAL = 2.0

    LOW_PROJECTILE_DMG = random.randrange(20, 40)
    MEDIUM_PROJECTILE_DMG = random.randrange(40, 60)
    HIGH_PROJECTILE_DMG = random.randrange(60, 90)

    NORMAL_SHOOTER_RADIUS = Tile.SCALED * 10
    BIG_SHOOTER_RADIUS = Tile.SCALED * 12

    MAX_OF_ONE_ENEMY_TYPE = 7

    @classmethod
    def create_level(cls, game_manager: GameManager, player, level: int):
        """Deals with how many enemies and what types spawn"""

        # Goblins have low hp but are fast and big in numbers.
        # Very small dmg
        # level1 3
        # level2 5
        # level3 7
        # level4 7
        # etc
        for i, _ in enumerate(range(level * 3 - (level - 1))):
            if i > cls.MAX_OF_ONE_ENEMY_TYPE:
                break

            game_manager.create_enemy(
                ChasingEnemy,
                Enemies.goblin,
                Melee(cls.LOW_MELEE_DMG),
                player,
                cls.NORMAL_CHASING_DETECTION_RADIUS,
                moving_speed=cls.VERY_FAST_SPEED
            )

        # Chorts are similar to goblins
        # level1 3
        # level2 5
        # level3 7
        # level4 7
        # etc
        for i, _ in enumerate(range(level * 3 - (level - 1))):
            if i > cls.MAX_OF_ONE_ENEMY_TYPE:
                break

            game_manager.create_enemy(
                ChasingEnemy,
                Enemies.chort,
                Melee(cls.LOW_MELEE_DMG),
                player,
                cls.NORMAL_CHASING_DETECTION_RADIUS,
                moving_speed=cls.VERY_FAST_SPEED
            )

        # Tiny zombies are similar to goblins
        # level1 3
        # level2 5
        # level3 7
        # level4 7
        # etc
        for i, _ in enumerate(range(level * 3 - (level - 1))):
            if i > cls.MAX_OF_ONE_ENEMY_TYPE:
                break

            game_manager.create_enemy(
                ChasingEnemy,
                Enemies.tiny_zombie,
                Melee(cls.LOW_MELEE_DMG),
                player,
                cls.NORMAL_CHASING_DETECTION_RADIUS,
                moving_speed=cls.VERY_FAST_SPEED
            )

        # Ice zombies demons are fast and not insta killable
        # level1 2
        # level2 4
        # level3 6
        # level4 7
        # etc
        for i, _ in enumerate(range(level * 2)):
            if i > cls.MAX_OF_ONE_ENEMY_TYPE:
                break

            game_manager.create_enemy(
                ChasingEnemy,
                Enemies.ice_zombie,
                Melee(cls.NORMAL_MELEE_DMG),
                player,
                cls.BIG_CHASING_DETECTION_RADIUS,
                moving_speed=cls.FAST_SPEED
            )

        # Big demons are tough foes, normal speed but lot HP.
        # Huge dmg and big detection radius
        # level1 3
        # level2 5
        # level3 6
        # level4 7
        # etc
        for i, _ in enumerate(range(level + 2 + level//3)):
            if i > cls.MAX_OF_ONE_ENEMY_TYPE:
                break

            game_manager.create_enemy(
                ChasingEnemy,
                Enemies.big_demon,
                Melee(cls.HIGH_MELEE_DMG),
                player,
                cls.BIG_CHASING_DETECTION_RADIUS,
                moving_speed=cls.NORMAL_SPEED
            )

        # Imps are shooting
        # level1 1
        # level2 2
        # level3 4
        # level4 5
        for i, _ in enumerate(range(level + level//2)):
            if i > cls.MAX_OF_ONE_ENEMY_TYPE:
                break

            game_manager.create_enemy(
                StationaryEnemy,
                Enemies.imp,
                Melee(cls.LOW_MELEE_DMG),
                player,
                cls.NORMAL_SHOOTER_RADIUS,
                shoot_interval=cls.FAST_SHOOT_INTERVAL,
                dmg=cls.LOW_PROJECTILE_DMG
            )

        # Necromancers are shooting
        # level1 0
        # level2 0
        # level3 1
        # level4 2
        for i, _ in enumerate(range(level - 2)):
            if i > cls.MAX_OF_ONE_ENEMY_TYPE:
                break

            game_manager.create_enemy(
                StationaryEnemy,
                Enemies.necromancer,
                Melee(cls.NORMAL_MELEE_DMG),
                player,
                cls.BIG_SHOOTER_RADIUS,
                shoot_interval=cls.SLOW_SHOOT_INTERVAL,
                dmg=cls.HIGH_PROJECTILE_DMG
            )

        # Muddy is slow mowing tank
        # level1 0
        # level2 2
        # level3 4
        # level4 6
        for i, _ in enumerate(range((level - 1) * 2)):
            if i > cls.MAX_OF_ONE_ENEMY_TYPE:
                break

            game_manager.create_enemy(
                ChasingEnemy,
                Enemies.muddy,
                Melee(cls.HIGH_MELEE_DMG),
                player,
                cls.HUGE_CHASING_DETECTION_RADIUS,
                moving_speed=cls.LOW_SPEED
            )

        game_manager.create_potion(
            PotionEffect(
                heal=100.0
            ),
            filename="assets/dungeon/frames/flask_yellow.png"
        )

        for _ in range(0, 3 - level):
            game_manager.create_potion(
                PotionEffect(
                    heal=200.0
                ),
                filename="assets/dungeon/frames/flask_big_yellow.png"
            )
        for _ in range(0, 3 - level):
            game_manager.create_potion(
                PotionEffect(
                    resistance=0.1
                ),
                duration=3.0,
                filename="assets/dungeon/frames/flask_green.png"
            )
        for _ in range(0, 3 - level):
            game_manager.create_potion(
                PotionEffect(
                    strength=0.1
                ),
                duration=3.0,
                filename="assets/dungeon/frames/flask_big_red.png"
            )
        for _ in range(0, 3 - level):
            game_manager.create_potion(
                PotionEffect(
                    speed=0.1
                ),
                duration=3.0,
                filename="assets/dungeon/frames/flask_big_blue.png"
            )
