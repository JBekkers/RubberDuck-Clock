import tkinter as tk

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import time
import ntplib

import threading
import pystray

import ctypes
import random

import json
import copy
import winsound

import os

from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
DATA_DIR = os.path.join(BASE_DIR, "Data")
SPRITES_DIR = os.path.join(ASSETS_DIR, "Sprites")
HATS_DIR = os.path.join(ASSETS_DIR, "Hats")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "Sounds")
CONFIG_DIR = os.path.join(
    os.getenv("APPDATA"),
    "RubberDuckClock"
)

# =======================
#   SETTINGS CONFIG
# =======================
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(
    CONFIG_DIR,
    "config.json"
)

DEFAULT_CONFIG = {
    "position": {
        "x": 915,
        "y": 0
    },
    "settings": {
        "hourly_quack": False
    }
}


def load_config():

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        # Add missing values if config changes in future
        for section, values in DEFAULT_CONFIG.items():

            if section not in config:
                config[section] = copy.deepcopy(values)

            else:
                for key, value in values.items():
                    if key not in config[section]:
                        config[section][key] = value

        return config

    except Exception:

        return copy.deepcopy(DEFAULT_CONFIG)


def save_config():

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(
                config,
                f,
                indent=4
            )

    except Exception:
        pass

config = load_config()



settings = config["settings"]

# =======================
#  WINDOW CONFIGURATION
# =======================
WINDOW_WIDTH = 150
WINDOW_HEIGHT = 150

CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

drag_offset_x = 0
drag_offset_y = 0

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

root.configure(bg="#010203")
root.wm_attributes("-transparentcolor", "#010203")

def start_move(event):
    global drag_offset_x, drag_offset_y
    drag_offset_x = event.x
    drag_offset_y = event.y

def move_window(event):
    x = event.x_root - drag_offset_x
    y = event.y_root - drag_offset_y
    root.geometry(f"+{x}+{y}")

canvas = tk.Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bg="#010203",
    highlightthickness=0
)

canvas.pack()

canvas.bind("<Button-1>", start_move)
canvas.bind("<B1-Motion>", move_window)

try:
    console = ctypes.windll.kernel32.GetConsoleWindow()
    if console:
        ctypes.windll.user32.ShowWindow(console, 0)
except Exception:
    pass

root.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
    f"+{config['position']['x']}"
    f"+{config['position']['y']}"
)


# =======================
#    ANIMATION ENGINE
# =======================
SPRITE_SIZE = (150, 150)

ANIMATION_FILE = os.path.join(
    DATA_DIR,
    "animations.json"
)

animations = {}

current_animation = "Idle"
current_frame = 0
loop_start_time = None

