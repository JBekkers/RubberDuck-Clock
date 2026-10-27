import os
import json
import copy

from Source.Config.paths import CONFIG_DIR
from Source.Config.error_handler import logger

os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(
    CONFIG_DIR,
    "config.json"
)

DEFAULT_CONFIG = {
    "position": {
        "x": 915,
        "y": 0
    },

    "settings": {
        "hourly_quack": False,
        "always_on_top": True,
        "disable_particles": False,

        "auto_timezone": True,
        "timezone": "Europe/Amsterdam",
        "clock_24_hour": True,
    }
}

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)

        if not isinstance(config, dict):
            raise ValueError(
                "Configuration root must be a JSON object."
            )

        for section, defaults in DEFAULT_CONFIG.items():
            section_data = config.get(section)

            if not isinstance(section_data, dict):
                config[section] = copy.deepcopy(defaults)
                continue

            for key, default_value in defaults.items():
                if key not in section_data:
                    section_data[key] = copy.deepcopy(default_value)

        # Validate position coordinates.
        position = config["position"]

        for key in ("x", "y"):
            value = position.get(key)

            if (
                not isinstance(value, int)
                or isinstance(value, bool)
            ):
                position[key] = DEFAULT_CONFIG["position"][key]

        # Validate setting value types against defaults.
        settings_data = config["settings"]

        for key, default_value in DEFAULT_CONFIG["settings"].items():
            value = settings_data.get(key)

            if not isinstance(value, type(default_value)):
                settings_data[key] = copy.deepcopy(default_value)

        return config

    except (OSError, ValueError, TypeError):
        logger.exception("Failed to load configuration.")
        return copy.deepcopy(DEFAULT_CONFIG)


def save_config(config):
    temp_file = CONFIG_FILE + ".tmp"

    try:
        with open(temp_file, "w") as f:
            json.dump(
                config,
                f,
                indent=4
            )

        os.replace(
            temp_file,
            CONFIG_FILE
        )

    except Exception:
        logger.exception(
            "Failed to save configuration."
        )

        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except OSError:
            pass