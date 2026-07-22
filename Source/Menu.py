import pystray
from Source.Window_Manager import root, canvas
from Source.Paths import ASSETS_DIR
from Source.Constants import WINDOW_HEIGHT, WINDOW_WIDTH

from Source.Config import save_config
from PIL import Image

import os
import tkinter as tk
import threading

from Source.Animation_Manager import play_animation

settings = None
config = None

def setup_menu(app_settings, app_config):
    global settings, config

    settings = app_settings
    config = app_config

    create_tray_icon()

    threading.Thread(
        target=icon.run,
        daemon=True
    ).start()

def reset_position(icon, item):

    default_x = 915
    default_y = 0

    config["position"]["x"] = default_x
    config["position"]["y"] = default_y

    save_config(config)

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

        save_config(config)

    except Exception:
        pass

    try:
        icon.stop()
    except Exception:
        pass

    root.destroy()

def quit_app(icon, item):
    root.after(0, shutdown)


def toggle_hourly_quack(icon, item):

    settings["hourly_quack"] = not settings["hourly_quack"]

    save_config(config)

    icon.update_menu()

tray_icon = Image.open(os.path.join(ASSETS_DIR, "Icon.png"))

icon = None


def create_tray_icon():

    global icon

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