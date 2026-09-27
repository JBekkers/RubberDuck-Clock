import ctypes
import sys
import atexit
from ctypes import wintypes

# ── Single-instance protection ──────────────────────

MUTEX_NAME = "Local\\RubberDuckClock_SingleInstance"
ERROR_ALREADY_EXISTS = 183

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

kernel32.CreateMutexW.argtypes = [
    ctypes.c_void_p,
    wintypes.BOOL,
    wintypes.LPCWSTR,
]
kernel32.CreateMutexW.restype = wintypes.HANDLE

kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL


def show_startup_error(message):
    """Display an error above the always-on-top clock."""
    ctypes.windll.user32.MessageBoxW(
        None,
        message,
        "RubberDuck Clock",
        0x10 | 0x40000,
    )


def acquire_single_instance():
    """Allow only one running instance of the clock."""
    ctypes.set_last_error(0)

    handle = kernel32.CreateMutexW(
        None,
        False,
        MUTEX_NAME,
    )

    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())

    if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
        kernel32.CloseHandle(handle)
        return False

    atexit.register(kernel32.CloseHandle, handle)
    return True


try:
    if not acquire_single_instance():
        sys.exit(0)

except OSError as error:
    show_startup_error(
        f"Could not start RubberDuck Clock.\n\n{error}"
    )
    sys.exit(1)


from Source.Config.config import load_config
from Source.Config.stats import load_stats, start_session

from Source.animation import animate_sprite, choose_random_animation, duck_clicked, set_config
from Source.UI.menu_manager import setup_menu
from Source.Window_Manager import root, canvas, set_position, start_move, move_window, set_always_on_top
from Source.clock import setup_clock, start_clock
from Source.UI.app import load_font, start_uptime_autosave, schedule_pos_save
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

root.bind(
    "<Configure>",
    lambda event: schedule_pos_save(event, config)
)

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

start_uptime_autosave(stats)

root.mainloop()