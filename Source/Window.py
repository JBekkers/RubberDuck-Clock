from Source.Constants import WINDOW_HEIGHT, WINDOW_WIDTH
from Source.Config import load_config

import ctypes
import tkinter as tk

drag_offset_x = 0
drag_offset_y = 0

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.protocol("WM_DELETE_WINDOW")

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

def set_position(x, y):
    root.geometry(
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"
    )