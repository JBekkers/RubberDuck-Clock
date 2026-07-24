import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "Sounds")
DATA_DIR = os.path.join(BASE_DIR, "Data")
SPRITES_DIR = os.path.join(ASSETS_DIR, "Sprites")