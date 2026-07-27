from Source.Config.style import WINDOW_HEIGHT, WINDOW_WIDTH

import ctypes
import tkinter as tk

menu_window = None

def set_menu_window(window):
    global menu_window
    menu_window = window

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.protocol("WM_DELETE_WINDOW")

root.configure(bg="#010203")
root.wm_attributes("-transparentcolor", "#010203")

def start_move(event, target):
    target._drag_x = event.x_root
    target._drag_y = event.y_root


def move_window(event, target):

    x = target.winfo_x() + (event.x_root - target._drag_x)
    y = target.winfo_y() + (event.y_root - target._drag_y)

    target.geometry(f"+{x}+{y}")

    target._drag_x = event.x_root
    target._drag_y = event.y_root

    if menu_window and menu_window.winfo_exists():

        menu_x = (
            x 
            + (target.winfo_width() // 2)
            - (menu_window.winfo_width() // 2)
        )

        menu_y = y + target.winfo_height()

        menu_window.geometry(
            f"+{menu_x}+{menu_y}"
        )

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

