"""Play sound."""
from __future__ import annotations
import pyglet
from pyglet.media import Player, load

from constants import ASSETS
import settings


class FadeOut(Player):
    """Class to fade out old tracks."""

    def __init__(self, old: BackgroundMusic):
        """Get the music and position from the old player."""
        super().__init__()
        self.volume = old.volume
        self.queue(load(f'{ASSETS}audio/{old.track}.wav'))
        self.seek(old.time)
        self.play()
        self.loop = True
        pyglet.clock.schedule_once(self.fade_out, 0.1)

    def fade_out(self, dt: float = None):
        """Fade out of the old track."""
        if self.volume > 0:
            self.volume = max((self.volume - 0.01, 0))
            pyglet.clock.schedule_once(self.fade_out, 0.1)


class BackgroundMusic(Player):
    """Class to loop the background music."""

    def __init__(self):
        """Start playing the music."""
        super().__init__()
        self.loop = True
        self.master_volume = settings.get_music_volume()
        self.volume = self.master_volume
        self.track = None
        self.play()

    def update_vol(self):
        """Update the volume if it changed."""
        self.master_volume = settings.get_music_volume()
        self.volume = self.master_volume

    def switch_track(self, new: str):
        """Switch to a new track."""
        if self._source:
            FadeOut(self)
        self.track = new
        had_source = bool(self._source)
        self.queue(load(f'{ASSETS}audio/{new}.wav'))
        if had_source:
            self.next_source()
        self.volume = 0
        pyglet.clock.schedule_once(self.fade_in, 0.1)

    def fade_in(self, dt: float = None):
        """Fade in to the next track."""
        if self.volume < self.master_volume:
            self.volume += 0.001
            pyglet.clock.schedule_once(self.fade_in, 0.1)


music = BackgroundMusic()
sfxs = []


def play_sound_effect(name: str, volume: float = 1.0):
    """Play a sound effect."""
    player = Player()
    player.queue(load(f'{ASSETS}audio/{name}.wav'))
    player.volume = volume * settings.get_sfx_volume()
    player.play()
    sfxs.append(player)
