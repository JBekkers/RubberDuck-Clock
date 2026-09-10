from Source.Config.config import load_config
from Source.Config.stats import load_stats, start_session

from Source.animation import animate_sprite, choose_random_animation, duck_clicked, set_config
from Source.UI.menu_manager import setup_menu
from Source.Window_Manager import root, canvas, set_position, start_move, move_window, set_always_on_top
from Source.clock import setup_clock, start_clock
from Source.UI.app import load_font
from Source.sound import set_sound_volume

from Source.Particle_spawner import ParticleSystem

load_font("Pxls-Regular.ttf")

config = load_config()
stats = load_stats()

settings = config["settings"]

start_session(stats)
set_config(config, stats)

set_always_on_top(settings["always_on_top"])
particle_system = ParticleSystem()

particle_system.set_disabled(
    "Bubbles",
    settings["disable_particles"]
)

setup_menu(
    settings,
    config,
    stats,
    particle_system
)


set_position(
    config["position"]["x"],
    config["position"]["y"]
)

set_sound_volume(
    settings.get("sound_volume", 100)
)

def on_click(event):
    start_move(event, root)
    duck_clicked(event)

def on_move(event):
    move_window(event, root)

canvas.tag_bind(
    "draggable",
    "<Button-1>",
    on_click
)

canvas.tag_bind(
    "draggable",
    "<B1-Motion>",
    on_move
)

setup_clock()
start_clock(settings)

animate_sprite()
choose_random_animation()

root.mainloop()