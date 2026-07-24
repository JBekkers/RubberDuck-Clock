import winsound
import os
from Source.Config.paths import SOUNDS_DIR

def play_sound(filename):
    path = os.path.join(SOUNDS_DIR, filename)

    winsound.PlaySound(
        path,
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )