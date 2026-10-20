import pystray
from Source.Window_Manager import root, set_always_on_top
from Source.Config.paths import ASSETS_DIR

from PIL import Image

import os
import threading

from Source.clock import timezone_changed

from Source.UI.app import reset_position, shutdown, restart_application
from Source.UI.Menu_Tabs.tab_loader import open_settings

from Source.UI.Menu_Button import (
    create_menu_button,
    set_reward_claim_callback,
    set_reward_available,
)

hat_manager = None
reward_timer_running = False

settings = None
config = None
particle_system = None
stats = None

def check_hat_reward():
    if hat_manager is None:
        return

    available = hat_manager.is_drop_available()

    set_reward_available(available)

    root.after(
        1000,
        check_hat_reward
    )


def claim_hat_reward():
    if hat_manager is None:
        return

    hat = hat_manager.claim_drop()

    if hat is None:
        return

    set_reward_available(False)

    from tkinter import messagebox

    messagebox.showinfo(
        "Hat unlocked!",
        f"You received: {hat['name']}\n"
        f"Rarity: {hat['rarity']}"
    )

def setup_menu(
    app_settings,
    app_config,
    app_stats,
    app_particle_system,
    app_hat_manager
):
    global settings, config, stats, particle_system, hat_manager

    settings = app_settings
    config = app_config
    stats = app_stats
    particle_system = app_particle_system
    hat_manager = app_hat_manager

    set_reward_claim_callback(
        claim_hat_reward
    )

    root.after(
        1000,
        check_hat_reward
    )

    create_tray_icon()

    threading.Thread(
        target=icon.run,
        daemon=True
    ).start()


def tray_reset_position(icon, item):
    reset_position(config)

def tray_restart_app(icon, item):
    restart_application(config, stats, icon)

def tray_quit_app(icon, item):
    root.after(
        0,
        lambda: shutdown(config, stats, icon)
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
        "quit": lambda: shutdown(config, stats, icon),
        "restart": lambda: restart_application(config, stats, icon),

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
        stats,
        actions,
        hat_manager
    )
    
create_menu_button(toggle_menu)