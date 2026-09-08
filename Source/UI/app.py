from Source.Window_Manager import root
from Source.Config.style import WINDOW_HEIGHT, WINDOW_WIDTH
from Source.UI.Menu_Tabs.tab_loader import position_menu
from Source.Config.stats import save_stats
from Source.Config.config import save_config
from Source.Config.paths import FONTS_DIR
from Source.UI.Menu_Tabs.stats import get_session_uptime

import ctypes

import os
import sys
import subprocess

def prepare_shutdown(config, stats, icon=None):
    save_current_pos(config)
    save_uptime(stats)

    if icon:
        try:
            icon.stop()
        except Exception:
            pass

def save_current_pos(config):
    config["position"]["x"] = root.winfo_x()
    config["position"]["y"] = root.winfo_y()

    save_config(config)

def reset_position(config):

    default_x = 915
    default_y = 0

    config["position"]["x"] = default_x
    config["position"]["y"] = default_y

    save_config(config)

    def move():
        root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{default_x}+{default_y}"
        )

        root.update_idletasks()
        position_menu(root)

    root.after(0, move)


def save_uptime(stats):
    session_time = get_session_uptime()

    stats["total_uptime"] = (
        stats.get("total_uptime", 0)
        + session_time
    )

    save_stats(stats)

def shutdown(config, stats, icon=None):
    prepare_shutdown(config, stats, icon)
    root.destroy()

FR_PRIVATE = 0x10

def load_font(filename):
    path = os.path.join(FONTS_DIR, filename)

    if os.path.exists(path):
        ctypes.windll.gdi32.AddFontResourceExW(
            path,
            FR_PRIVATE,
            0
        )

def restart_application(config, stats, icon=None):
    prepare_shutdown(config, stats, icon)

    subprocess.Popen(
        [sys.executable] + sys.argv
    )

    root.destroy()
