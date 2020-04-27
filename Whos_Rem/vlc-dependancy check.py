import vlc
import time

vlc_instance = vlc.Instance('--input-repeat=-1')
player = vlc_instance.media_player_new()
media = vlc_instance.media_new(r"Whos_Rem\main\tracks\TRACK_1.mp3")
player.set_media(media)
player.play()
time.sleep(10)