def load_animation(
    name,
    frame_width,
    frame_height,
    speed,
    looping=False,
    loop_time=0,
    next_animation="Idle",
    weight=0,
    sound=None,
):

    sheet = Image.open(
        os.path.join(SPRITES_DIR, f"{name}.png")
    ).convert("RGBA")

    frames = []

    for i in range(sheet.height // frame_height):

        frame = sheet.crop((
            0,
            i * frame_height,
            frame_width,
            (i + 1) * frame_height
        ))

        frame = frame.resize(
            SPRITE_SIZE,
            Image.Resampling.NEAREST
        )

        frames.append(ImageTk.PhotoImage(frame))

    animations[name] = {
        "frames": frames,
        "speed": speed,
        "looping": looping,
        "loop_time": loop_time,
        "next": next_animation,
        "weight": weight,
        "sound": sound,
    }

with open(ANIMATION_FILE, "r") as f:
    animation_data = json.load(f)

default = animation_data["default"]


for name, data in animation_data["animations"].items():

    load_animation(
        name=name,
        frame_width=default["frame_width"],
        frame_height=default["frame_height"],
        speed=data["speed"],
        looping=data.get("looping", False),
        loop_time=data.get("loop_time", 0),
        next_animation=data.get("next", "Idle"),
        weight=data.get("weight", 0),
        sound=data.get("sound")
    )

sprite_id = canvas.create_image(
    CENTER_X,
    CENTER_Y,
    image=animations[current_animation]["frames"][0],
    anchor="center"
)

def animate_sprite():

    global current_animation
    global current_frame

    animation = animations[current_animation]
    frames = animation["frames"]

    canvas.itemconfig(
        sprite_id,
        image=frames[current_frame]
    )

    current_frame += 1

    if current_frame == len(frames):

        if animation["looping"]:

            elapsed = (
                time.monotonic() - loop_start_time
                if loop_start_time is not None
                else 0
            )   

            if elapsed >= animation["current_loop_time"]:
                play_animation(animation["next"])
            else:
                current_frame = 0

        else:

            play_animation(animation["next"])

    root.after(
        animation["speed"],
        animate_sprite
    )

def choose_random_animation():

    if current_animation != "Idle":
        root.after(2000, choose_random_animation)
        return

    choices = []
    weights = []

    for name, anim in animations.items():
        if anim["weight"] > 0:
            choices.append(name)
            weights.append(anim["weight"])

    if choices:
        animation = random.choices(
            choices,
            weights=weights,
            k=1
        )[0]

        play_animation(animation)

    root.after(6000, choose_random_animation)

def play_animation(name):
    global current_animation
    global current_frame
    global loop_start_time

    current_animation = name
    current_frame = 0
    loop_start_time = time.monotonic()

    animation = animations[current_animation]

    if animation["looping"]:
        loop_time = animation["loop_time"]

        if isinstance(loop_time, list):
            animation["current_loop_time"] = random.uniform(
                loop_time[0],
                loop_time[1]
            )
        else:
            animation["current_loop_time"] = loop_time
    
    if animation["sound"]:
        play_sound(animation["sound"])


# =======================
#   SOUND ENGINE
# =======================

def play_sound(filename):
    path = os.path.join(SOUNDS_DIR, filename)

    winsound.PlaySound(
        path,
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )

# =======================
#       CLOCK CONFIG
# =======================
TIMEZONE = ZoneInfo("Europe/Amsterdam") 
SYNC_INTERVAL = 60   
CLOCK_Y_OFFSET = 30

last_hour_quacked = None
network_time = None
sync_monotonic = None

NTP_SERVERS = [
    "time.cloudflare.com",
    "time.google.com",
    "time.windows.com",
    "time.apple.com",
    "pool.ntp.org",
]

time_display = canvas.create_text(
    CENTER_X,
    CENTER_Y + CLOCK_Y_OFFSET - 10,
    text="--:--",
    font=("Segoe UI", 11, "bold"),
    fill="black",
    anchor="center"
)

date_display = canvas.create_text(
    CENTER_X,
    CENTER_Y + CLOCK_Y_OFFSET + 10,
    text="--/--",
    font=("Segoe UI", 8),
    fill="black",
    anchor="center"
)

def toggle_hourly_quack(icon, item):

    settings["hourly_quack"] = not settings["hourly_quack"]

    save_config()

    icon.update_menu()

def synchronize_time():

    global network_time, sync_monotonic

    try:
        client = ntplib.NTPClient()

        for server in NTP_SERVERS:
            try:
                response = client.request(server, version=3, timeout=3)
                break
            except Exception:
                response = None

        if response is None:
            raise Exception("All NTP servers failed.")

        utc_now = datetime.fromtimestamp(
        response.tx_time,
        tz=timezone.utc
        )

        network_time = utc_now.astimezone(TIMEZONE)

        sync_monotonic = time.monotonic()

    except Exception:
        pass

    root.after(SYNC_INTERVAL * 1000, synchronize_time)


def update_clock_display():

    if network_time is not None:

        elapsed = time.monotonic() - sync_monotonic

        current_time = network_time + timedelta(seconds=elapsed)

        global last_hour_quacked

        if (
            settings["hourly_quack"] and
            current_time.minute == 0 and
            current_animation == "Idle" and
            last_hour_quacked != current_time.hour
        ):
            last_hour_quacked = current_time.hour
            play_animation("Quack")


        elif current_time.minute != 0:
            last_hour_quacked = None



        canvas.itemconfig(
            time_display,
            text=current_time.strftime("%H:%M")
        )

        canvas.itemconfig(
            date_display,
            text=current_time.strftime("%d-%m-%Y")
        )

    else:

        canvas.itemconfig(
            time_display,
            text="Offline"
        )

        canvas.itemconfig(
            date_display,
            text=""
        )
    root.after(200, update_clock_display)

# =======================
#       MENU CONFIG
# =======================
def reset_position(icon, item):

    default_x = 915
    default_y = 0

    config["position"]["x"] = default_x
    config["position"]["y"] = default_y

    save_config()

    root.after(
        0,
        lambda: root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{default_x}+{default_y}"
        )
    )

def shutdown():

    try:
        root.update_idletasks()

        x = root.winfo_x()
        y = root.winfo_y()

        config["position"]["x"] = x
        config["position"]["y"] = y

        save_config()

    except Exception:
        pass

    try:
        icon.stop()
    except Exception:
        pass

    root.destroy()

def quit_app(icon, item):
    root.after(0, shutdown)

tray_icon = Image.open(os.path.join(ASSETS_DIR, "Icon.png"))

icon = pystray.Icon(
    "Duck Clock",
    tray_icon,
    "Duck Clock",
    menu=pystray.Menu(

        pystray.MenuItem(
            "Reset Position",
            reset_position
        ),

        pystray.MenuItem(
            "Quack on full hour",
            toggle_hourly_quack,
            checked=lambda item: settings["hourly_quack"]
        ),

        pystray.Menu.SEPARATOR,

        pystray.MenuItem(
            "Quit",
            quit_app
        ),
    ),
)

def show_context_menu(event):
    menu.tk_popup(event.x_root, event.y_root)

menu = tk.Menu(root, tearoff=1)

menu.add_command(label="Sleep", command=lambda: play_animation("Sleeping_Start"))
menu.add_separator()
menu.add_command(label="Quit", command=shutdown)

canvas.bind("<Button-3>", show_context_menu)

root.protocol("WM_DELETE_WINDOW", shutdown)

# =======================
#    START LOOP
# =======================
threading.Thread(target=icon.run, daemon=True).start()

animate_sprite()
choose_random_animation()

synchronize_time()
update_clock_display()

root.mainloop()