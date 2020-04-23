"""The core game functionality."""
import arcade

from constants import BACKGROUND, FONT, HEIGHT, SCALING, SIDE, TOP, WIDTH
from displays import Box, PausePlay
from engine import BiDirectionalPhysicsEnginePlatformer
from player import Player
from scores import add_score, add_time, get_hiscore
from sprites import Block, Gem, RandomBlock
from ui import View
import views


class Game(View):
    """A single run of the game."""

    reset_viewport = False

    def __init__(self):
        """Create sprites and set up counters etc."""
        super().__init__()
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.set_background_color(BACKGROUND)

        self.left = 0
        self.score = 0
        self.time = 0
        self.randomblocks = 2
        self.hiscore = get_hiscore()
        self.paused = False
        self.pause_screen = None
        self.blocks = arcade.SpriteList()
        self.gems = arcade.SpriteList()
        self.boxes = arcade.SpriteList()
        self.others = arcade.SpriteList()
        self.spikes = arcade.SpriteList()

        # sprites
        self.player = Player(self)

        size = int(128 * SCALING)
        for x in range(-SIDE, WIDTH + SIDE, size):
            Block(self, x, HEIGHT - TOP, False)
            Block(self, x, size // 2, True)

        for _ in range(3):
            Gem(self)
        for _ in range(2):
            RandomBlock(self)

        for n in range(5):
            Box(self, n)

        self.pauseplay = PausePlay(0, HEIGHT - 40, self)
        self.buttons.append(self.pauseplay)

        self.engine = BiDirectionalPhysicsEnginePlatformer(
            self.player, self.blocks, 1
        )

        self.sprite_lists = [
            self.blocks, self.gems, self.boxes, self.others, self.spikes
        ]

    def on_draw(self):
        """Draw all the sprites and UI elements."""
        arcade.start_render()
        self.pauseplay.center_x = self.left + WIDTH - 40
        super().on_draw()
        arcade.draw_text(
            text=f'High Score: {self.hiscore:03d}',
            start_x=self.left + WIDTH - 100,
            start_y=HEIGHT - (TOP - self.blocks[0].height // 2) // 2 + 15,
            color=arcade.color.WHITE, font_size=20, anchor_x='right',
            anchor_y='center', font_name=FONT.format(type='b')
        )
        arcade.draw_text(
            text=f'Score: {self.score:03d}',
            start_x=self.left + WIDTH - 100,
            start_y=HEIGHT - (TOP - self.blocks[0].height // 2) // 2 - 15,
            color=arcade.color.WHITE, font_size=20, anchor_x='right',
            anchor_y='center', font_name=FONT.format(type='b')
        )
        for sprite_list in self.sprite_lists:
            sprite_list.draw()
        self.player.draw()
        if self.paused:
            arcade.draw_lrtb_rectangle_filled(
                left=self.left, right=WIDTH + self.left, top=HEIGHT, bottom=0,
                color=(255, 255, 255, 100)
            )
            super().on_draw()
            if not self.pause_screen:
                self.pause_screen = views.Paused(self)
                self.window.show_view(self.pause_screen)

    def on_update(self, timedelta: float):
        """Moove sprites and update counters."""
        super().on_update(timedelta)
        if not self.paused:
            self.time = timedelta
            for sprite_list in self.sprite_lists:
                sprite_list.update()
            self.player.update(timedelta)
            if self.randomblocks < 6:
                progress = self.left / WIDTH
                if 2 + progress / 3 < self.randomblocks:
                    self.randomblocks += 1
                    RandomBlock(self)
            self.engine.update()
            self.scroll()

    def gem_added(self):
        """Check if the inventory is full or gems can be matched."""
        colours = [box.colour for box in self.boxes if box.colour]
        counts = {'r': 0, 'b': 0, 'y': 0}
        for colour in colours:
            if colour == 'w':
                for key in counts:
                    counts[key] += 1
            elif colour in counts:
                counts[colour] += 1
        all_three = None
        for colour in counts:
            if counts[colour] >= 3:
                all_three = colour
        if all_three:
            self.score += 1
            self.remove_three(all_three)
            return
        over = False
        size = 5 - colours.count('p')
        unique = sum(1 for i in 'rby' if (i in colours))
        if len(colours) == 5:
            over = True
        elif size < 3:
            over = True
        elif size - unique < 2:
            over = True
        if over:
            self.game_over('Inventory Full')

    def remove_three(self, colour: str):
        """Once notified that there are three of some colour, remove them."""
        removed = 0
        for box in self.boxes:
            if box.colour == colour:
                box.remove_gem()
                removed += 1
                if removed == 3:
                    return
        for box in self.boxes:
            if box.colour == 'w':
                box.remove_gem()
                removed += 1
                if removed == 3:
                    return

    def save(self):
        """Save the player's score and time spent playing."""
        add_score(self.score)
        add_time(self.time)

    def game_over(self, message: str):
        """Display the game over view with some explanatory message."""
        self.save()
        self.window.show_view(views.GameOver(message))

    def scroll(self):
        """Scroll the viewport."""
        self.left += self.player.speed
        arcade.set_viewport(self.left, WIDTH + self.left, 0, HEIGHT)
        if self.left > self.player.right:
            self.game_over('Got Stuck')

    def on_key_press(self, _key: int, _modifiers: int):
        """Process key press."""
        if not self.paused:
            self.player.switch()
