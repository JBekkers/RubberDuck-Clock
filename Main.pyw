from Source.Config import load_config
from Source.Animation import animate_sprite, choose_random_animation
from Source.Clock import synchronize_time, update_clock_display
from Source.Menu import setup_menu
from Source.Window import root, set_position
from Source.Clock import setup_clock, start_clock
from Source.Window import root, canvas


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
DATA_DIR = os.path.join(BASE_DIR, "Data")
SPRITES_DIR = os.path.join(ASSETS_DIR, "Sprites")
HATS_DIR = os.path.join(ASSETS_DIR, "Hats")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "Sounds")


config = load_config()
settings = config["settings"]

setup_menu(settings, config)

set_position(
    config["position"]["x"],
    config["position"]["y"]
)

setup_clock(canvas)
start_clock(settings)

animate_sprite()
choose_random_animation()

synchronize_time()
update_clock_display()

root.mainloop()