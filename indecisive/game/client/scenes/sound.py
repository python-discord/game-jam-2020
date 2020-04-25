import arcade
import time
import random


class Sound:
    def __init__(self):
        self.list_music = []
        self.song_number = random.randint(0, 4)
        self.music = None

    def setup(self, pressed):
        self.list_music = ["./assets/music1.mp3", "./assets/music2.mp3", "./assets/music3.mp3", "./assets/music4.mp3",
                           "./assets/music5.mp3"]

        self.play_song()

    def play_song(self):
        self.music = arcade.Sound(self.list_music[self.song_number], streaming=True)
        print(self.music)
        if not self.music:
            self.music.stop()
        self.music.play(0.01)
        time.sleep(0.05)

    def change_song(self):
        self.song_number += 1
        if self.song_number >= len(self.music):
            self.song_number = 0


