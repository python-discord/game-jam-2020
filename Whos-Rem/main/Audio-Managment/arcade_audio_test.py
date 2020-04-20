import arcade
import pyaudio
import aubio
import math
import numpy as np
import json
import random
import threading
import time

win_s = 1024                # fft size
hop_s = win_s // 2          # hop size
filename = "Camellia_MEGALOVANIA_Remix.wav"
beat = (0, False)

beats = []
once = True

class AudioManage(pyaudio.PyAudio):
    a_source = aubio.source(filename, hop_size=hop_s)
    samplerate = a_source.samplerate
    pitch_o = aubio.notes("default", win_s, hop_s, samplerate)
    temp_o = aubio.tempo("default", win_s, hop_s, samplerate)
    filter = aubio.digital_filter(7)
    filter.set_a_weighting(samplerate)

    click = 0.7 * np.sin(2. * np.pi * np.arange(hop_s) / hop_s * samplerate / 3000.)
    first_time, start_time = True, 0

    def __init__(self):
        super().__init__()
        pyaudio_format = pyaudio.paFloat32
        frames_per_buffer = hop_s
        n_channels = 1
        self.stream = self.open(
            format=pyaudio_format,
            channels=n_channels,
            rate=self.samplerate,
            output=True,
            frames_per_buffer=frames_per_buffer,
            stream_callback=self.pyaudio_callback)

    def pyaudio_callback(self, _in_data, _frame_count, _time_info, _status):
        global beat, run_through, count, once
        if run_through:
            count += 1

        if self.first_time:
            self.first_time, self.start_time = False, _time_info['current_time']

        samples, read = self.a_source()
        #filtered = self.filter(samples)
        filtered = samples
        is_pitch = self.pitch_o(filtered, method="phase")
        if any(is_pitch):
            beat = (is_pitch[0] + is_pitch[1] + is_pitch[2], any(self.temp_o(samples)))
        audiobuf = samples.tobytes()
        if read < hop_s:
            if once:
                run_through = True
                with open('output.json', 'w+') as file:
                    json.dump(keys, file)
                once = False
                print("boOm")
            return audiobuf, pyaudio.paComplete
        return audiobuf, pyaudio.paContinue


SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Audio Test"

# Size of the rectangle
RECT_WIDTH = 50
RECT_HEIGHT = 50

# defaults
default_x, default_y = 300, 0
count = 0
last_val = 0
keys = []
run_through = False


def on_draw(time_delta):
    global beat, last_val, keys, run_through
    arcade.start_render()
    if not run_through:
        height, on = beat
        diffrence = height - last_val
        if diffrence not in range(-3, 3):
            last_val = height

            arcade.draw_rectangle_filled(center_x=diffrence * 7, center_y=300, color=arcade.color.CRIMSON, height=100, width=300)
            if ((diffrence * 7) < 400) and on:
                keys.append([True, False, False])
            elif ((diffrence * 7) < 1000) and on:
                keys.append([False, True, False])
            elif ((diffrence * 7) < 1600) and on:
                keys.append([False, False, True])
            else:
                keys.append([False, False, False])
    else:
        render = keys[count]
        if render[0]:
            arcade.draw_rectangle_filled(center_x=300,
                                         center_y=300,
                                         color=arcade.color.CRIMSON,
                                         height=100,
                                         width=300)
        elif render[1]:
            arcade.draw_rectangle_filled(center_x=900,
                                         center_y=300,
                                         color=arcade.color.CRIMSON,
                                         height=100,
                                         width=300)
        elif render[2]:
            arcade.draw_rectangle_filled(center_x=1500,
                                         center_y=300,
                                         color=arcade.color.CRIMSON,
                                         height=100,
                                         width=300)


def main():
    global music
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(on_draw, 1/30)
    music = AudioManage()
    music.stream.start_stream()
    arcade.run()


if __name__ == "__main__":
    main()
