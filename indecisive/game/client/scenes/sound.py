import arcade
import time


class Sound:
    def __init__(self):
        self.list_music = []
        self.song_number = 0
        self.music = None

    def setup(self):
        self.list_music = ["./assets/muse.mp3"]
        self.play_song()

    def play_song(self):
        self.music = arcade.Sound(self.list_music[self.song_number], streaming=True)
        self.music.play(0.01)
        time.sleep(0.05)

    def stop_song(self):
        self.music.stop()

    def change_song(self):
        self.song_number += 1
        if self.song_number >= len(self.music):
            self.song_number = 0


