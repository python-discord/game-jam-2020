import sys
import time
import pyaudio
import aubio
import numpy as np

win_s = 1024                # fft size
hop_s = win_s // 2          # hop size


filename = "test_4.wav"


# create aubio source
a_source = aubio.source(filename, hop_size=hop_s)
samplerate = a_source.samplerate

# create aubio tempo detection
a_tempo = aubio.pitch("default", win_s, hop_s, samplerate)

# create a simple click sound
click = 0.7 * np.sin(2. * np.pi * np.arange(hop_s) / hop_s * samplerate / 3000.)

first_time, start_time = True, 0


def pyaudio_callback(_in_data, _frame_count, _time_info, _status):
    global first_time, start_time
    if first_time:
        first_time, start_time = False, _time_info['current_time']
    print(float(_time_info['current_time']) - int(start_time))

    samples, read = a_source()
    is_beat = a_tempo(samples)
    if is_beat:
        print(is_beat)
    audiobuf = samples.tobytes()
    if read < hop_s:
        return audiobuf, pyaudio.paComplete
    return audiobuf, pyaudio.paContinue


music = AudioManage()
while stream.is_active():
    time.sleep(0.1)

# stop pyaudio stream
stream.stop_stream()
stream.close()
# close pyaudio
p.terminate()