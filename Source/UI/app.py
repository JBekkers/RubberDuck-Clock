from Source.Window_Manager import root
from Source.Config.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from Source.Config.config import save_config


def reset_position(config):

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