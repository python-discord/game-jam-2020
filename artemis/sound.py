"""Play sound."""
from pyglet.media import Player, load

from constants import ASSETS
import settings


class BackgroundMusic(Player):
    """Class to loop the background music."""

    def __init__(self):
        """Start playing the music."""
        super().__init__()
        self.loop = True
        self.volume = settings.get_music_volume()
        self.track = None
        self.play()

    def update_vol(self):
        """Update the volume if it changed."""
        self.volume = settings.get_music_volume()

    def switch_track(self, new: str):
        """Switch to a new track."""
        self.track = new
        had_source = bool(self._source)
        self.queue(load(f'{ASSETS}audio/{new}.wav'))
        if had_source:
            self.next_source()


music = BackgroundMusic()
sfxs = []


def play_sound_effect(name: str, volume: float = 1.0):
    """Play a sound effect."""
    player = Player()
    player.queue(load(f'{ASSETS}audio/{name}.wav'))
    player.volume = volume * settings.get_sfx_volume()
    player.play()
    sfxs.append(player)
