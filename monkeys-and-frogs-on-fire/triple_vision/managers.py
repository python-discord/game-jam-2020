import itertools
from typing import Optional, Tuple, List

import arcade

from triple_vision import Settings as s, SoundSettings as ss
from triple_vision.entities import DamageIndicator, States
from triple_vision.sound import SoundTrack


class GameManager:

    def __init__(self, view) -> None:
        self.view = view

        self.enemies = arcade.SpriteList()
        self.player_projectiles = arcade.SpriteList()
        self.enemy_projectiles = arcade.SpriteList()
        self.damage_indicators = arcade.SpriteList()

        self.spikes: Optional[arcade.SpriteList] = None

        self.points = 0
        self.prev_sent = False

    def draw(self) -> None:
        self.enemies.draw()
        self.player_projectiles.draw()
        self.enemy_projectiles.draw()
        self.damage_indicators.draw()

    def create_enemy(self, enemy_class, *args, **kwargs) -> None:
        enemy = enemy_class(ctx=self, *args, **kwargs)
        enemy.setup()
        self.enemies.append(enemy)

    def create_dmg_indicator(self, text: str, position: Tuple[float, float]) -> None:
        dmg_indicator = DamageIndicator(text, *position)
        self.damage_indicators.append(dmg_indicator)

    def on_update(self, delta_time) -> None:
        for enemy in self.enemies:

            projectile_hit_enemy = arcade.check_for_collision_with_list(enemy, self.player_projectiles)
            for projectile in projectile_hit_enemy:
                self.create_dmg_indicator(str(projectile.dmg), enemy.position)
                enemy.hit(projectile)
                projectile.kill()

        projectiles_hit_player = arcade.check_for_collision_with_list(self.view.player, self.enemy_projectiles)
        for projectile in projectiles_hit_player:
            self.view.player.hit(projectile)
            projectile.kill()

        spikes_hit = arcade.check_for_collision_with_list(self.view.player, self.spikes)
        for spike in spikes_hit:
            if 0 < spike.ticks < 7:
                self.view.player.hit(spike)

        self.enemies.on_update(delta_time)
        self.player_projectiles.on_update(delta_time)
        self.enemy_projectiles.on_update(delta_time)
        self.damage_indicators.on_update(delta_time)

        if not self.view.player.is_alive and not self.prev_sent:
            # send score to server
            pass

    def enemy_killed(self, enemy) -> None:
        self.points += enemy.kill_value


class CardManager:

    def __init__(self, view) -> None:
        self.view = view

        self.cards = arcade.SpriteList()
        self.colors = ('red', 'green', 'blue')

        card_scale = s.SCALING / 6

        self.MIN_CARD_HEIGHT = -132 * card_scale
        self.MAX_CARD_HEIGHT = 84 * card_scale
        self.MAX_CARD_HOVER_HEIGHT = 280 * card_scale

        for idx, color in enumerate(self.colors):
            self.cards.append(
                arcade.Sprite(
                    filename=f'assets/wizard/{color}_card.png',
                    scale=card_scale,
                    center_x=s.WINDOW_SIZE[0] / 1.35 + (idx - 1) * 400 * card_scale,
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
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                self.cards[0].left < x < self.cards[-1].right and
                self.cards[0].bottom < y < self.cards[-1].top
            ):

                for idx, card in enumerate(self.cards):
                    if (
                        card.left < x < card.right and
                        card.bottom < y < card.top
                    ):
                        self.view.player.curr_color = self.colors[idx]
                        self.show_cards = False
                        self.view.slow_down = False

                return True

        return False

    def draw(self) -> None:
        self.cards.draw()

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

        self.cards.update()


class SoundtrackManager:
    def __init__(self, sounds: List[arcade.Sound] = []) -> None:
        self._sounds = sounds
        self._sounds_cycle = itertools.cycle(self._sounds)
        self.curr_sound: SoundTrack = None
        self.tick_delta = 0.0
        self.playing = False

    def add_sound(self, sound_name: str, faded: bool = False, max_volume: float = 1.0) -> None:
        self._sounds.append(SoundTrack(sound_name, is_faded=faded, max_volume=max_volume))
        self.update_cycle()

    def remove_sound(self, sound_name: str):
        self._sounds = [sound for sound in self._sounds if sound.file_name != sound_name]
        self.update_cycle()

    def play_external_sound(
        self, sound_name: str = None, faded: bool = False, max_volume: float = 1.0
    ) -> None:
        self.curr_sound = SoundTrack(sound_name, is_faded=faded, max_volume=max_volume)
        self.playing = False

    def play_sound_from_list(self, index):
        self.curr_sound = (
            self._sounds[index]
            if index - len(self._sounds) <= index < len(self._sounds)
            else self.curr_sound
        )
        self.playing = False

    def toggle_next_sound(self) -> None:
        self.curr_sound = next(self._sounds_cycle)

    def update_cycle(self):
        self._sounds_cycle = itertools.cycle(self._sounds)

    @staticmethod
    def load_sound(
        file_name: str, is_faded: bool = False, max_volume: float = 1.0
    ) -> Optional[SoundTrack]:

        try:
            sound = SoundTrack(file_name, is_faded=is_faded, max_volume=max_volume)
            return sound
        except Exception as e:
            print(f'Unable to load sound file: "{file_name}". Exception: {e}')
            return None

    def update(self, delta_time: float) -> None:
        self.tick_delta += delta_time

        if self.curr_sound is None:
            return

        if not self.playing:
            arcade.play_sound(self.curr_sound)
            self.playing = True

        if not self.curr_sound.faded:
            return

        if self.tick_delta < ss.FADE_FREQUENCY:
            return

        self.curr_sound.set_volume(self.curr_sound.get_volume() + ss.FADE_AMOUNT)
        self.tick_delta = 0.0


class CursorManager:
    def __init__(self, view: arcade.View, player):
        self.view = view
        self.window = view.window
        self.player = player

        self._curr_cursor: arcade.Sprite = None
        self.cursors = {
            "moving": arcade.Sprite("assets/crosshairs/moving.png"),  # TODO Add seperate crosshair
            "ranged": arcade.Sprite("assets/crosshairs/ranged.png"),
            "blocked": arcade.Sprite("assets/crosshairs/blocked.png")
        }
        self.window.set_mouse_visible(False)

    def set_curr_cursor(self, value):
        self._curr_cursor = self.cursors.get(value, None)

    def get_curr_cursor(self):
        return self._curr_cursor

    curr_cursor = property(get_curr_cursor, set_curr_cursor)

    def on_mouse_motion(self, x, y):
        if self._curr_cursor is None:
            return
        self._curr_cursor.center_x = x
        self._curr_cursor.center_y = y

    def process_mouse_motion(self, x, y):
        if not arcade.get_sprites_at_exact_point((x, y), self.view.collision_list):
            return
        self.curr_cursor = "blocked"

    def update(self):
        if self.player.state == States.ATTACKING_RANGED:
            self.curr_cursor = "ranged"
        elif self.player.state == States.MOVING:
            self.curr_cursor = "moving"
        elif self.player.state == States.AIMING_BLOCKED:
            self.curr_cursor = "blocked"
        elif self.player.state == States.IDLE:
            # TODO
            pass

    def draw(self):
        self._curr_cursor.draw()
