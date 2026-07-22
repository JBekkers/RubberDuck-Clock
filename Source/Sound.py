import winsound
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")

SOUNDS_DIR = os.path.join(ASSETS_DIR, "Sounds")

def play_sound(filename):
    path = os.path.join(SOUNDS_DIR, filename)

    winsound.PlaySound(
        path,
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )