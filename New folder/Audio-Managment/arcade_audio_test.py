import arcade
from aubio import source, notes
import time


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


# --- Set up the constants

# Size of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Bouncing Rectangle Example"

# Size of the rectangle
RECT_WIDTH = 50
RECT_HEIGHT = 50

# note making
music_notes = get_notes('test.wav', None)


# defaults
default_x, default_y = 300, 0
count = 0


def on_draw(delta_time):
    global count, start
    """
    Use this function to draw everything to the screen.
    """

    # Start the render. This must happen before any drawing
    # commands. We do NOT need a stop render command.
    arcade.start_render()

    # Draw a rectangle.
    # For a full list of colors see:
    # http://arcade.academy/arcade.color.html
    arcade.draw_rectangle_filled(on_draw.center_x, on_draw.center_y,
                                 RECT_WIDTH, RECT_HEIGHT,
                                 arcade.color.ALIZARIN_CRIMSON)

    end = time.time() - start
    if end > music_notes[count][0]:
        on_draw.center_y = default_y + music_notes[count][1]
        count += 1


on_draw.center_x = 300  # type: ignore # dynamic attribute on function obj  # Initial x position
on_draw.center_y = 0   # type: ignore # dynamic attribute on function obj  # Initial y position

song = arcade.Sound('test.wav')
start = None

def main():
    global start
    # Open up our window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.WHITE)

    # Tell the computer to call the draw command at the specified interval.
    arcade.schedule(on_draw, 1 / 60)

    # Run the program
    song.play(volume=0.01)
    start = time.time()
    arcade.run()


if __name__ == "__main__":
    main()
