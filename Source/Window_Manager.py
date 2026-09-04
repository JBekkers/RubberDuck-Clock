from Source.Config.style import WINDOW_HEIGHT, WINDOW_WIDTH
from Source.Config.config import load_config

import ctypes
import tkinter as tk

config = load_config()
settings = config["settings"]

menu_window = None
def set_always_on_top(enabled):
    root.attributes("-topmost", enabled)

    if menu_window and menu_window.winfo_exists():
        menu_window.attributes("-topmost", enabled)

def set_menu_window(window):
    global menu_window
    menu_window = window

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", settings["always_on_top"])
root.protocol("WM_DELETE_WINDOW")

root.configure(bg="#010203")
root.wm_attributes("-transparentcolor", "#010203")

def start_move(event, target):
    target._drag_x = event.x_root
    target._drag_y = event.y_root

def update_menu_position(target):
    if menu_window and menu_window.winfo_exists():
        x = (
            target.winfo_x()
            + target.winfo_width() // 2
            - menu_window.winfo_width() // 2
        )

        y = target.winfo_y() + target.winfo_height()

        menu_window.geometry(f"+{x}+{y}")

def move_window(event, target):

    x = target.winfo_x() + event.x_root - target._drag_x
    y = target.winfo_y() + event.y_root - target._drag_y

    target.geometry(f"+{x}+{y}")

    target._drag_x = event.x_root
    target._drag_y = event.y_root

    update_menu_position(target)

    if menu_callback:
        menu_callback(target)

canvas = tk.Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bg="#010203",
    highlightthickness=0
)

canvas.pack()

try:
    console = ctypes.windll.kernel32.GetConsoleWindow()
    if console:
        ctypes.windll.user32.ShowWindow(console, 0)
except Exception:
    pass

def set_position(x, y):
    root.geometry(
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"
    )

menu_callback = None

def set_menu_callback(callback):
    global menu_callback
    menu_callback = callback

