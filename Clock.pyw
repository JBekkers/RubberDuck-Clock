import tkinter as tk
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import threading
import time
import ntplib
import pystray
import ctypes
import random

import os
from PIL import Image, ImageTk

##LOAD ASSETS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "Sprites")
HATS_DIR = os.path.join(ASSETS_DIR, "Hats")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "Sounds")

WINDOW_WIDTH = 150
WINDOW_HEIGHT = 150

CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

SPRITE_SIZE = (150, 150)
FRAME_WIDTH = 128
FRAME_HEIGHT = 120

TIMEZONE = ZoneInfo("Europe/Amsterdam") 
SYNC_INTERVAL = 60   
CLOCK_Y_OFFSET = 30

NTP_SERVERS = [
    "time.cloudflare.com",
    "time.google.com",
    "time.windows.com",
    "time.apple.com",
    "pool.ntp.org",
]

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
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+915+0")
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

def load_animation(name, frame_width, frame_height,speed):
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

        frame = frame.resize(SPRITE_SIZE, Image.Resampling.NEAREST)
        frames.append(ImageTk.PhotoImage(frame))

    animations[name] = {
    "frames": frames,
    "speed": speed
    }

load_animation("Idle", FRAME_WIDTH, FRAME_HEIGHT, 120)
load_animation("Blink", FRAME_WIDTH, FRAME_HEIGHT, 50)
load_animation("TailWag", FRAME_WIDTH, FRAME_HEIGHT, 120)

current_animation = "Idle"
current_frame = 0

sprite_id = canvas.create_image(
    CENTER_X,
    CENTER_Y,
    image=animations[current_animation]["frames"][0],
    anchor="center"
)

def animate_sprite():
    global current_frame, current_animation
    animation = animations[current_animation]
    frames = animation["frames"]

    current_frame += 1

    if current_frame >= len(frames):

        if current_animation != "Idle":
            current_animation = "Idle"

        current_frame = 0
        animation = animations[current_animation]
        frames = animation["frames"]

    canvas.itemconfig(
        sprite_id,
        image=frames[current_frame]
    )

    speed = animation["speed"]
    root.after(speed, animate_sprite)

def choose_random_animation():

    if current_animation != "Idle":
        root.after(2000, choose_random_animation)
        return

    roll = random.random()

    if roll < 0.10:
        play_animation("Blink")

    elif roll < 0.30:
        play_animation("TailWag")

    root.after(2000, choose_random_animation)


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
    global current_animation, current_frame

    current_animation = name
    current_frame = 0


# TRAY ICON
def shutdown():
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
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", quit_app),
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