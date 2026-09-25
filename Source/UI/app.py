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


pos_save_job = None
last_pos = None

def schedule_pos_save(event, config):
    global pos_save_job, last_pos

    pos = (root.winfo_x(), root.winfo_y())

    if pos == last_pos:
        return

    last_pos = pos

    if pos_save_job:
        root.after_cancel(pos_save_job)

    pos_save_job = root.after(
        400,
        lambda: save_current_pos(config)
    )


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

_last_saved_uptime = 0

def save_uptime(stats):
    global _last_saved_uptime

    session_time = int(get_session_uptime())

    # Only add time that has not already been saved.
    elapsed = session_time - _last_saved_uptime

    if elapsed <= 0:
        return

    # Save only the new time.
    stats["total_uptime"] = (
        stats.get("total_uptime", 0) + elapsed
    )

    if save_stats(stats):
        _last_saved_uptime = session_time
    else:
        # Undo the in-memory change if saving failed.
        stats["total_uptime"] -= elapsed

def start_uptime_autosave(stats, interval_ms=30_000):
    def checkpoint():
        save_uptime(stats)

        # Schedule the next checkpoint.
        root.after(interval_ms, checkpoint)

    root.after(interval_ms, checkpoint)

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
