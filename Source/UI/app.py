from Source.Window_Manager import root
from Source.Config.style import WINDOW_HEIGHT, WINDOW_WIDTH
from Source.UI.Menu_Tabs.tab_loader import position_menu
from Source.Config.config import save_config
from Source.Config.paths import FONTS_DIR
import os
import ctypes

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


def shutdown(config, icon=None):

    try:
        x = root.winfo_x()
        y = root.winfo_y()

        config["position"]["x"] = x
        config["position"]["y"] = y

        save_config(config)

    except Exception:
        pass


    if icon:
        try:
            icon.stop()
        except Exception:
            pass

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