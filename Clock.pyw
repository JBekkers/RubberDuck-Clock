import tkinter as tk
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import threading
import time
import ntplib
import pystray
import ctypes

import os
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WINDOW_WIDTH = 150
WINDOW_HEIGHT = 150

CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

SPRITE_SIZE = (150, 150)

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


def move_window(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")


canvas = tk.Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bg="#010203",
    highlightthickness=0
)

canvas.pack()

canvas.bind("<B1-Motion>", move_window)

sprite = Image.open(
    os.path.join(BASE_DIR, "ClockSkins", "duck.png")
).convert("RGBA")

sprite = sprite.resize(
    SPRITE_SIZE,
    Image.Resampling.NEAREST
)

sprite_photo = ImageTk.PhotoImage(sprite)

sprite_id = canvas.create_image(
    CENTER_X,
    CENTER_Y,
    anchor="center",
    image=sprite_photo
)

# Time text
time_display = canvas.create_text(
    CENTER_X,
    CENTER_Y + CLOCK_Y_OFFSET - 10,
    text="--:--",
    font=("Segoe UI", 11, "bold"),
    fill="black",
    anchor="center"
)


# Date text
date_display = canvas.create_text(
    CENTER_X,
    CENTER_Y + CLOCK_Y_OFFSET + 10,
    text="--/--",
    font=("Segoe UI", 8),
    fill="black",
    anchor="center"
)

# Tray Icon
def shutdown():
    try:
        icon.stop()
    except Exception:
        pass

    root.destroy()

def quit_app(icon, item):
    root.after(0, shutdown)

root.protocol("WM_DELETE_WINDOW", shutdown)

tray_icon = Image.open(os.path.join(BASE_DIR, "Icon.png"))

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


# Synchronize Clock time with ntp server
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
synchronize_time()
update_clock_display()

root.mainloop()