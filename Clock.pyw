import tkinter as tk
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import threading
import time
import ntplib
import pystray
import ctypes
import random
import json

import os
from PIL import Image, ImageTk

##LOAD ASSETS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "Sprites")
HATS_DIR = os.path.join(ASSETS_DIR, "Hats")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "Sounds")
CONFIG_DIR = os.path.join(
    os.getenv("APPDATA"),
    "RubberDuckClock"
)

WINDOW_WIDTH = 150
WINDOW_HEIGHT = 150

CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

SPRITE_SIZE = (150, 150)

TIMEZONE = ZoneInfo("Europe/Amsterdam") 
SYNC_INTERVAL = 60   
CLOCK_Y_OFFSET = 30

ANIMATION_FILE = os.path.join(
    ASSETS_DIR,
    "animations.json"
)

NTP_SERVERS = [
    "time.cloudflare.com",
    "time.google.com",
    "time.windows.com",
    "time.apple.com",
    "pool.ntp.org",
]

os.makedirs(CONFIG_DIR, exist_ok=True)

POSITION_FILE = os.path.join(
    CONFIG_DIR,
    "position.txt"
)

# Hide console
try:
    console = ctypes.windll.kernel32.GetConsoleWindow()
    if console:
        ctypes.windll.user32.ShowWindow(console, 0)
except Exception:
    pass

# Tkinter Window
root = tk.Tk()
root.title("Rubber Duck Clock")
##root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+915+0")
def load_position():
    try:
        with open(POSITION_FILE, "r") as f:
            x, y = f.read().split(",")
            return int(x), int(y)

    except Exception:
        # Default first launch position
        return 915, 0

saved_x, saved_y = load_position()

root.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{saved_x}+{saved_y}"
)

root.overrideredirect(True)
root.attributes("-topmost", True)

root.configure(bg="#010203")
root.wm_attributes("-transparentcolor", "#010203")


## CLICK AND DRAG TO MOVE
drag_offset_x = 0
drag_offset_y = 0

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

animations = {}

def load_animation(
    name,
    frame_width,
    frame_height,
    speed,
    looping=False,
    loop_time=0,
    next_animation="Idle",
    weight=0
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
        "weight": weight
    }

with open(ANIMATION_FILE, "r") as f:
    animation_data = json.load(f)

default = animation_data["default"]

FRAME_WIDTH = default["frame_width"]
FRAME_HEIGHT = default["frame_height"]

for name, data in animation_data["animations"].items():

    load_animation(
        name=name,
        frame_width=FRAME_WIDTH,
        frame_height=FRAME_HEIGHT,
        speed=data["speed"],
        looping=data.get("looping", False),
        loop_time=data.get("loop_time", 0),
        next_animation=data.get("next", "Idle"),
        weight=data.get("weight", 0)
    )

current_animation = "Idle"
current_frame = 0
loop_start_time = None

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

            if elapsed >= animation["loop_time"]:
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


# TIME TEXT 
time_display = canvas.create_text(
    CENTER_X,
    CENTER_Y + CLOCK_Y_OFFSET - 10,
    text="--:--",
    font=("Segoe UI", 11, "bold"),
    fill="black",
    anchor="center"
)


# DATE TEXT
date_display = canvas.create_text(
    CENTER_X,
    CENTER_Y + CLOCK_Y_OFFSET + 10,
    text="--/--",
    font=("Segoe UI", 8),
    fill="black",
    anchor="center"
)

def play_animation(name):
    global current_animation
    global current_frame
    global loop_start_time

    current_animation = name
    current_frame = 0

    if animations[name]["looping"]:
        loop_start_time = time.monotonic()
    else:
        loop_start_time = None

def reset_position(icon, item):
    default_x = 915
    default_y = 0

    # Move window
    root.after(
        0,
        lambda: root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{default_x}+{default_y}"
        )
    )

    # Save new position
    try:
        with open(POSITION_FILE, "w") as f:
            f.write(f"{default_x},{default_y}")
    except Exception:
        pass

# TRAY ICON
def shutdown():

    try:
        root.update_idletasks()

        x = root.winfo_x()
        y = root.winfo_y()

        with open(POSITION_FILE, "w") as f:
            f.write(f"{x},{y}")

    except Exception:
        pass


    try:
        icon.stop()
    except Exception:
        pass

    root.destroy()

def quit_app(icon, item):
    root.after(0, shutdown)

root.protocol("WM_DELETE_WINDOW", shutdown)

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
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(
            "Quit",
            quit_app
        ),
    ),
)

threading.Thread(target=icon.run, daemon=True).start()


# Clock Variables
network_time = None
sync_monotonic = None


# SYNC CLOCK WITH NTP SERVERS
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


# Update Display
def update_clock_display():

    if network_time is not None:

        elapsed = time.monotonic() - sync_monotonic

        current_time = network_time + timedelta(seconds=elapsed)

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

#Call functions
animate_sprite()
choose_random_animation()

synchronize_time()
update_clock_display()

root.mainloop()