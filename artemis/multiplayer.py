"""Multiplayer game functionality."""
from __future__ import annotations
import arcade

from constants import (
    BACKGROUND, FONT, GRAVITY, HEIGHT, SCALING, SIDE, SPEED, TOP, WIDTH
)
import displays
from engine import PhysicsEngine
import player
from sprites import Block, Gem, RandomBlock
from ui import View
import views


class MultiplayerGame(View):
    """A single run of a multiplayer game."""

    reset_viewport = False

    def __init__(self, players: int):
        """Create sprites and set up counters etc."""
        super().__init__()
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.set_background_color(BACKGROUND)

        self.left = 0
        self.time_left = 90
        self.randomblocks = 2
        self.paused = False
        self.pause_screen = None
        self.blocks = arcade.SpriteList()
        self.gems = arcade.SpriteList()
        self.others = arcade.SpriteList()
        self.spikes = arcade.SpriteList()
        self.players = arcade.SpriteList()

        # sprites
        import player
        for n in range(players):
            self.players.append(player.Player(self, n))

        size = int(128 * SCALING)
        for x in range(-SIDE, WIDTH + SIDE, size):
            Block(self, x, HEIGHT - TOP, False)
            Block(self, x, size // 2, True)

        for _ in range(3):
            Gem(self)
        for _ in range(2):
            RandomBlock(self)

        self.pauseplay = displays.PausePlay(0, HEIGHT - 40, self)
        self.buttons.append(self.pauseplay)

        self.engines = []
        for player in self.players:
            blocks = arcade.SpriteList()
            for block in self.blocks:
                blocks.append(block)
            for other in self.players:
                if other != player:
                    blocks.append(other)
            player.blocks = blocks
            engine = PhysicsEngine(player, blocks, GRAVITY)
            self.engines.append(engine)
            player.engine = engine

        self.sprite_lists = [
            self.blocks, self.gems, self.others, self.spikes
        ]

    def on_draw(self):
        """Draw all the sprites and UI elements."""
        arcade.start_render()
        self.pauseplay.center_x = self.left + WIDTH - 40
        super().on_draw()
        for n, player in enumerate(self.players):
            center_x = n * (WIDTH / 4) + self.left + 136.5
            arcade.draw_text(
                text=f'Player {n + 1}',
                start_x=center_x,
                start_y=HEIGHT - 5,
                color=arcade.color.WHITE, font_size=20, anchor_x='center',
                anchor_y='top', font_name=FONT.format(type='b')
            )
            if player.death_message:
                message = (
                    f'{player.death_message}, {player.revive_after // 60}'
                )
                colour = (255, 0, 0)
            else:
                message = f'Score: {player.score:3d}'
                colour = (255, 255, 255)
            arcade.draw_text(
                text=message,
                start_x=center_x,
                start_y=HEIGHT - TOP + 21,
                color=colour, font_size=20, anchor_x='center',
                font_name=FONT.format(type='r')
            )
        for sprite_list in self.sprite_lists:
            sprite_list.draw()
        for player in self.players:
            player.draw()
        if self.paused:
            arcade.draw_lrtb_rectangle_filled(
                left=self.left, right=WIDTH + self.left, top=HEIGHT, bottom=0,
                color=(255, 255, 255, 100)
            )
            super().on_draw()
            if not self.pause_screen:
                self.pause_screen = views.Paused(
                    self,  lambda: MultiplayerGame(len(self.players))
                )
                self.window.show_view(self.pause_screen)

    def on_update(self, timedelta: float):
        """Move sprites and update counters."""
        super().on_update(timedelta)
        if not self.paused:
            self.time_left -= timedelta
            if self.time_left < 0:
                self.time_up()
                return
            for sprite_list in self.sprite_lists:
                sprite_list.update()
            for player in self.players:
                player.update()
            if self.randomblocks < 6:
                progress = self.left / WIDTH
                if 2 + progress / 3 < self.randomblocks:
                    self.randomblocks += 1
                    RandomBlock(self)
            self.scroll()

    def save(self):
        """Don't save anything in multiplayer mode."""

    def time_up(self):
        """Display the game over view when the time runs out."""
        self.window.show_view(views.GameOver(
            'Time Up!', [i.score for i in self.players],
            lambda: MultiplayerGame(len(self.players))
        ))

    def game_over(self, message: str, player: displays.Player):
        """Kill the player and show some explanatory message."""
        player.score = 0
        for box in player.boxes:
            box.remove_gem()
        player.revive_after = 240
        player.death_message = message
        for other in self.players:
            if other != player:
                other.blocks.remove(player)

    def scroll(self):
        """Scroll the viewport."""
        self.left += SPEED
        arcade.set_viewport(self.left, WIDTH + self.left, 0, HEIGHT)
        for player in self.players:
            if self.left > player.right and player.revive_after is None:
                self.game_over('Got Stuck', player)

    def on_key_press(self, key: int, _modifiers: int):
        """Process key press."""
        if not self.paused:
            if key == arcade.key.W:
                self.players[0].switch()
            elif key == arcade.key.SPACE and len(self.players) > 1:
                self.players[1].switch()
            elif key in (arcade.key.UP,
                         arcade.key.LSHIFT,
                         arcade.key.RSHIFT) and len(self.players) > 2:
                self.players[2].switch()
