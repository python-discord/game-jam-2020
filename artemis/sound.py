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
        self.queue(load(ASSETS + 'audio/music.wav'))
        self.volume = settings.get_music_volume()
        self.play()

    def update_vol(self):
        """Update the volume if it changed."""
        self.volume = settings.get_music_volume()


music = BackgroundMusic()
sfxs = []


def play_sound_effect(name: str, volume: float = 1.0):
    """Play a sound effect."""
    player = Player()
    player.queue(load(f'{ASSETS}audio/{name}.wav'))
    player.volume = volume * settings.get_sfx_volume() * 2
    player.play()
    sfxs.append(player)
