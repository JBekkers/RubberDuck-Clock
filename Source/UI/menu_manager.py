import pystray
from Source.Window_Manager import root, canvas
from Source.Config.paths import ASSETS_DIR

from PIL import Image

import os
import threading

from Source.UI.app import reset_position, shutdown
from Source.UI.Menu_Tabs.tab_loader import open_settings
from Source.UI.Menu_Button import create_menu_button

settings = None
config = None
menu_window = None

def setup_menu(app_settings, app_config):
    global settings, config

    settings = app_settings
    config = app_config

    create_tray_icon()

    threading.Thread(
        target=icon.run,
        daemon=True
    ).start()


def tray_reset_position(icon, item):
    reset_position(config)


def tray_quit_app(icon, item):

    root.after(
        0,
        lambda: shutdown(config, icon)
    )

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
                tray_reset_position
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Quit Application",
                tray_quit_app
            ),
        ),
    )

def toggle_menu(event=None):
    global menu_window

    # Menu already open -> close it
    if menu_window is not None and menu_window.winfo_exists():
        menu_window.destroy()
        menu_window = None
        return

    actions = {
        "reset_position": lambda: reset_position(config),
        "quit": lambda: shutdown(config, icon)
    }

    menu_window = open_settings(
        root,
        settings,
        config,
        actions
    )

    # If the user closes it manually
    menu_window.protocol(
        "WM_DELETE_WINDOW",
        close_menu
    )

def close_menu():
    global menu_window

    if menu_window is not None:
        menu_window.destroy()
        menu_window = None

create_menu_button(toggle_menu)