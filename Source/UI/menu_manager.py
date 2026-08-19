import pystray
from Source.Window_Manager import root, set_always_on_top
from Source.Config.paths import ASSETS_DIR

from PIL import Image

import os
import threading

from Source.clock import timezone_changed

from Source.UI.app import reset_position, shutdown, restart_application
from Source.UI.Menu_Tabs.tab_loader import open_settings
from Source.UI.Menu_Button import create_menu_button

settings = None
config = None
particle_system = None

def setup_menu(app_settings, app_config, app_particle_system):
    global settings, config, particle_system

    settings = app_settings
    config = app_config
    particle_system = app_particle_system

    create_tray_icon()

    threading.Thread(
        target=icon.run,
        daemon=True
    ).start()


def tray_reset_position(icon, item):
    reset_position(config)

def tray_restart_app(icon, item):
    restart_application(config, icon)

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
                "Reset Clock Position",
                tray_reset_position
            ),


            pystray.MenuItem(
                "Restart Application",
                tray_restart_app
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Quit Application",
                tray_quit_app
            ),
        ),
    )

def toggle_menu(event=None):

    actions = {
        "reset_position": lambda: reset_position(config),
        "quit": lambda: shutdown(config, icon),
        "restart": lambda: restart_application(config, icon),

        "disable_particles": lambda disabled:
            particle_system.set_disabled(
                "Bubbles",
                disabled
            ),

        "always_on_top": set_always_on_top,
        "sound_volume": 100,

        "timezone_changed": timezone_changed
    }

    open_settings(
        root,
        settings,
        config,
        actions
    )
    
create_menu_button(toggle_menu)