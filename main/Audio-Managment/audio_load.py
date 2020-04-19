import sys
from aubio import source, notes


filename = "test.wav"


def get_notes(file_name, call_back):
    down_sample = 1
    sample_rate = 44100 // down_sample

    win_s = 512 // down_sample
    hop_s = 256 // down_sample

    s = source(file_name, sample_rate, hop_s)
    sample_rate = s.samplerate

    notes_o = notes("default", win_s, hop_s, sample_rate)

    print("%8s" % "time", "[ start", "vel", "last ]")

    # total number of frames read
    total_frames = 0
    song_notes = []
    while True:
        samples, read = s()
        new_note = notes_o(samples)
        if new_note[0] != 0:
            song_notes.append(((total_frames/float(sample_rate)), new_note[0]))
        total_frames += read

        if read < hop_s:
            return song_notes


#print(get_notes('test.wav', None))

